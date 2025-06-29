from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session as flask_session
from flask_login import login_required, current_user
from datetime import datetime
import json
import os
from app.models.models import Session, File, User, CollaborationRole, ChatMessage
from app.extensions import db
from app.services.session_manager import SessionManager

main_bp = Blueprint('main_bp', __name__)

# Полный список всех языков программирования
LANGUAGES = {
    'python': {'name': 'Python', 'mode': 'python', 'file_extension': 'py'},
    'javascript': {'name': 'JavaScript', 'mode': 'javascript', 'file_extension': 'js'},
    'typescript': {'name': 'TypeScript', 'mode': 'typescript', 'file_extension': 'ts'},
    'java': {'name': 'Java', 'mode': 'java', 'file_extension': 'java'},
    'c': {'name': 'C', 'mode': 'c', 'file_extension': 'c'},
    'cpp': {'name': 'C++', 'mode': 'cpp', 'file_extension': 'cpp'},
    'csharp': {'name': 'C#', 'mode': 'csharp', 'file_extension': 'cs'},
    'go': {'name': 'Go', 'mode': 'go', 'file_extension': 'go'},
    'rust': {'name': 'Rust', 'mode': 'rust', 'file_extension': 'rs'},
    'ruby': {'name': 'Ruby', 'mode': 'ruby', 'file_extension': 'rb'},
    'php': {'name': 'PHP', 'mode': 'php', 'file_extension': 'php'},
    'html': {'name': 'HTML', 'mode': 'html', 'file_extension': 'html'},
    'css': {'name': 'CSS', 'mode': 'css', 'file_extension': 'css'},
    'json': {'name': 'JSON', 'mode': 'json', 'file_extension': 'json'},
    'xml': {'name': 'XML', 'mode': 'xml', 'file_extension': 'xml'},
    'markdown': {'name': 'Markdown', 'mode': 'markdown', 'file_extension': 'md'},
    'sql': {'name': 'SQL', 'mode': 'sql', 'file_extension': 'sql'},
    'text': {'name': 'Plain Text', 'mode': 'plaintext', 'file_extension': 'txt'},
    'shell': {'name': 'Shell Script', 'mode': 'shell', 'file_extension': 'sh'},
    'dockerfile': {'name': 'Dockerfile', 'mode': 'dockerfile', 'file_extension': 'dockerfile'},
    'yaml': {'name': 'YAML', 'mode': 'yaml', 'file_extension': 'yaml'},
    'ini': {'name': 'INI', 'mode': 'ini', 'file_extension': 'ini'},
    'graphql': {'name': 'GraphQL', 'mode': 'graphql', 'file_extension': 'graphql'},
    'perl': {'name': 'Perl', 'mode': 'perl', 'file_extension': 'pl'},
    'r': {'name': 'R', 'mode': 'r', 'file_extension': 'r'},
    'swift': {'name': 'Swift', 'mode': 'swift', 'file_extension': 'swift'},
    'kotlin': {'name': 'Kotlin', 'mode': 'kotlin', 'file_extension': 'kt'},
    'dart': {'name': 'Dart', 'mode': 'dart', 'file_extension': 'dart'},
    'hcl': {'name': 'HCL (Terraform)', 'mode': 'hcl', 'file_extension': 'hcl'},
    'powershell': {'name': 'PowerShell', 'mode': 'powershell', 'file_extension': 'ps1'},
    'fsharp': {'name': 'F#', 'mode': 'fsharp', 'file_extension': 'fs'},
    'objective-c': {'name': 'Objective-C', 'mode': 'objective-c', 'file_extension': 'm'},
    'vb': {'name': 'Visual Basic', 'mode': 'vb', 'file_extension': 'vb'},
    'scss': {'name': 'SCSS', 'mode': 'scss', 'file_extension': 'scss'},
    'less': {'name': 'LESS', 'mode': 'less', 'file_extension': 'less'},
    'coffeescript': {'name': 'CoffeeScript', 'mode': 'coffeescript', 'file_extension': 'coffee'},
    'batch': {'name': 'Batch', 'mode': 'batch', 'file_extension': 'bat'},
    'clojure': {'name': 'Clojure', 'mode': 'clojure', 'file_extension': 'clj'},
    'elixir': {'name': 'Elixir', 'mode': 'elixir', 'file_extension': 'ex'},
    'erlang': {'name': 'Erlang', 'mode': 'erlang', 'file_extension': 'erl'},
    'fortran': {'name': 'Fortran', 'mode': 'fortran', 'file_extension': 'f'},
    'haskell': {'name': 'Haskell', 'mode': 'haskell', 'file_extension': 'hs'},
    'julia': {'name': 'Julia', 'mode': 'julia', 'file_extension': 'jl'},
    'lisp': {'name': 'Lisp', 'mode': 'lisp', 'file_extension': 'lisp'},
    'lua': {'name': 'Lua', 'mode': 'lua', 'file_extension': 'lua'},
    'matlab': {'name': 'MATLAB', 'mode': 'matlab', 'file_extension': 'm'},
    'pascal': {'name': 'Pascal', 'mode': 'pascal', 'file_extension': 'pas'},
    'prolog': {'name': 'Prolog', 'mode': 'prolog', 'file_extension': 'plg'},
    'scheme': {'name': 'Scheme', 'mode': 'scheme', 'file_extension': 'scm'},
    'gdscript': {'name': 'GDScript', 'mode': 'gdscript', 'file_extension': 'gd'}
}


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Сессии, которыми владеет текущий пользователь
    owned_sessions = Session.query.filter_by(owner_id=current_user.id).order_by(Session.created_at.desc()).all()

    # Сессии, в которых пользователь является коллаборатором
    collaborating_sessions_roles = CollaborationRole.query.filter_by(user_id=current_user.id).all()
    collaborating_session_ids = [role.session_id for role in collaborating_sessions_roles]
    
    # Исключаем сессии, которыми пользователь владеет, чтобы не дублировать
    collaborating_sessions = Session.query.filter(
        Session.id.in_(collaborating_session_ids),
        Session.owner_id != current_user.id
    ).order_by(Session.created_at.desc()).all()

    # Сопоставляем роли для отображения
    session_roles = {role.session_id: role.role for role in collaborating_sessions_roles}

    return render_template('dashboard.html', 
                           owned_sessions=owned_sessions, 
                           collaborating_sessions=collaborating_sessions,
                           session_roles=session_roles)

