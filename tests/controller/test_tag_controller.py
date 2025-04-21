from kairix_todo.models import Tag


def test_list_tags(client, db_session):
    """Test GET /tags endpoint returns all tags in the system."""
    # Create test tags
    tag1 = Tag(name="Work")
    tag2 = Tag(name="Personal")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    # Test the endpoint
    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert any(tag["name"] == "Work" for tag in data)
    assert any(tag["name"] == "Personal" for tag in data)


def test_create_tag(client, db_session):
    """Test POST /tags endpoint creates a new tag."""
    # Test the endpoint
    response = client.post("/tags/", json={"name": "New Tag"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New Tag"

    # Verify tag was created in the database
    tag = db_session.query(Tag).filter_by(name="New Tag").first()
    assert tag is not None
    assert tag.name == "New Tag"


def test_get_tag(client, db_session):
    """Test GET /tags/<tag_id> endpoint returns a specific tag."""
    # Create a test tag
    tag = Tag(name="Fetch Me")
    db_session.add(tag)
    db_session.commit()

    # Test the endpoint
    response = client.get(f"/tags/{tag.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fetch Me"
    assert data["id"] == tag.id


def test_get_nonexistent_tag(client):
    """Test GET /tags/<tag_id> with a non-existent tag ID returns 404."""
    response = client.get("/tags/nonexistent-id")
    assert response.status_code == 404


def test_update_tag(client, db_session):
    """Test PUT /tags/<tag_id> endpoint updates a tag."""
    # Create a test tag
    tag = Tag(name="Old Tag")
    db_session.add(tag)
    db_session.commit()

    # Test the endpoint
    response = client.put(f"/tags/{tag.id}", json={"name": "Updated Tag"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Tag"

    # Verify tag was updated in the database
    updated_tag = db_session.get(Tag, tag.id)
    assert updated_tag.name == "Updated Tag"


def test_update_nonexistent_tag(client):
    """Test PUT /tags/<tag_id> with a non-existent tag ID returns 404."""
    response = client.put("/tags/nonexistent-id", json={"name": "Updated Tag"})
    assert response.status_code == 404


def test_delete_tag(client, db_session):
    """Test DELETE /tags/<tag_id> endpoint deletes a tag."""
    # Create a test tag
    tag = Tag(name="Tag to Delete")
    db_session.add(tag)
    db_session.commit()

    # Test the endpoint
    response = client.delete(f"/tags/{tag.id}")
    assert response.status_code == 204

    # Verify tag was deleted from the database
    deleted_tag = db_session.get(Tag, tag.id)
    assert deleted_tag is None


def test_delete_nonexistent_tag(client):
    """Test DELETE /tags/<tag_id> with a non-existent tag ID returns 404."""
    response = client.delete("/tags/nonexistent-id")
    assert response.status_code == 404
