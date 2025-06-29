from flask_login import UserMixin
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

from ..extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owned_sessions = db.relationship(
        'Session',
        backref='owner',
        lazy=True,
        foreign_keys='Session.owner_id',
        cascade="all, delete-orphan"
    )
    collaboration_roles = db.relationship(
        'CollaborationRole',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )
    chat_messages = db.relationship(
        'ChatMessage',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)

class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    language = db.Column(db.String(50), nullable=False, default='python')
    is_private = db.Column(db.Boolean, nullable=False, default=True)
    editing_locked = db.Column(db.Boolean, nullable=False, default=False)
    output = db.Column(db.Text, nullable=True) # Для сохранения вывода выполнения кода
    timer_duration = db.Column(db.Integer, nullable=True) # Длительность таймера в секундах
    timer_start_time = db.Column(db.DateTime, nullable=True) # Время начала таймера


    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "owner_id": self.owner_id,
            "editing_locked": self.editing_locked,
            "is_private": self.is_private,
            "timer_start_time": self.timer_start_time.isoformat() if self.timer_start_time else None,
            "timer_duration": self.timer_duration,
            "language": self.language,
            "output": self.output
        }
    files = db.relationship('File', backref='session', lazy=True, cascade="all, delete-orphan")
    chat_messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade="all, delete-orphan")
    
    # Добавлено: Определение отношения с CollaborationRole
    collaboration_roles = db.relationship(
        'CollaborationRole', 
        backref='session', 
        lazy=True, 
        cascade="all, delete-orphan",
        foreign_keys='CollaborationRole.session_id' # Явно указываем foreign_keys
    )

    def __repr__(self):
        return f'<Session {self.title}>'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('session.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(50), nullable=False)
    is_main = db.Column(db.Boolean, default=False) # Флаг для обозначения основного файла
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('session_id', 'name', name='_session_name_uc'),)

    def to_dict(self):
        """Возвращает словарь, представляющий объект File."""
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'language': self.language,
            'is_main': self.is_main
        }

    def __repr__(self):
        return f'<File {self.name} in Session {self.session_id}>'

class CollaborationRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='viewer')
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('session_id', 'user_id', name='_session_user_uc'),)

    def __repr__(self):
        return f'<CollaborationRole User:{self.user_id} Session:{self.session_id} Role:{self.role}>'

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Unknown',
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

    def __repr__(self):
        return f'<ChatMessage Session:{self.session_id} User:{self.user_id} Time:{self.timestamp}>'