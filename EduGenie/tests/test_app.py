from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_all_endpoints_work_in_demo_mode():
    cases = [
        ("/qa", "What is Python?"),
        ("/explain", "photosynthesis"),
        ("/quiz", "Photosynthesis is the process by which plants use light energy."),
        ("/summarize", "Photosynthesis converts light energy into chemical energy in plants."),
        ("/learn/recommendations", "SQL"),
    ]
    for endpoint, text in cases:
        response = client.post(endpoint, json={"text": text})
        assert response.status_code == 200, response.text
        assert response.json()


def test_empty_input_is_rejected():
    response = client.post("/qa", json={"text": "   "})
    assert response.status_code == 422
