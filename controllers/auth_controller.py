from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from utils.auth import validate_registration

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('task.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        errors = validate_registration(username, password)
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        user_id = User.create(username, password)
        if user_id:
            flash('Registro exitoso. Por favor, inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('El nombre de usuario ya existe', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('task.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.get_by_username(username)
        
        if user and user.verify_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(url_for('task.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))