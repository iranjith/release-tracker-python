from fastapi.testclient import TestClient

from release_tracker.main import app  # type: ignore[import-untyped]

client = TestClient(app)


def test_list_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_projects_by_name():
    response = client.get("/projects", params={"name": "Project A"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Project A"
