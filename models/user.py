from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db
import sqlite3

class User:
    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
    
    @staticmethod
    def create(username, password):
        password_hash = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def get_by_username(username):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row['id'], row['username'], row['password_hash'], row['created_at'])
        return None
    
    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row['id'], row['username'], row['password_hash'], row['created_at'])
        return None
    
    def verify_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)