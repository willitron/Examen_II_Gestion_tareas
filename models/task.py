from models.database import get_db

class Task:
    def __init__(self, id, title, description, completed, user_id, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id
        self.created_at = created_at
    
    @staticmethod
    def create(title, description, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)',
            (title, description, user_id)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id
    
    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            tasks.append(Task(
                row['id'], row['title'], row['description'],
                row['completed'], row['user_id'], row['created_at']
            ))
        return tasks
    
    @staticmethod
    def get_by_id(task_id, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, user_id)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Task(
                row['id'], row['title'], row['description'],
                row['completed'], row['user_id'], row['created_at']
            )
        return None
    
    @staticmethod
    def update(task_id, title, description, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET title = ?, description = ? WHERE id = ? AND user_id = ?',
            (title, description, task_id, user_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def toggle_completed(task_id, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET completed = NOT completed WHERE id = ? AND user_id = ?',
            (task_id, user_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(task_id, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, user_id)
        )
        conn.commit()
        conn.close()