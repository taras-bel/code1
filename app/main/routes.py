from flask import Blueprint, render_template, request, redirect, url_for, flash, session as flask_session
from flask_login import login_required, current_user
from .. import db
from ..models.models import Session # <--- ЭТА СТРОКА ВЫЗЫВАЕТ ПРОБЛЕМУ
import uuid
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

# Доступные языки и их настройки для CodeMirror
LANGUAGES = {
    'python': {'name': 'Python', 'mode': 'python'},
    'javascript': {'name': 'JavaScript', 'mode': 'javascript'},
    'java': {'name': 'Java', 'mode': 'clike'},
    'cpp': {'name': 'C++', 'mode': 'clike'},
    'text': {'name': 'Plain Text', 'mode': 'text/plain'}
}


@main.route('/')
def index():
    # Показываем только сессии, которыми владеет текущий пользователь,
    # если он аутентифицирован.
    user_sessions = []
    if current_user.is_authenticated:
        user_sessions = Session.query.filter_by(owner_id=current_user.id).all()
    return render_template('index.html', user_sessions=user_sessions)


@main.route('/create_session', methods=['POST'])
@login_required
def create_session():
    session_id = str(uuid.uuid4())
    default_code = "print('Hello, CodeShare!')" # Пример кода по умолчанию
    default_language = 'python'
    default_output = "" # Пустой вывод при создании

    # Время сессии - 60 минут по умолчанию
    timer_duration = 60 # Минут

    new_session = Session(
        id=session_id,
        owner_id=current_user.id,
        code=default_code,
        language=default_language,
        output=default_output,
        # timer_started_at остается None до запуска таймера
        timer_duration=timer_duration,
        editing_locked=False
    )
    db.session.add(new_session)
    db.session.commit()

    flash(f'Сессия "{session_id}" создана!', 'success')
    return redirect(url_for('main.editor', session_id=session_id))

@main.route('/editor/<session_id>')
@login_required
def editor(session_id):
    session_data = Session.query.get(session_id)

    if not session_data:
        flash('Сессия не найдена.', 'danger')
        return redirect(url_for('main.index'))

    # Проверяем, является ли текущий пользователь владельцем сессии,
    # или, если вы хотите разрешить всем присоединяться, просто убедитесь, что сессия существует.
    # Для целей этого проекта, мы пока что разрешим любому аутентифицированному пользователю присоединиться.
    # Если вы хотите строгую проверку владельца:
    # if session_data.owner_id != current_user.id:
    #     flash('У вас нет доступа к этой сессии.', 'danger')
    #     return redirect(url_for('main.index'))

    # Сохраняем ID сессии в сессии Flask, чтобы использовать его в SocketIO
    flask_session['session_id'] = session_id

    return render_template('editor.html', session=session_data, languages=LANGUAGES)