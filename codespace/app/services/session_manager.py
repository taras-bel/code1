from app import db
from app.models.models import Session, File, CollaborationRole, User
import uuid
from datetime import datetime

class SessionManager:
    # Полный список всех языков программирования и их свойств
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
        'swift': {'name': 'Swift', 'mode': 'swift', 'file_extension': 'swift'},
        'kotlin': {'name': 'Kotlin', 'mode': 'kotlin', 'file_extension': 'kt'},
        'scala': {'name': 'Scala', 'mode': 'scala', 'file_extension': 'scala'},
        'r': {'name': 'R', 'mode': 'r', 'file_extension': 'r'},
        'dart': {'name': 'Dart', 'mode': 'dart', 'file_extension': 'dart'},
        'elixir': {'name': 'Elixir', 'mode': 'elixir', 'file_extension': 'ex'},
        'haskell': {'name': 'Haskell', 'mode': 'haskell', 'file_extension': 'hs'},
        'lua': {'name': 'Lua', 'mode': 'lua', 'file_extension': 'lua'},
        'perl': {'name': 'Perl', 'mode': 'perl', 'file_extension': 'pl'},
        'plaintext': {'name': 'Plain Text', 'mode': 'plaintext', 'file_extension': 'txt'}
    }

    @staticmethod
    def create_session(owner_id, title, description, is_private, initial_language):
        """Создание новой сессии с правильными параметрами"""
        try:
            # Убеждаемся, что initial_language является действительным или устанавливаем значение по умолчанию
            # Проверяем на None, пустую строку или отсутствие в LANGUAGES
            if not initial_language or initial_language not in SessionManager.LANGUAGES:
                initial_language = 'plaintext' # Резервное значение по умолчанию

            new_session = Session(
                id=str(uuid.uuid4()),
                owner_id=owner_id,
                title=title,
                description=description,
                is_private=is_private,
                language=initial_language, # Используем потенциально исправленный initial_language
                created_at=datetime.utcnow(),
                last_accessed=datetime.utcnow(),
                editing_locked=False
            )
            db.session.add(new_session)

            owner_role = CollaborationRole(
                session_id=new_session.id,
                user_id=owner_id,
                role='owner'
            )
            db.session.add(owner_role)

            initial_file = File(
                session_id=new_session.id,
                name=f'main.{SessionManager.get_file_extension(initial_language)}',
                content=SessionManager.get_default_code(initial_language),
                language=initial_language, # Используем потенциально исправленный initial_language
                is_main=True
            )
            db.session.add(initial_file)

            db.session.commit()
            return new_session.id
        except Exception as e:
            db.session.rollback()
            print(f"Error creating session: {e}")
            return None

    @staticmethod
    def get_session(session_id):
        return Session.query.get(session_id)

    @staticmethod
    def delete_session(session_id):
        session = Session.query.get(session_id)
        if session:
            try:
                File.query.filter_by(session_id=session_id).delete()
                CollaborationRole.query.filter_by(session_id=session_id).delete()
                db.session.delete(session)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error deleting session: {e}")
        return False

    @staticmethod
    def get_user_role_in_session(session_id, user_id):
        role = CollaborationRole.query.filter_by(
            session_id=session_id, 
            user_id=user_id
        ).first()
        return role.role if role else None

    @staticmethod
    def add_collaborator(session_id, user_id, role='viewer'):
        existing_role = CollaborationRole.query.filter_by(
            session_id=session_id,
            user_id=user_id
        ).first()
        
        if existing_role:
            if SessionManager._role_priority(role) > SessionManager._role_priority(existing_role.role):
                existing_role.role = role
                try:
                    db.session.commit()
                    return True
                except Exception as e:
                    db.session.rollback()
                    print(f"Error updating collaborator role: {e}")
            return False

        new_collaboration = CollaborationRole(
            session_id=session_id,
            user_id=user_id,
            role=role
        )
        db.session.add(new_collaboration)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding collaborator: {e}")
            return False

    @staticmethod
    def update_collaborator_role(session_id, user_id, new_role):
        role_entry = CollaborationRole.query.filter_by(
            session_id=session_id,
            user_id=user_id
        ).first()
        
        if role_entry:
            if role_entry.role == 'owner' and new_role != 'owner':
                return False
            
            role_entry.role = new_role
            try:
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error updating collaborator role: {e}")
        return False

    @staticmethod
    def remove_collaborator(session_id, user_id):
        role = CollaborationRole.query.filter_by(
            session_id=session_id,
            user_id=user_id
        ).first()
        
        if role and role.role != 'owner':
            try:
                db.session.delete(role)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error removing collaborator: {e}")
        return False

    @staticmethod
    def get_session_collaborators_with_users(session_id):
        return db.session.query(CollaborationRole, User).join(
            User, CollaborationRole.user_id == User.id
        ).filter(
            CollaborationRole.session_id == session_id
        ).all()

    @staticmethod
    def get_session_files(session_id):
        return File.query.filter_by(
            session_id=session_id
        ).order_by(File.name.asc()).all()

    @staticmethod
    def create_initial_file_for_session(session_id, language):
        # Убеждаемся, что language является действительным или устанавливаем значение по умолчанию
        # Проверяем на None, пустую строку или отсутствие в LANGUAGES
        if not language or language not in SessionManager.LANGUAGES:
            language = 'plaintext' # Резервное значение по умолчанию

        try:
            default_code = SessionManager.get_default_code(language)
            file_extension = SessionManager.get_file_extension(language)
            
            initial_file = File(
                session_id=session_id,
                name=f'main.{file_extension}',
                content=default_code,
                language=language, # Используем потенциально исправленный language
                is_main=True
            )
            db.session.add(initial_file)
            db.session.commit()
            return initial_file
        except Exception as e:
            db.session.rollback()
            print(f"Error creating initial file: {e}")
            return None

    @staticmethod
    def get_default_code(language):
        # Используем словарь LANGUAGES для всеобъемлющих значений по умолчанию
        if language in SessionManager.LANGUAGES:
            # Предоставляем конкретные значения по умолчанию для общих языков, иначе - общий комментарий
            defaults = {
                'python': "print('Hello, CodeShare from Python!')",
                'javascript': "console.log('Hello, CodeShare from JavaScript!');",
                'java': """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, CodeShare from Java!");
    }
}""",
                'c': "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, CodeShare from C!\\n\");\n    return 0;\n}",
                'cpp': """#include <iostream>

int main() {
    std::cout << "Hello, CodeShare from C++!" << std::endl;
    return 0;
}""",
                'csharp': """using System;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Hello, CodeShare from C#!");
    }
}""",
                'go': """package main

import "fmt"

func main() {
    fmt.Println("Hello, CodeShare from Go!")
}""",
                'rust': """fn main() {
    println!("Hello, CodeShare from Rust!");
}""",
                'ruby': "puts \"Hello, CodeShare from Ruby!\"",
                'php': "<?php\n\necho \"Hello, CodeShare from PHP!\";\n\n?>",
                'swift': "import Swift\n\nprint(\"Hello, CodeShare from Swift!\")",
                'kotlin': "fun main() {\n    println(\"Hello, CodeShare from Kotlin!\")\n}",
                'scala': "object Main extends App {\n  println(\"Hello, CodeShare from Scala!\")\n}",
                'r': "print(\"Hello, CodeShare from R!\")",
                'dart': "void main() {\n  print('Hello, CodeShare from Dart!');\n}",
                'elixir': "IO.puts \"Hello, CodeShare from Elixir!\"",
                'haskell': "main :: IO ()\nmain = putStrLn \"Hello, CodeShare from Haskell!\"",
                'lua': "print(\"Hello, CodeShare from Lua!\")",
                'perl': "print \"Hello, CodeShare from Perl!\\n\";",
                'typescript': "console.log(\"Hello, CodeShare from TypeScript!\");",
                'plaintext': "// Hello, CodeShare!"
            }
            return defaults.get(language, f"// Default code for {SessionManager.LANGUAGES[language]['name']}")
        return "// Hello, CodeShare!" # Резервное значение, если язык не в LANGUAGES (должно быть обработано create_session)


    @staticmethod
    def get_file_extension(language):
        # Используем словарь LANGUAGES для расширений
        return SessionManager.LANGUAGES.get(language, {}).get('file_extension', 'txt')

    @staticmethod
    def _role_priority(role):
        """Определение приоритета роли для сравнения"""
        role_priority = {
            'owner': 3,
            'editor': 2,
            'viewer': 1
        }
        return role_priority.get(role, 0)