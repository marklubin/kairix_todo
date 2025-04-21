import json
import os

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint  # type: ignore[import]
from sqlalchemy.orm import scoped_session, sessionmaker

from kairix_todo.controller.search_controller import SearchController
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

    # Register controllers
    task_controller = TaskController(session)
    tag_controller = TagController(session)
    search_controller = SearchController(session)

    app.register_blueprint(task_controller.blueprint)
    app.register_blueprint(tag_controller.blueprint)
    app.register_blueprint(search_controller.blueprint)

    # Load OpenAPI schema
    openapi_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "openapi.json"
    )
    with open(openapi_path, "r") as f:
        openapi_spec = json.load(f)

    # Add endpoint to serve OpenAPI schema
    @app.route("/api/swagger.json")
    def swagger_json():
        return jsonify(openapi_spec)

    # Configure Swagger UI
    SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
    API_URL = "/api/swagger.json"  # Our API url

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Kairix Todo API"},  # Swagger UI config overrides
    )

    # Register blueprint at URL
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    db.create_all()


@app.route("/")
def index():
    return render_template("web_app.html")


@app.route("/health")
def health() -> dict:
    return {"status": "running"}


@app.route("/web-app")
def web_app():
    return render_template("web_app.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
