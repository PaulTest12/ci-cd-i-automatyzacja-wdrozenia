"""Automated tests for the demo web application."""

from app import app


def test_home_page_returns_application_information():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    body = response.get_json()
    assert body["app"] == "Platforma automatycznego wdrażania aplikacji internetowych"
    assert "/health" in body["endpoints"]


def test_health_endpoint_reports_ok():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "service": "web-deployment-platform",
    }


def test_items_endpoint_returns_sample_items():
    client = app.test_client()
    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json()[0]["name"] == "Demo item"


def test_unknown_route_returns_json_404():
    client = app.test_client()
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}
