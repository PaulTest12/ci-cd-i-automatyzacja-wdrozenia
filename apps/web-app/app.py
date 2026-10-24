"""Minimal web application used to demonstrate automated deployments."""

from flask import Flask, jsonify

app = Flask(__name__)

ITEMS = [
    {"id": 1, "name": "Demo item"},
    {"id": 2, "name": "Second item"},
]


@app.get("/")
def index():
    """Return basic information about the demo application."""
    return jsonify(
        app="Platforma automatycznego wdrażania aplikacji internetowych",
        message="Aplikacja działa poprawnie.",
        endpoints=["/", "/health", "/items"],
    )


@app.get("/health")
def health():
    """Health-check endpoint used by deployment automation."""
    return jsonify(status="ok", service="web-deployment-platform"), 200


@app.get("/items")
def items():
    """Return sample data to demonstrate an application endpoint."""
    return jsonify(ITEMS), 200


@app.errorhandler(404)
def not_found(_error):
    """Return a small JSON error instead of the default HTML page."""
    return jsonify(error="Not found"), 404
