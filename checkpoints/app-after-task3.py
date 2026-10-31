# CHECKPOINT: app.py as it should look at the end of Task 3.
# Copy it over vulnerable-api/app.py only if you are stuck.
"""
Notes API -- internal microservice for the SCN lab.

WARNING: This service is INTENTIONALLY INSECURE for teaching purposes.
Do not deploy it anywhere reachable from an untrusted network.
"""
from flask import Flask, jsonify, request
from flasgger import Swagger

from data import NOTES

app = Flask(__name__)

Swagger(app, template={
    "info": {
        "title": "SCN Notes API",
        "description": (
            "Internal notes microservice.\n\n"
            "> **WARNING — deliberately insecure.** All endpoints below are "
            "unauthenticated in this start state. That is the lab exercise, not a mistake."
        ),
        "version": "0.3.0",
    },
    "host": "localhost:5000",
    "schemes": ["http"],
})

# TODO: move this out of source before go-live (ticket SCN-142)
API_KEY = "sk-live-3f9a2c7d8e1b4056a9c2f7e0d6b3a18c"

SERVICE_CONFIG = {
    "service": "notes-api",
    "environment": "production",
    "api_key": API_KEY,
    "db_host": "db.internal.scn.lab",
}

import jwt   # PyJWT, already installed in the container

# Hardcoded for now; Task 4 moves it to .env
JWT_SECRET = "dev-signing-secret-change-me"

def require_jwt(view):
    from functools import wraps
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify(error="missing bearer token"), 401
        token = auth.removeprefix("Bearer ").strip()
        try:
            jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"],
                options={"require": ["exp", "sub"]},
            )
        except jwt.ExpiredSignatureError:
            return jsonify(error="token expired"), 401
        except jwt.InvalidTokenError:
            return jsonify(error="invalid token"), 401
        return view(*args, **kwargs)
    return wrapper


@app.route("/health")
def health():
    """
    Liveness check.
    ---
    tags:
      - Info
    summary: Returns 200 if the service is running.
    responses:
      200:
        description: Service is alive.
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return jsonify(status="ok")


@app.route("/notes")
@require_jwt
def list_notes():
    """
    Retrieve all notes.
    ---
    tags:
      - Notes
    summary: Returns every note in the system.
    description: >
      Returns all stored notes for all users.
      **No authentication is required** in this start state — any caller
      receives every record. Fixing this is the goal of Tasks 2 and 3.
    responses:
      200:
        description: A list of all notes.
        schema:
          type: object
          properties:
            notes:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  owner:
                    type: string
                    example: a.shah
                  title:
                    type: string
                    example: Wi-Fi onboarding
                  body:
                    type: string
                    example: "Guest network PSK for the demo room is 'Welcome-2026!'."
    """
    # No authentication: any caller receives every note.
    return jsonify(notes=NOTES)


@app.route("/admin/keys")
@require_jwt
def admin_keys():
    """
    Service configuration and credentials.
    ---
    tags:
      - Admin
    summary: Returns service configuration including live credentials.
    description: >
      Returns the running service configuration.
      **No authentication is required** and the response includes the live
      API key — a textbook example of sensitive data exposure
      (OWASP API3:2023 Broken Object Property Level Authorization).
    responses:
      200:
        description: Service configuration including credentials.
        schema:
          type: object
          properties:
            service:
              type: string
              example: notes-api
            environment:
              type: string
              example: production
            api_key:
              type: string
              example: sk-live-3f9a2c7d8e1b4056a9c2f7e0d6b3a18c
              description: Live API key — should never appear in an API response.
            db_host:
              type: string
              example: db.internal.scn.lab
    """
    # No authentication: leaks the running service configuration.
    return jsonify(SERVICE_CONFIG)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
