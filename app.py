
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task
import os
from datetime import datetime

app = Flask(__name__)
CORS(app) 

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()  # Create tables for the data models

# Root route
@app.route('/')
def home():
    return "Task Management API is running", 200

#to Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        new_task = Task(title=data['title'], description=data['description'], due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

#to Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date}
        output.append(task_data)
    return jsonify({'tasks': output}), 200

# to Retrieve a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date}
    return jsonify({'task': task_data}), 200

#to Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()  # Convert due_date to date object
        task.title = data['title']
        task.description = data['description']
        task.due_date = due_date
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

#to Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
