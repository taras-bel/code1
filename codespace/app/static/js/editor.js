
function logToServer(sessionId, type, details) {
  fetch('/api/log_event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      event_type: type,
      details: details
    })
  });
}


document.addEventListener('DOMContentLoaded', function() {
    // ==================== 1. ИНИЦИАЛИЗАЦИЯ ====================
    if (typeof require === 'undefined') {
        console.error('RequireJS не загружен');
        showFlashMessage('Ошибка загрузки редактора: требуется RequireJS', 'danger');
        return;
    }

    require.config({
        paths: { 
            'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs' 
        },
        waitSeconds: 30
    });

    // ==================== 2. ЗАГРУЗКА MONACO ====================
    require(['vs/editor/editor.main.js'], function() {
        console.log('Monaco Editor загружен');

        // ==================== 3. КОНФИГУРАЦИЯ ====================
        const editorContainer = document.getElementById('editor-container');
        if (!editorContainer) {
            console.error('Элемент #editor-container не найден');
            return;
        }

        // Все data-атрибуты
        const SESSION_ID = editorContainer.dataset.sessionId;
        const CURRENT_USER_ID = parseInt(editorContainer.dataset.userId, 10);
        const CURRENT_USERNAME = editorContainer.dataset.username;
        let CURRENT_USER_ROLE = editorContainer.dataset.userRole;
        let EDITING_LOCKED = editorContainer.dataset.editingLocked === 'True';
        const INITIAL_FILE_ID = parseInt(editorContainer.dataset.initialFileId, 10) || null;
        const INITIAL_LANGUAGE = editorContainer.dataset.initialLanguage || 'plaintext';

        // Все элементы DOM
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
        const lockSessionBtn = document.getElementById('lockSessionBtn');
        const unlockSessionBtn = document.getElementById('unlockSessionBtn');
        const timerDisplay = document.getElementById('timerDisplay');
        const startTimerBtn = document.getElementById('startTimerBtn');
        const timerDurationInput = document.getElementById('timerDuration');
        const copySessionBtn = document.getElementById('copySessionBtn');
        const manageParticipantsBtn = document.getElementById('manageParticipantsBtn');

        // Состояние
        let currentFileId = INITIAL_FILE_ID;
        let files = {};
        let collaborators = {};
        let editor;
        let timerInterval = null;
        let timeRemaining = 0;

        // ==================== 4. ТЕМА РЕДАКТОРА ====================
        monaco.editor.defineTheme('code-share-theme', {
            base: 'vs',
            inherit: true,
            rules: [
                { token: 'comment', foreground: '008800', fontStyle: 'italic' },
                { token: 'keyword', foreground: '0000FF' }
            ],
            colors: {
                'editor.background': '#F8F9FA',
                'editor.lineHighlightBackground': '#E9ECEF',
                'editorLineNumber.foreground': '#6C757D',
                'editorCursor.foreground': '#000000',
                'editor.selectionBackground': '#3390FF33'
            }
        });

        // ==================== 5. ИНИЦИАЛИЗАЦИЯ РЕДАКТОРА ====================
        function initializeEditor() {
            editor = monaco.editor.create(editorContainer, {
                value: '',
                language: INITIAL_LANGUAGE,
                theme: 'code-share-theme',
                automaticLayout: true,
                readOnly: EDITING_LOCKED || !['owner', 'editor'].includes(CURRENT_USER_ROLE),
                minimap: { enabled: true },
                fontSize: 14,
                lineNumbers: 'on',
                roundedSelection: true,
                scrollBeyondLastLine: false,
                renderWhitespace: 'none',
                tabSize: 4,
                quickSuggestions: false
            });

            // Блокировка горячих клавиш
            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyC, function() {
                if (EDITING_LOCKED) {
                    showFlashMessage('Копирование заблокировано', 'warning');
                    return;
                }
                document.execCommand('copy');
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, function() {
                if (EDITING_LOCKED) {
                    showFlashMessage('Вставка заблокирована', 'warning');
                    return;
                }
                document.execCommand('paste');
            });

            // Обработчик изменений
            editor.onDidChangeModelContent(throttle(function(e) {
                if (!editor._isApplyingRemoteEdit && currentFileId) {
                    socket.emit('code_change', {
                        sessionId: SESSION_ID,
                        fileId: currentFileId,
                        changes: e.changes,
                        cursorPosition: editor.getPosition(),
                        userId: CURRENT_USER_ID,
                        username: CURRENT_USERNAME
                    });
                }
            }, 300));
        }

        // ==================== 6. SOCKET.IO ====================
        const socket = io();

        // Все обработчики подключения
        socket.on('connect', function() {
            console.log('Подключено к серверу');
            socket.emit('join', {
                sessionId: SESSION_ID,
                userId: CURRENT_USER_ID,
                username: CURRENT_USERNAME
            });
        });

        socket.on('disconnect', function() {
            console.log('Отключено от сервера');
            showFlashMessage('Потеряно соединение с сервером', 'warning');
        });

        socket.on('connect_error', function(err) {
            console.error('Ошибка подключения:', err);
            showFlashMessage('Ошибка соединения: ' + err.message, 'danger');
        });

        // Обработчики управления доступом
        socket.on('session_locked', function() {
            EDITING_LOCKED = true;
            updateEditorState();
            showFlashMessage('Редактирование заблокировано владельцем', 'warning');
        });

        socket.on('session_unlocked', function() {
            EDITING_LOCKED = false;
            updateEditorState();
            showFlashMessage('Редактирование разблокировано', 'success');
        });

        socket.on('role_updated', function(data) {
            if (data.userId === CURRENT_USER_ID) {
                CURRENT_USER_ROLE = data.newRole;
                showFlashMessage('Ваша роль изменена: ' + data.newRole, 'info');
                updateEditorState();
            }
        });

        // Обработчики файлов
        socket.on('load_file_content', function(data) {
            currentFileId = data.fileId;
            if (editor) {
                editor.setValue(data.content);
                monaco.editor.setModelLanguage(editor.getModel(), data.language);
                if (languageSelect) languageSelect.value = data.language;
                if (activeFileNameDisplay) {
                    activeFileNameDisplay.textContent = files[data.fileId]?.name || data.fileName || 'Новый файл';
                }
                updateFileListSelection();
            }
        });

        socket.on('file_added', function(data) {
            files[data.file.id] = data.file;
            updateFileList();
            showFlashMessage('Файл добавлен: ' + data.file.name, 'success');
        });

        socket.on('file_deleted', function(data) {
            const fileName = files[data.fileId]?.name || 'файл';
            delete files[data.fileId];
            if (currentFileId === data.fileId) {
                const firstFile = Object.values(files)[0];
                if (firstFile) {
                    socket.emit('switch_file', { sessionId: SESSION_ID, fileId: firstFile.id });
                } else {
                    currentFileId = null;
                    if (editor) editor.setValue('');
                }
            }
            updateFileList();
            showFlashMessage('Файл удален: ' + fileName, 'info');
        });

        // Обработчики участников
        socket.on('participants_update', function(data) {
            collaborators = {};
            if (!participantsList) return;
            
            participantsList.innerHTML = '';
            data.participants.forEach(participant => {
                collaborators[participant.id] = participant;
                
                const item = document.createElement('li');
                item.className = 'list-group-item d-flex align-items-center';
                
                const badgeClass = participant.role === 'owner' ? 'bg-success' : 
                                 participant.role === 'editor' ? 'bg-primary' : 'bg-info';
                
                item.innerHTML = `
                    <span class="badge ${badgeClass} me-2">${participant.role}</span>
                    <strong>${participant.username}</strong>
                    ${participant.id === CURRENT_USER_ID ? '<span class="ms-auto text-muted small">(Вы)</span>' : ''}
                `;
                
                participantsList.appendChild(item);
            });
        });

        // Обработчики чата
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
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });

        // Обработчики выполнения кода
        socket.on('execution_started', function(data) {
            if (outputContent) {
                outputContent.textContent = data.message;
                outputContent.style.color = '#f8f9fa';
            }
        });

        socket.on('execution_result', function(data) {
            if (outputContent) {
                outputContent.textContent = data.output;
                outputContent.style.color = data.output.toLowerCase().includes('error') ? '#ff6b6b' : '#51cf66';
            }
        });

        // Обработчики таймера
        socket.on('timer_updated', function(data) {
            if (timerInterval) clearInterval(timerInterval);
            timeRemaining = data.remaining;
            updateTimerDisplay();
            
            if (data.is_running) {
                startTimerCountdown();
            }
        });

        // ==================== 7. ФУНКЦИИ УПРАВЛЕНИЯ ====================
        // Блокировка/разблокировка
        function lockSession() {
            socket.emit('lock_session', { sessionId: SESSION_ID });
        }

        function unlockSession() {
            socket.emit('unlock_session', { sessionId: SESSION_ID });
        }

        // Таймер
        function startTimer() {
            const minutes = parseInt(timerDurationInput.value) || 60;
            socket.emit('start_timer', {
                sessionId: SESSION_ID,
                duration: minutes
            });
        }

        function startTimerCountdown() {
            timerInterval = setInterval(() => {
                timeRemaining--;
                updateTimerDisplay();
                
                if (timeRemaining <= 0) {
                    clearInterval(timerInterval);
                    showFlashMessage('Время сессии истекло!', 'danger');
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            if (!timerDisplay) return;
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            timerDisplay.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        }

        // Управление файлами
        function updateFileList() {
            if (!fileListElement) return;
            
            fileListElement.innerHTML = '';
            const sortedFiles = Object.values(files).sort((a, b) => {
                if (a.is_main) return -1;
                if (b.is_main) return 1;
                return a.name.localeCompare(b.name);
            });
            
            sortedFiles.forEach(file => {
                const item = document.createElement('li');
                item.className = `list-group-item d-flex justify-content-between align-items-center file-item ${
                    file.id === currentFileId ? 'active' : ''
                }`;
                item.dataset.fileId = file.id;
                
                const canModify = ['owner', 'editor'].includes(CURRENT_USER_ROLE);
                const isMain = file.is_main;
                
                item.innerHTML = `
                    <a href="#" class="text-decoration-none text-reset flex-grow-1">
                        ${file.name} <span class="badge bg-secondary">${file.language}</span>
                        ${isMain ? '<span class="badge bg-success">Основной</span>' : ''}
                    </a>
                    <div class="file-actions ms-2">
                        ${canModify && !isMain ? `
                            <button class="btn btn-sm btn-outline-info set-main-file-btn">
                                <i class="fas fa-star"></i>
                            </button>` : ''}
                        ${canModify && sortedFiles.length > 1 ? `
                            <button class="btn btn-sm btn-outline-danger delete-file-btn">
                                <i class="fas fa-trash-alt"></i>
                            </button>` : ''}
                    </div>
                `;
                
                // Обработчики для кнопок файлов
                item.querySelector('a').addEventListener('click', function(e) {
                    e.preventDefault();
                    if (file.id !== currentFileId) {
                        socket.emit('switch_file', {
                            sessionId: SESSION_ID,
                            fileId: file.id
                        });
                    }
                });

                const setMainBtn = item.querySelector('.set-main-file-btn');
                if (setMainBtn) {
                    setMainBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        socket.emit('set_main_file', {
                            sessionId: SESSION_ID,
                            fileId: file.id
                        });
                    });
                }

                const deleteBtn = item.querySelector('.delete-file-btn');
                if (deleteBtn) {
                    deleteBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        if (confirm(`Удалить файл "${file.name}"?`)) {
                            socket.emit('delete_file', {
                                sessionId: SESSION_ID,
                                fileId: file.id
                            });
                        }
                    });
                }
                
                fileListElement.appendChild(item);
            });
        }

        function updateFileListSelection() {
            if (!fileListElement) return;
            fileListElement.querySelectorAll('.file-item').forEach(item => {
                const fileId = parseInt(item.dataset.fileId, 10);
                item.classList.toggle('active', fileId === currentFileId);
            });
        }

        // Обновление состояния редактора
        function updateEditorState() {
            const canEdit = ['owner', 'editor'].includes(CURRENT_USER_ROLE);
            const isLocked = EDITING_LOCKED;
            
            if (editor) {
                editor.updateOptions({ readOnly: !canEdit || isLocked });
            }
            
            if (languageSelect) languageSelect.disabled = !canEdit || isLocked;
            if (runCodeBtn) runCodeBtn.disabled = !canEdit || isLocked;
            if (chatInput) chatInput.disabled = isLocked;
            if (sendMessageBtn) sendMessageBtn.disabled = isLocked;
            
            if (editingLockStatusDisplay) {
                editingLockStatusDisplay.textContent = isLocked ? 
                    ' (Редактирование заблокировано)' : ' (Редактирование разблокировано)';
                editingLockStatusDisplay.className = isLocked ? 
                    'ms-2 text-danger' : 'ms-2 text-success';
            }
            
            if (currentUserRoleDisplay) {
                currentUserRoleDisplay.textContent = `Ваша роль: ${CURRENT_USER_ROLE}`;
                currentUserRoleDisplay.className = `badge bg-${
                    canEdit ? 'primary' : 'info'
                } ms-2`;
            }
            
            // Кнопки блокировки/разблокировки
            if (lockSessionBtn) lockSessionBtn.disabled = isLocked || CURRENT_USER_ROLE !== 'owner';
            if (unlockSessionBtn) unlockSessionBtn.disabled = !isLocked || CURRENT_USER_ROLE !== 'owner';
        }

        // Вспомогательные функции
        function showFlashMessage(message, type) {
            const container = document.createElement('div');
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1100';
            
            container.innerHTML = `
                <div class="alert alert-${type} alert-dismissible fade show">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            document.body.appendChild(container);
            
            setTimeout(() => {
                container.remove();
            }, 5000);
        }

        function throttle(func, limit) {
            let lastFunc;
            let lastRan;
            return function() {
                const context = this;
                const args = arguments;
                if (!lastRan) {
                    func.apply(context, args);
                    lastRan = Date.now();
                } else {
                    clearTimeout(lastFunc);
                    lastFunc = setTimeout(function() {
                        if ((Date.now() - lastRan) >= limit) {
                            func.apply(context, args);
                            lastRan = Date.now();
                        }
                    }, limit - (Date.now() - lastRan));
                }
            };
        }

        // Инициализация файлов
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

        // ==================== 8. ИНИЦИАЛИЗАЦИЯ ====================
        initializeEditor();
        initializeFiles();
        updateEditorState();
        updateFileList();

        // Обработчики кнопок
        if (lockSessionBtn) {
            lockSessionBtn.addEventListener('click', lockSession);
        }

        if (unlockSessionBtn) {
            unlockSessionBtn.addEventListener('click', unlockSession);
        }

        if (startTimerBtn && timerDurationInput) {
            startTimerBtn.addEventListener('click', startTimer);
        }

        if (copySessionBtn) {
            copySessionBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(SESSION_ID).then(() => {
                    showFlashMessage('ID сессии скопирован', 'success');
                });
            });
        }

        if (manageParticipantsBtn) {
            manageParticipantsBtn.addEventListener('click', function() {
                window.location.href = `/session/${SESSION_ID}/manage`;
            });
        }

    }, function(error) {
        console.error('Ошибка загрузки Monaco Editor:', error);
        showFlashMessage('Не удалось загрузить редактор кода', 'danger');
    });
});

// Инициализация CodeSession после загрузки данных
if (window.SESSION_BOOTSTRAP) {
  const { sessionConfig, filesData, activeFileData, participantsData, userData } = window.SESSION_BOOTSTRAP;

  window.codeSession = new CodeSession({
    sessionId: sessionConfig.id,
    userId: userData.id,
    username: userData.username,
    userRole: userData.role,
    editingLocked: sessionConfig.editing_locked,
    initialFileId: activeFileData ? activeFileData.id : null,
    initialLanguage: activeFileData ? activeFileData.language : sessionConfig.language,
    initialFiles: filesData,
    initialParticipants: participantsData
  });
}


// Логирование смены вкладок (в фоне / активен)
document.addEventListener('visibilitychange', () => {
  const hidden = document.hidden;
  const status = hidden ? 'hidden' : 'visible';
  if (window.codeSession) {
    logToServer(codeSession.sessionId, 'tab_visibility_change', {
      user: codeSession.username,
      visibility: status
    });
  }
});
