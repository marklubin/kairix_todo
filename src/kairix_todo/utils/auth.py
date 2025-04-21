import os
from flask import request, abort

def check_api_key():
    """
    Before-request handler to enforce API key authentication.

    If a key file exists at the path given by the API_KEYS_FILE environment
    variable (default "api_keys.txt"), only requests with a valid
    X-API-Key header matching one of the keys in that file are allowed.
    If the file does not exist, authentication is skipped (all requests allowed).
    """
    api_keys_file = os.getenv("API_KEYS_FILE", "api_keys.txt")
    try:
        with open(api_keys_file) as f:
            valid_keys = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        # No key file: skip authentication
        return

    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key not in valid_keys:
        abort(401, description="Unauthorized: invalid or missing API key")