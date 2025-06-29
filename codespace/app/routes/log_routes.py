import os
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

log_bp = Blueprint('log_bp', __name__)

@log_bp.route('/api/log_event', methods=['POST'])
def log_event():
    data = request.get_json()
    session_id = data.get('session_id')
    event_type = data.get('event_type')
    details = data.get('details', {})
    timestamp = datetime.utcnow().isoformat()

    if not session_id or not event_type:
        return jsonify({'error': 'session_id and event_type are required'}), 400

    # Определим путь к папке и создадим её при необходимости
    base_dir = os.path.join(current_app.root_path, '..', 'logs', session_id)
    os.makedirs(base_dir, exist_ok=True)
    log_file_path = os.path.join(base_dir, 'activity_log.md')

    # Запишем событие в Markdown-файл
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(f"### {timestamp} — {event_type}\n")
        for key, value in details.items():
            f.write(f"- **{key}**: {value}\n")
        f.write("\n")

    return jsonify({'status': 'logged'}), 200