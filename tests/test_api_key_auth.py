import os
import pytest

def test_no_key_file_allows_requests(client):
    # No api_keys.txt in cwd: auth should be skipped and request allowed
    response = client.get("/tags/")
    assert response.status_code == 200

def test_api_key_enforced(monkeypatch, tmp_path, client):
    # Create a temporary key file and point environment at it
    key_file = tmp_path / "test_keys.txt"
    # Write one valid key
    key_file.write_text("goodkey\n")
    monkeypatch.setenv("API_KEYS_FILE", str(key_file))

    # Missing header -> 401 Unauthorized
    resp = client.get("/tags/")
    assert resp.status_code == 401

    # Invalid key -> 401 Unauthorized
    resp = client.get("/tags/", headers={"X-API-Key": "badkey"})
    assert resp.status_code == 401

    # Valid key -> 200 OK
    resp = client.get("/tags/", headers={"X-API-Key": "goodkey"})
    assert resp.status_code == 200