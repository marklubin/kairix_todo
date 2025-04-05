from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from kairix_todo.controller.task_controller import TaskController
from kairix_todo.models import Base

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"  # Path to your database
db = SQLAlchemy(app)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app, model_class=Base)

with app.app_context():  # <-- add this block
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    task_controller = TaskController(Session())
    app.register_blueprint(task_controller.blueprint)
    db.create_all()

@app.route("/")
def health():
    return {"status": "running"}


@app.route("/web-app")
def web_app():
    return render_template("web_app.html")

if __name__ == "__main__":
    app.run(debug=True)
