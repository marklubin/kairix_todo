from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kairix_todo.models import Task, Tag, Reminder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' # Path to your database
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Welcome to Kairix Todo App!"

@app.route('/tasks', methods=['POST'])
def create_task(request):
    data = request.get_json()
    new_task = Task(title=data['title'], completed=data['completed'], due_date=data['due_date'], additional_details=data['additional_details'])
    db.session.add(new_task)
    db.session.commit()
    return "Task created", 201
