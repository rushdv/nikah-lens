"""
API integration tests using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from database.seed.seed_data import run_seed

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    run_seed()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "adapters" in data


def test_profiles_list():
    response = client.get("/api/v1/profiles?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "deen" in data[0]


def test_profile_detail():
    list_res = client.get("/api/v1/profiles?limit=1")
    profile_id = list_res.json()[0]["id"]

    response = client.get(f"/api/v1/profiles/{profile_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == profile_id
    assert "education" in data
    assert "career" in data


def test_search_api_transparent_results():
    search_payload = {
        "criteria": {
            "gender": "male",
            "age": {"min": 22, "max": 29, "priority": "REQUIRED"},
            "height": {"min_cm": 165.1, "priority": "REQUIRED"},
            "locations": [{"name": "Rangpur", "priority": "PREFERRED"}],
            "marital_status": {"values": ["never_married"], "priority": "REQUIRED"},
            "deen": {"priority": "very_high", "require_salah": True},
            "career": {"priority": "high", "require_occupation_stated": True}
        }
    }
    response = client.post("/api/v1/search", json=search_payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "summary_counts" in data
    assert len(data["results"]) > 0

    first_res = data["results"][0]
    assert "match_status" in first_res
    assert "why_matched" in first_res
    assert "needs_review" in first_res


def test_search_profiles_crud():
    # 1. List
    list_res = client.get("/api/v1/search-profiles")
    assert list_res.status_code == 200
    initial_count = len(list_res.json())

    # 2. Create
    new_sp = {
        "name": "Test Search Profile",
        "description": "Created during automated test",
        "is_active": False,
        "criteria": {
            "gender": "male",
            "age": {"min": 24, "max": 28, "priority": "REQUIRED"},
            "height": {"min_cm": 165.1, "priority": "REQUIRED"},
            "locations": [{"name": "Rangpur", "priority": "REQUIRED"}],
            "marital_status": {"values": ["never_married"], "priority": "REQUIRED"},
            "deen": {"priority": "high", "require_salah": True},
            "career": {"priority": "medium", "require_occupation_stated": True}
        }
    }
    create_res = client.post("/api/v1/search-profiles", json=new_sp)
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # 3. Update
    patch_res = client.patch(f"/api/v1/search-profiles/{created_id}", json={"description": "Updated description"})
    assert patch_res.status_code == 200
    assert patch_res.json()["description"] == "Updated description"

    # 4. Delete
    del_res = client.delete(f"/api/v1/search-profiles/{created_id}")
    assert del_res.status_code == 200


def test_shortlist_and_private_notes():
    list_res = client.get("/api/v1/profiles?limit=1")
    profile_id = list_res.json()[0]["id"]

    # Add to shortlist
    sl_res = client.post("/api/v1/shortlists", json={"profile_id": profile_id, "stage": "Shortlisted", "notes": "Test candidate"})
    assert sl_res.status_code == 200
    assert sl_res.json()["stage"] == "Shortlisted"

    # Add private note
    note_res = client.post("/api/v1/notes", json={"profile_id": profile_id, "content": "Private note test: family verification pending"})
    assert note_res.status_code == 201
    note_id = note_res.json()["id"]

    # Get notes
    get_notes = client.get(f"/api/v1/profiles/{profile_id}/notes")
    assert get_notes.status_code == 200
    assert any(n["id"] == note_id for n in get_notes.json())


def test_sources_api():
    res = client.get("/api/v1/sources")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 4
    source_names = [s["name"] for s in data]
    assert "mock" in source_names
    assert "ahlia" in source_names
    assert "ordhekdeen" in source_names
    assert "idealnikah" in source_names
