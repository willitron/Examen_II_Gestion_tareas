from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para requerir autenticación en rutas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_registration(username, password):
    """Valida los datos de registro"""
    errors = []
    
    if not username or len(username) < 3:
        errors.append('El nombre de usuario debe tener al menos 3 caracteres')
    
    if not password or len(password) < 6:
        errors.append('La contraseña debe tener al menos 6 caracteres')
    
    return errors