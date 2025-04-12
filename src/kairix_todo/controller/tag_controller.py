from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm import Session

from kairix_todo.models import Tag, TagSchema


class TagController:
    def __init__(self, session: Session):
        self.session = session
        self.blueprint = Blueprint("tags", __name__, url_prefix="/tags")
        self.tag_schema = TagSchema()
        self.tags_schema = TagSchema(many=True)

        # Route definitions
        self.blueprint.route("/", methods=["GET"])(self.list_tags)
        self.blueprint.route("/", methods=["POST"])(self.create_tag)
        self.blueprint.route("/<tag_id>", methods=["GET"])(self.get_tag)
        self.blueprint.route("/<tag_id>", methods=["PUT"])(self.update_tag)
        self.blueprint.route("/<tag_id>", methods=["DELETE"])(self.delete_tag)

    def list_tags(self):
        tags = self.session.query(Tag).all()
        return jsonify(self.tags_schema.dump(tags)), 200

    def create_tag(self):
        data = request.json
        tag = Tag(**data)
        self.session.add(tag)
        self.session.commit()
        return jsonify(self.tag_schema.dump(tag)), 201

    def get_tag(self, tag_id: str):
        tag = self.session.get(Tag, tag_id)
        if not tag:
            abort(404, description="Tag not found.")
        return jsonify(self.tag_schema.dump(tag)), 200

    def update_tag(self, tag_id: str):
        tag = self.session.get(Tag, tag_id)
        if not tag:
            abort(404, description="Tag not found.")

        data = request.json
        if data:  # Check if data is not empty
            for key, value in data.items():
                setattr(tag, key, value)

        self.session.commit()
        return jsonify(self.tag_schema.dump(tag)), 200

    def delete_tag(self, tag_id: str):
        tag = self.session.get(Tag, tag_id)
        if not tag:
            abort(404, description="Tag not found.")

        self.session.delete(tag)
        self.session.commit()
        return jsonify({"message": "Tag deleted"}), 204
