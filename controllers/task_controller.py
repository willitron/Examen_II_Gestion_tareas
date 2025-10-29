from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.task import Task
from utils.auth import login_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.get_all_by_user(session['user_id'])
    return render_template('index.html', tasks=tasks)

@task_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.get_all_by_user(session['user_id'])
    return render_template('dashboard.html', tasks=tasks)

@task_bp.route('/task/create', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not title:
        flash('El título es obligatorio', 'danger')
        return redirect(url_for('task.dashboard'))
    
    Task.create(title, description, session['user_id'])
    flash('Tarea creada exitosamente', 'success')
    return redirect(url_for('task.dashboard'))

@task_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.get_by_id(task_id, session['user_id'])
    if task:
        Task.toggle_completed(task_id, session['user_id'])
        flash('Tarea actualizada', 'success')
    else:
        flash('Tarea no encontrada', 'danger')
    
    return redirect(url_for('task.dashboard'))

@task_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.get_by_id(task_id, session['user_id'])
    
    if not task:
        flash('Tarea no encontrada', 'danger')
        return redirect(url_for('task.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            flash('El título es obligatorio', 'danger')
            return render_template('edit_task.html', task=task)
        
        Task.update(task_id, title, description, session['user_id'])
        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('task.dashboard'))
    
    return render_template('edit_task.html', task=task)

@task_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.get_by_id(task_id, session['user_id'])
    if task:
        Task.delete(task_id, session['user_id'])
        flash('Tarea eliminada exitosamente', 'success')
    else:
        flash('Tarea no encontrada', 'danger')
    
    return redirect(url_for('task.dashboard'))