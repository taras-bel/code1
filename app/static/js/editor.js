document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple editor initialized');

    // Get editor element
    const editor = document.getElementById('editor');
    if (!editor) {
        console.error('Editor element not found');
        return;
    }

    // Extract data attributes
    const SESSION_ID = editor.dataset.sessionId;
    const CURRENT_USER_ID = parseInt(editor.dataset.userId, 10);
    const CURRENT_USERNAME = editor.dataset.username;
    let CURRENT_USER_ROLE = editor.dataset.userRole;
    let EDITING_LOCKED = editor.dataset.editingLocked === 'True';
    const INITIAL_FILE_ID = parseInt(editor.dataset.initialFileId, 10) || null;
    const INITIAL_LANGUAGE = editor.dataset.initialLanguage || 'plaintext';

    // Get other DOM elements
    const languageSelect = document.getElementById('languageSelect');
    const runCodeBtn = document.getElementById('executeCodeBtn');
    const outputContent = document.getElementById('outputContent');
    const chatInput = document.getElementById('chatInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const chatMessages = document.getElementById('chatMessages');
    const participantsList = document.getElementById('participantsList');
    const activeFileNameDisplay = document.getElementById('activeFileName');
    const currentUserRoleDisplay = document.getElementById('currentUserRole');
    const editingLockStatusDisplay = document.getElementById('editingLockStatus');
    const fileListElement = document.getElementById('fileList');

    // Current state
    let currentFileId = INITIAL_FILE_ID;
    let files = {};
    let collaborators = {};

    // Initialize Socket.IO connection
    const socket = io();

    // Socket event handlers
    socket.on('connect', function() {
        console.log('Connected to WebSocket server');
        socket.emit('join', {
            sessionId: SESSION_ID,
            userId: CURRENT_USER_ID,
            username: CURRENT_USERNAME
        });
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from WebSocket server');
    });

    socket.on('error', function(data) {
        console.error('Socket error:', data.message);
        showFlashMessage(data.message, 'danger');
    });

    // File content handling
    socket.on('load_file_content', function(data) {
        console.log('Received file content:', data);
        currentFileId = data.fileId;
        editor.value = data.content;
        
        if (activeFileNameDisplay) {
            activeFileNameDisplay.textContent = files[data.fileId]?.name || data.fileName || 'Новый файл';
        }
        
        if (languageSelect && data.language) {
            languageSelect.value = data.language;
        }
        
        updateEditorState();
        updateActiveFileInList();
    });

    socket.on('code_update', function(data) {
        if (data.fileId === currentFileId && data.userId !== CURRENT_USER_ID) {
            editor.value = data.currentContent;
        }
    });

    socket.on('editor_revert', function(data) {
        if (data.fileId === currentFileId) {
            editor.value = data.content;
            showFlashMessage('Ваши изменения были отменены', 'warning');
        }
    });

    // Session state handling
    socket.on('session_config', function(data) {
        CURRENT_USER_ROLE = data.current_user_role;
        EDITING_LOCKED = data.editing_locked;
        updateEditorState();
    });

    socket.on('role_updated', function(data) {
        if (data.userId === CURRENT_USER_ID) {
            CURRENT_USER_ROLE = data.newRole;
            showFlashMessage(data.message, 'info');
            updateEditorState();
        }
    });

    // File management
    socket.on('file_added', function(data) {
        const newFile = data.file;
        files[newFile.id] = newFile;
        updateFileList();
        showFlashMessage(`Файл "${newFile.name}" добавлен`, 'success');
    });

    socket.on('file_deleted', function(data) {
        const deletedFileId = data.fileId;
        const deletedFileName = files[deletedFileId]?.name || 'файл';
        delete files[deletedFileId];
        
        if (currentFileId === deletedFileId) {
            const firstFile = Object.values(files)[0];
            if (firstFile) {
                socket.emit('switch_file', { sessionId: SESSION_ID, fileId: firstFile.id });
            } else {
                currentFileId = null;
                editor.value = '';
                editor.readOnly = true;
                if (activeFileNameDisplay) activeFileNameDisplay.textContent = 'Нет активного файла';
            }
        }
        
        updateFileList();
        showFlashMessage(`Файл "${deletedFileName}" удален`, 'info');
    });

    socket.on('main_file_changed', function(data) {
        Object.values(files).forEach(f => {
            f.is_main = (f.id === data.fileId);
        });
        updateFileList();
        showFlashMessage(`Основной файл изменен на "${files[data.fileId]?.name || data.fileId}"`, 'info');
    });

    // Participants handling
    socket.on('participants_update', function(data) {
        if (!participantsList) return;
        
        participantsList.innerHTML = '';
        const newCollaborators = {};
        
        data.participants.forEach(participant => {
            newCollaborators[participant.id] = participant;
            
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item d-flex align-items-center';
            
            let badgeClass = 'bg-info';
            if (participant.role === 'owner') badgeClass = 'bg-success';
            else if (participant.role === 'editor') badgeClass = 'bg-primary';
            
            listItem.innerHTML = `
                <span class="badge ${badgeClass} me-2">${participant.role}</span>
                <strong>${participant.username}</strong>
                ${participant.id === CURRENT_USER_ID ? '<span class="ms-auto text-muted small">(Вы)</span>' : ''}
                ${participant.id !== CURRENT_USER_ID && participant.current_file_id === currentFileId ? 
                    '<span class="ms-auto text-muted small">(редактирует этот файл)</span>' : ''}
            `;
            
            participantsList.appendChild(listItem);
        });
        
        collaborators = newCollaborators;
    });

    // Chat handling
    socket.on('new_message', function(data) {
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message mb-2';
        
        const timestamp = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageElement.innerHTML = `
            <strong>${data.user}</strong>
            <span class="text-muted small">${timestamp}</span>:
            ${data.message}
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollTop + 1000;
    });

    // Execution handling
    socket.on('execution_started', function(data) {
        if (outputContent) {
            outputContent.textContent = data.message;
            outputContent.style.color = '#f8f9fa';
        }
    });

    socket.on('execution_result', function(data) {
        if (outputContent) {
            outputContent.textContent = data.output;
            if (data.output.toLowerCase().includes('error') || data.output.toLowerCase().includes('exception')) {
                outputContent.style.color = '#ff6b6b';
            } else {
                outputContent.style.color = '#51cf66';
            }
        }
    });

    // UI event handlers
    if (languageSelect) {
        languageSelect.addEventListener('change', function() {
            if (currentFileId) {
                socket.emit('update_file_language', {
                    sessionId: SESSION_ID,
                    fileId: currentFileId,
                    language: languageSelect.value
                });
            }
        });
    }

    if (runCodeBtn) {
        runCodeBtn.addEventListener('click', function() {
            if (currentFileId) {
                socket.emit('execute_code', {
                    sessionId: SESSION_ID,
                    fileId: currentFileId
                });
            }
        });
    }

    if (sendMessageBtn && chatInput) {
        function sendChatMessage() {
            const message = chatInput.value.trim();
            if (message) {
                socket.emit('chat_message', {
                    sessionId: SESSION_ID,
                    message: message
                });
                chatInput.value = '';
            }
        }
        
        sendMessageBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }

    // File list handling
    function updateFileList() {
        if (!fileListElement) return;
        
        fileListElement.innerHTML = '';
        
        const sortedFiles = Object.values(files).sort((a, b) => {
            if (a.is_main) return -1;
            if (b.is_main) return 1;
            return a.name.localeCompare(b.name);
        });
        
        sortedFiles.forEach(file => {
            const listItem = document.createElement('li');
            listItem.className = `list-group-item d-flex justify-content-between align-items-center file-item ${file.id === currentFileId ? 'active' : ''}`;
            listItem.dataset.fileId = file.id;
            listItem.dataset.fileName = file.name;
            listItem.dataset.fileLanguage = file.language;
            
            const canModify = CURRENT_USER_ROLE === 'owner' || CURRENT_USER_ROLE === 'editor';
            const isMain = file.is_main;
            
            listItem.innerHTML = `
                <a href="#" class="text-decoration-none text-reset flex-grow-1">
                    ${file.name} <span class="badge bg-secondary">${file.language}</span>
                    ${isMain ? '<span class="badge bg-success">Основной</span>' : ''}
                </a>
                <div class="file-actions ms-2">
                    ${canModify && !isMain ? `
                        <button type="button" class="btn btn-sm btn-outline-info set-main-file-btn" title="Сделать основным">
                            <i class="fas fa-code"></i>
                        </button>` : ''}
                    ${canModify && sortedFiles.length > 1 ? `
                        <button type="button" class="btn btn-sm btn-outline-danger delete-file-btn" title="Удалить файл">
                            <i class="fas fa-times"></i>
                        </button>` : ''}
                </div>
            `;
            
            listItem.querySelector('a').addEventListener('click', function(e) {
                e.preventDefault();
                if (file.id !== currentFileId) {
                    socket.emit('switch_file', {
                        sessionId: SESSION_ID,
                        fileId: file.id
                    });
                }
            });

            if (canModify) {
                if (!isMain) {
                    listItem.querySelector('.set-main-file-btn')?.addEventListener('click', function(e) {
                        e.stopPropagation();
                        socket.emit('set_main_file_socket', {
                            sessionId: SESSION_ID,
                            fileId: file.id
                        });
                    });
                }

                if (sortedFiles.length > 1) {
                    listItem.querySelector('.delete-file-btn')?.addEventListener('click', function(e) {
                        e.stopPropagation();
                        if (confirm(`Вы уверены, что хотите удалить файл "${file.name}"?`)) {
                            socket.emit('delete_file_socket', {
                                sessionId: SESSION_ID,
                                fileId: file.id
                            });
                        }
                    });
                }
            }

            fileListElement.appendChild(listItem);
        });
    }

    function updateActiveFileInList() {
        if (!fileListElement) return;
        
        fileListElement.querySelectorAll('.file-item').forEach(item => {
            const fileId = parseInt(item.dataset.fileId, 10);
            item.classList.toggle('active', fileId === currentFileId);
        });
    }

    // Editor state management
    function updateEditorState() {
        const canEdit = CURRENT_USER_ROLE === 'owner' || CURRENT_USER_ROLE === 'editor';
        const isLocked = EDITING_LOCKED;
        editor.readOnly = !canEdit || isLocked;
        
        if (languageSelect) languageSelect.disabled = editor.readOnly;
        if (runCodeBtn) runCodeBtn.disabled = editor.readOnly;
        if (chatInput) chatInput.disabled = isLocked;
        if (sendMessageBtn) sendMessageBtn.disabled = isLocked;
        
        if (editingLockStatusDisplay) {
            editingLockStatusDisplay.textContent = isLocked ? ' (Редактирование заблокировано)' : ' (Редактирование разблокировано)';
            editingLockStatusDisplay.className = isLocked ? 'ms-2 text-danger' : 'ms-2 text-success';
        }
        
        if (currentUserRoleDisplay) {
            currentUserRoleDisplay.textContent = `Ваша роль: ${CURRENT_USER_ROLE}`;
            currentUserRoleDisplay.className = `badge bg-${canEdit ? 'primary' : 'info'} ms-2`;
        }
    }

    // Content change handling
    editor.addEventListener('input', function() {
        if (!editor.readOnly) {
            socket.emit('code_change', {
                sessionId: SESSION_ID,
                fileId: currentFileId,
                currentContent: editor.value
            });
        }
    });

    // Helper functions
    function showFlashMessage(message, type) {
        const flashContainer = document.createElement('div');
        flashContainer.className = 'position-fixed top-0 end-0 p-3';
        flashContainer.style.zIndex = '1100';
        
        flashContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        document.body.appendChild(flashContainer);
        
        setTimeout(() => {
            flashContainer.remove();
        }, 5000);
    }

    // Initialize file list from server-side data
    function initializeFiles() {
        if (fileListElement) {
            fileListElement.querySelectorAll('.file-item').forEach(item => {
                const fileId = parseInt(item.dataset.fileId, 10);
                files[fileId] = {
                    id: fileId,
                    name: item.dataset.fileName,
                    language: item.dataset.fileLanguage,
                    is_main: item.querySelector('.badge.bg-success') !== null
                };
            });
        }
    }

    // Initial setup
    initializeFiles();
    updateEditorState();
    updateFileList();
    setupCopyPasteProtection();
});