@main_bp.route('/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        initial_language = request.form.get('initial_language')
        visibility = request.form.get('visibility') # 'public' or 'private'
        
        if not title:
            flash('Название сессии не может быть пустым.', 'danger')
            return redirect(url_for('main_bp.create_session'))

        is_private = (visibility == 'private')

        new_session = Session(
            title=title,
            description=description,
            owner_id=current_user.id,
            language=initial_language,
            is_private=is_private
        )
        db.session.add(new_session)
        db.session.flush() # Получаем ID новой сессии до коммита

        # Добавляем владельца как коллаборатора с ролью 'owner'
        owner_role = CollaborationRole(
            session_id=new_session.id,
            user_id=current_user.id,
            role='owner'
        )
        db.session.add(owner_role)

        # Создаем начальный файл для сессии
        initial_file_name = f"main.{LANGUAGES[initial_language]['file_extension']}" if initial_language in LANGUAGES else "main.txt"
        initial_file_content = "" # Пустое содержимое для нового файла

        new_file = File(
            session_id=new_session.id,
            name=initial_file_name,
            content=initial_file_content,
            language=initial_language,
            is_main=True # Устанавливаем его как основной файл
        )
        db.session.add(new_file)
        
        db.session.commit()
        flash('Сессия успешно создана!', 'success')
        return redirect(url_for('main_bp.session', session_id=new_session.id))
    
    return render_template('create_session.html', languages=LANGUAGES)

@main_bp.route('/session/<string:session_id>') # ИЗМЕНЕНО
@login_required
def session(session_id):
    current_session = Session.query.get_or_404(session_id)
    
    # Проверяем роль текущего пользователя в сессии
    user_role_obj = CollaborationRole.query.filter_by(
        session_id=session_id, user_id=current_user.id
    ).first()

    if not user_role_obj:
        if current_session.is_private:
            flash("У вас нет доступа к этой приватной сессии.", "danger")
            return redirect(url_for('main_bp.dashboard'))
        else:
            # Автоматически добавляем вьюера, если сессия публичная и пользователь не участвует
            new_role = CollaborationRole(session_id=session_id, user_id=current_user.id, role='viewer')
            db.session.add(new_role)
            db.session.commit()
            user_role_obj = new_role # Обновляем объект роли после добавления

    current_user_role = user_role_obj.role

    # Получаем все файлы для этой сессии
    files = File.query.filter_by(session_id=session_id).order_by(File.name).all()
    
    # Определяем активный файл: либо по file_id из query params, либо основной файл, либо первый файл
    active_file_id = request.args.get('file_id', type=int)
    active_file = None
    if active_file_id:
        active_file = next((f for f in files if f.id == active_file_id), None)
    
    if not active_file:
        active_file = next((f for f in files if f.is_main), None)
    
    if not active_file and files:
        active_file = files[0]
    
    # Если файлов нет, то редактор будет пуст, и это нормально.
    # Файл создастся при первой его модификации или добавлении.

    # Получаем всех участников сессии
    participants = []
    for role in current_session.collaboration_roles:
        if role.user: # Убедимся, что пользователь существует
            participants.append({
                'id': role.user.id,
                'username': role.user.username,
                'role': role.role
            })
    
    # Получаем последние 50 сообщений чата
    chat_messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp.desc()).limit(50).all()

    # Подготавливаем данные для JavaScript
    session_data = {
        'id': current_session.id,
        'title': current_session.title,
        'description': current_session.description,
        'owner_id': current_session.owner_id,
        'language': current_session.language,
        'is_private': current_session.is_private,
        'editing_locked': current_session.editing_locked,
        'output': current_session.output,
        'timer_duration': current_session.timer_duration,
        'timer_start_time': current_session.timer_start_time.isoformat() if current_session.timer_start_time else None
    }
    
    files_data = [{
        'id': f.id, 
        'name': f.name, 
        'content': f.content, 
        'language': f.language, 
        'is_main': f.is_main
    } for f in files]

    active_file_data = {
        'id': active_file.id,
        'name': active_file.name,
        'content': active_file.content,
        'language': active_file.language,
        'is_main': active_file.is_main
    } if active_file else None

    # Сериализуем данные в JSON для передачи в JS
    session_json = session_data
    files_json = files_data
    active_file_json = active_file_data
    participants_json = participants

    return render_template('session.html',
        session=current_session, # Передаем объект сессии для использования в Jinja
        session_json=session_json,
        files_json=files_json,
        active_file_json=active_file_json,
        participants_json=participants_json,
        active_file=active_file, # Передаем активный файл для использования в Jinja
        files=files, # Передаем список файлов для использования в Jinja
        participants=participants, # Передаем участников для использования в Jinja
        chat_messages=chat_messages, # Передаем сообщения чата для использования в Jinja
        current_user_role=current_user_role,
        LANGUAGES=LANGUAGES
    )

