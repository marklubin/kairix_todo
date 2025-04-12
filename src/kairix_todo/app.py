from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from kairix_todo.controller.tag_controller import TagController
from kairix_todo.controller.task_controller import TaskController
from kairix_todo.models import Base

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.url_map.strict_slashes = False  # Handle trailing slashes consistently

db = SQLAlchemy(app, model_class=Base)

with app.app_context():
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    session = Session()

    # Register both controllers
    task_controller = TaskController(session)
    tag_controller = TagController(session)

    app.register_blueprint(task_controller.blueprint)
    app.register_blueprint(tag_controller.blueprint)

    db.create_all()


@app.route("/")
def health() -> dict:
    return {"status": "running"}


@app.route("/web-app")
def web_app():
    return render_template("web_app.html")


if __name__ == "__main__":
    app.run(debug=True)
