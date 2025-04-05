from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from kairix_todo.controller.task_controller import TaskController
from kairix_todo.models import Base


@pytest.fixture
def app(db_session: Session) -> Generator[Flask, None, None]:
    app = Flask(__name__)
    app.config["TESTING"] = True
    controller = TaskController(db_session)
    app.register_blueprint(controller.blueprint)

    yield app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:

    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()