@main_bp.route('/add_file/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def add_file(session_id):
    current_session = Session.query.get_or_404(session_id)

    # Проверка прав доступа: только владелец или редактор могут добавлять файлы
    user_role_obj = CollaborationRole.query.filter_by(
        session_id=session_id, user_id=current_user.id
    ).first()

    if not user_role_obj or user_role_obj.role not in ['owner', 'editor']:
        flash("У вас нет прав для добавления файлов в эту сессию.", "danger")
        return redirect(url_for('main_bp.session', session_id=session_id))
    
    if current_session.editing_locked:
        flash("Сессия заблокирована для редактирования. Невозможно добавить файл.", "danger")
        return redirect(url_for('main_bp.session', session_id=session_id))

    file_name = request.form.get('file_name')
    file_language = request.form.get('file_language')

    if not file_name or not file_language:
        flash("Имя файла и язык не могут быть пустыми.", "danger")
        return redirect(url_for('main_bp.session', session_id=session_id))

    # Проверка на дублирование имени файла
    existing_file = File.query.filter_by(session_id=session_id, name=file_name).first()
    if existing_file:
        flash(f"Файл с именем '{file_name}' уже существует в этой сессии.", "warning")
        return redirect(url_for('main_bp.session', session_id=session_id))

    new_file = File(
        session_id=session_id,
        name=file_name,
        content="", # Новый файл создается с пустым содержимым
        language=file_language,
        is_main=False # Новый файл по умолчанию не является основным
    )
    db.session.add(new_file)
    db.session.commit()
    flash(f"Файл '{file_name}' успешно добавлен.", "success")
    
    # Отправляем обновление через SocketIO
    SessionManager.emit_file_list_update(session_id, [f.to_dict() for f in current_session.files])
    
    return redirect(url_for('main_bp.session', session_id=session_id, file_id=new_file.id))

@main_bp.route('/delete_file/<string:session_id>/<int:file_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def delete_file(session_id, file_id):
    current_session = Session.query.get_or_404(session_id)
    file_to_delete = File.query.get_or_404(file_id)

    # Проверка, что файл принадлежит данной сессии
    if file_to_delete.session_id != session_id:
        flash("Файл не принадлежит этой сессии.", "danger")
        return jsonify(status="error", message="Файл не принадлежит этой сессии.")

    # Проверка прав доступа: только владелец или редактор могут удалять файлы
    user_role_obj = CollaborationRole.query.filter_by(
        session_id=session_id, user_id=current_user.id
    ).first()

    if not user_role_obj or user_role_obj.role not in ['owner', 'editor']:
        flash("У вас нет прав для удаления файлов из этой сессии.", "danger")
        return jsonify(status="error", message="У вас нет прав для удаления файлов из этой сессии.")
    
    if current_session.editing_locked:
        flash("Сессия заблокирована для редактирования. Невозможно удалить файл.", "danger")
        return jsonify(status="error", message="Сессия заблокирована для редактирования. Невозможно удалить файл.")

    # Нельзя удалить основной файл, если он единственный
    if file_to_delete.is_main and len(current_session.files) == 1:
        flash("Невозможно удалить единственный основной файл сессии.", "danger")
        return jsonify(status="error", message="Невозможно удалить единственный основной файл сессии.")

    db.session.delete(file_to_delete)
    db.session.commit()
    flash(f"Файл '{file_to_delete.name}' успешно удален.", "success")
    
    # Отправляем обновление через SocketIO
    SessionManager.emit_file_list_update(session_id, [f.to_dict() for f in current_session.files])

    # Если удаленный файл был основным, или активным, нужно выбрать новый активный
    if file_to_delete.is_main or request.args.get('file_id', type=int) == file_id:
        new_active_file = File.query.filter_by(session_id=session_id).order_by(File.name).first()
        if new_active_file:
            # Обновляем активный файл на клиентах
            SessionManager.emit_active_file_change(session_id, new_active_file.id)
            return jsonify(status="success", message="Файл удален.", redirect_url=url_for('main_bp.session', session_id=session_id, file_id=new_active_file.id))
        else:
            return jsonify(status="success", message="Файл удален.", redirect_url=url_for('main_bp.session', session_id=session_id))

    return jsonify(status="success", message="Файл удален.")

@main_bp.route('/set_main_file/<string:session_id>/<int:file_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def set_main_file(session_id, file_id):
    current_session = Session.query.get_or_404(session_id)
    file_to_set_main = File.query.get_or_404(file_id)

    if file_to_set_main.session_id != session_id:
        flash("Файл не принадлежит этой сессии.", "danger")
        return jsonify(status="error", message="Файл не принадлежит этой сессии.")

    user_role_obj = CollaborationRole.query.filter_by(
        session_id=session_id, user_id=current_user.id
    ).first()

    if not user_role_obj or user_role_obj.role not in ['owner', 'editor']:
        flash("У вас нет прав для изменения основного файла.", "danger")
        return jsonify(status="error", message="У вас нет прав для изменения основного файла.")

    if current_session.editing_locked:
        flash("Сессия заблокирована для редактирования. Невозможно изменить основной файл.", "danger")
        return jsonify(status="error", message="Сессия заблокирована для редактирования. Невозможно изменить основной файл.")

    # Снимаем флаг is_main со всех остальных файлов в этой сессии
    for file in current_session.files:
        if file.is_main:
            file.is_main = False
    
    # Устанавливаем новый основной файл
    file_to_set_main.is_main = True
    db.session.commit()
    flash(f"Файл '{file_to_set_main.name}' теперь является основным.", "success")

    # Отправляем обновление через SocketIO
    SessionManager.emit_file_list_update(session_id, [f.to_dict() for f in current_session.files])
    SessionManager.emit_active_file_change(session_id, file_to_set_main.id) # Возможно, переключить на него
    
    return jsonify(status="success", message="Основной файл изменен.")

@main_bp.route('/toggle_lock_session/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def toggle_lock_session(session_id):
    current_session = Session.query.get_or_404(session_id)

    if current_session.owner_id != current_user.id:
        flash("Только владелец сессии может блокировать/разблокировать редактирование.", "danger")
        return jsonify(status="error", message="Только владелец сессии может блокировать/разблокировать редактирование.")
    
    current_session.editing_locked = not current_session.editing_locked
    db.session.commit()
    
    status_message = "заблокирована" if current_session.editing_locked else "разблокирована"
    flash(f"Редактирование сессии теперь {status_message}.", "success")
    
    SessionManager.emit_session_lock_status(session_id, current_session.editing_locked)
    
    return jsonify(status="success", locked=current_session.editing_locked, message=f"Сессия {status_message}.")

@main_bp.route('/execute_code/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def execute_code(session_id):
    current_session = Session.query.get_or_404(session_id)

    user_role_obj = CollaborationRole.query.filter_by(
        session_id=session_id, user_id=current_user.id
    ).first()

    if not user_role_obj or user_role_obj.role not in ['owner', 'editor']:
        return jsonify(status="error", output="У вас нет прав для выполнения кода.", success=False)
    
    if current_session.editing_locked:
        return jsonify(status="error", output="Сессия заблокирована для редактирования. Невозможно выполнить код.", success=False)

    code_to_execute = request.json.get('code')
    file_language = request.json.get('language')
    
    if not code_to_execute:
        return jsonify(status="error", output="Нет кода для выполнения.", success=False)

    # Временный файл для выполнения
    temp_dir = 'temp_code_executions'
    os.makedirs(temp_dir, exist_ok=True)
    
    # Генерация уникального имени файла
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_extension = LANGUAGES.get(file_language, {}).get('file_extension', 'txt')
    temp_file_name = f"code_{current_user.id}_{timestamp}.{file_extension}"
    temp_file_path = os.path.join(temp_dir, temp_file_name)

    # Запись кода во временный файл
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(code_to_execute)

    command = []
    output = ""
    error = ""

    try:
        if file_language == 'python':
            command = ['python', temp_file_path]
        elif file_language == 'javascript':
            command = ['node', temp_file_path]
        elif file_language == 'java':
            # Для Java нужно скомпилировать, затем запустить
            class_name = "Main" # Предполагаем, что класс называется Main
            java_file_name = f"{class_name}.java"
            temp_java_file_path = os.path.join(temp_dir, java_file_name)
            with open(temp_java_file_path, 'w', encoding='utf-8') as f:
                # Обновляем имя файла для Java
                f.write(code_to_execute) 
            
            # Компиляция Java
            compile_result = SessionManager.execute_command(['javac', temp_java_file_path], temp_dir)
            if compile_result['stderr']:
                error = compile_result['stderr']
            else:
                command = ['java', '-cp', temp_dir, class_name] # Запуск Java
        elif file_language == 'c' or file_language == 'cpp':
            # Для C/C++ нужно скомпилировать
            executable_name = "a.out"
            if file_language == 'c':
                compiler = 'gcc'
            else:
                compiler = 'g++'
            
            compile_result = SessionManager.execute_command([compiler, temp_file_path, '-o', os.path.join(temp_dir, executable_name)], temp_dir)
            if compile_result['stderr']:
                error = compile_result['stderr']
            else:
                command = [os.path.join(temp_dir, executable_name)] # Запуск скомпилированного файла
        # Добавьте другие языки по мере необходимости
        else:
            output = f"Выполнение для языка '{file_language}' не поддерживается."
            return jsonify(status="error", output=output, success=False)
        
        if command: # Если команда для выполнения была сформирована
            exec_result = SessionManager.execute_command(command, temp_dir)
            output = exec_result['stdout']
            error += exec_result['stderr'] # Добавляем ошибки выполнения к ошибкам компиляции

    except Exception as e:
        error = f"Ошибка при выполнении кода: {str(e)}"
    finally:
        # Очистка временных файлов
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if 'java_file_name' in locals() and os.path.exists(temp_java_file_path):
            os.remove(temp_java_file_path)
        if 'executable_name' in locals() and os.path.exists(os.path.join(temp_dir, executable_name)):
            os.remove(os.path.join(temp_dir, executable_name))


    final_output = (output + "\n" + error).strip()
    if not final_output:
        final_output = "Код выполнен без вывода."

    # Сохраняем вывод в сессии
    current_session.output = final_output
    db.session.commit()

    # Отправляем вывод всем клиентам в сессии
    SessionManager.emit_code_output(session_id, final_output)

    return jsonify(status="success", output=final_output, success=True)

@main_bp.route('/edit_session/<string:session_id>', methods=['GET', 'POST']) # ИЗМЕНЕНО
@login_required
def edit_session(session_id):
    session = Session.query.get_or_404(session_id)

    if session.owner_id != current_user.id:
        flash("У вас нет прав на редактирование этой сессии.", "danger")
        return redirect(url_for('main_bp.dashboard'))

    if request.method == 'POST':
        session.title = request.form['title']
        session.description = request.form['description']
        session.language = request.form['language']
        session.is_private = True if request.form.get('is_private') == 'on' else False
        
        # Обновляем основной файл сессии, если язык изменился и основной файл существует
        main_file = File.query.filter_by(session_id=session.id, is_main=True).first()
        if main_file and main_file.language != session.language:
            main_file.language = session.language
            # Также можно обновить расширение файла, если это необходимо
            main_file.name = f"main.{LANGUAGES[session.language]['file_extension']}" if session.language in LANGUAGES else "main.txt"


        try:
            db.session.commit()
            flash('Сессия успешно обновлена!', 'success')
            return redirect(url_for('main_bp.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обновлении сессии: {e}", "danger")
            flash("Не удалось обновить сессию.", "danger")

        return redirect(url_for('main_bp.dashboard'))

    return render_template('edit_session.html', session=session, languages=LANGUAGES)

@main_bp.route('/join_session/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def join_session(session_id):
    session = Session.query.get_or_404(session_id)

    existing = CollaborationRole.query.filter_by(session_id=session.id, user_id=current_user.id).first()
    if existing:
        flash("Вы уже участвуете в этой сессии.", "info")
        return redirect(url_for('main_bp.dashboard'))

    if session.is_private:
        flash("Эта сессия приватная. Вы не можете присоединиться без приглашения.", "danger")
        return redirect(url_for('main_bp.dashboard'))

    role = CollaborationRole(session_id=session.id, user_id=current_user.id, role="viewer")
    db.session.add(role)
    db.session.commit()

    flash("Вы присоединились к сессии.", "success")
    return redirect(url_for('main_bp.dashboard'))

@main_bp.route('/manage_session/<string:session_id>') # ИЗМЕНЕНО
@login_required
def manage_collaborators(session_id): # Переименовал, чтобы было понятнее
    current_session = Session.query.get_or_404(session_id)

    if current_session.owner_id != current_user.id:
        flash("У вас нет прав на управление этой сессией.", "danger")
        return redirect(url_for('main_bp.dashboard'))

    collaborators_roles = CollaborationRole.query.filter_by(session_id=session_id).all()
    
    # Получаем список всех пользователей для добавления
    all_users = User.query.all()
    # Отфильтровываем пользователей, которые уже являются коллабораторами
    existing_collaborator_ids = {cr.user_id for cr in collaborators_roles}
    available_users_to_add = [u for u in all_users if u.id not in existing_collaborator_ids]

    return render_template('manage_collaborators.html', 
                           session=current_session, 
                           collaborators_roles=collaborators_roles,
                           available_users_to_add=available_users_to_add)

@main_bp.route('/add_collaborator/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def add_collaborator(session_id):
    current_session = Session.query.get_or_404(session_id)

    if current_session.owner_id != current_user.id:
        flash("Только владелец сессии может добавлять коллабораторов.", "danger")
        return redirect(url_for('main_bp.dashboard'))
    
    user_id = request.form.get('user_id')
    role = request.form.get('role', 'viewer') # По умолчанию viewer

    if not user_id:
        flash("Пользователь не выбран.", "danger")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))
    
    user_id = int(user_id)
    if user_id == current_user.id:
        flash("Вы не можете добавить себя в качестве коллаборатора таким способом.", "warning")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

    existing_role = CollaborationRole.query.filter_by(session_id=session_id, user_id=user_id).first()
    if existing_role:
        flash("Этот пользователь уже является коллаборатором в данной сессии.", "warning")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

    new_collaboration = CollaborationRole(session_id=session_id, user_id=user_id, role=role)
    db.session.add(new_collaboration)
    db.session.commit()
    flash('Коллаборатор успешно добавлен.', 'success')
    return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

@main_bp.route('/update_collaborator_role/<string:session_id>/<int:user_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def update_collaborator_role(session_id, user_id):
    current_session = Session.query.get_or_404(session_id)

    if current_session.owner_id != current_user.id:
        flash("Только владелец сессии может изменять роли коллабораторов.", "danger")
        return redirect(url_for('main_bp.dashboard'))
    
    if user_id == current_user.id:
        flash("Вы не можете изменить свою собственную роль через это меню.", "warning")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

    new_role = request.form.get('new_role')
    if not new_role or new_role not in ['viewer', 'editor', 'owner']: # Владельца нельзя назначать через это меню, только менять свою роль
        flash("Недопустимая роль.", "danger")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

    collaboration_role = CollaborationRole.query.filter_by(session_id=session_id, user_id=user_id).first()
    if not collaboration_role:
        flash("Коллаборатор не найден.", "danger")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))
    
    collaboration_role.role = new_role
    db.session.commit()
    flash('Роль коллаборатора успешно обновлена.', 'success')
    return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

@main_bp.route('/remove_collaborator/<string:session_id>/<int:user_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def remove_collaborator(session_id, user_id):
    current_session = Session.query.get_or_404(session_id)

    if current_session.owner_id != current_user.id:
        flash("Только владелец сессии может удалять коллабораторов.", "danger")
        return redirect(url_for('main_bp.dashboard'))
    
    if user_id == current_user.id:
        flash("Вы не можете удалить себя из своей же сессии. Если хотите покинуть, удалите сессию.", "warning")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

    collaboration_role = CollaborationRole.query.filter_by(session_id=session_id, user_id=user_id).first()
    if not collaboration_role:
        flash("Коллаборатор не найден.", "danger")
        return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))
    
    db.session.delete(collaboration_role)
    db.session.commit()
    flash('Коллаборатор успешно удален.', 'success')
    return redirect(url_for('main_bp.manage_collaborators', session_id=session_id))

@main_bp.route('/delete_session/<string:session_id>', methods=['POST']) # ИЗМЕНЕНО
@login_required
def delete_session(session_id):
    session_to_delete = Session.query.get_or_404(session_id)

    if session_to_delete.owner_id != current_user.id:
        flash("У вас нет прав на удаление этой сессии.", "danger")
        return redirect(url_for('main_bp.dashboard'))

    try:
        db.session.delete(session_to_delete)
        db.session.commit()
        flash('Сессия успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении сессии: {e}", "danger")
        flash("Не удалось удалить сессию.", "danger")

    return redirect(url_for('main_bp.dashboard'))








