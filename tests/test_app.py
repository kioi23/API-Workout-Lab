import pytest

from config import TestConfig
from server import create_app, db


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ---------- Exercises ----------

def test_create_exercise(client):
    resp = client.post("/exercises", json={"name": "Burpee", "category": "cardio"})
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "Burpee"


def test_create_exercise_missing_name(client):
    resp = client.post("/exercises", json={"category": "cardio"})
    assert resp.status_code == 400


def test_create_exercise_invalid_category(client):
    resp = client.post("/exercises", json={"name": "Test Move", "category": "not_real"})
    assert resp.status_code == 400


def test_duplicate_exercise_name_rejected(client):
    client.post("/exercises", json={"name": "Unique Move", "category": "strength"})
    resp = client.post("/exercises", json={"name": "Unique Move", "category": "strength"})
    assert resp.status_code == 400


def test_get_exercises(client):
    client.post("/exercises", json={"name": "Lunge", "category": "strength"})
    resp = client.get("/exercises")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_get_single_exercise_not_found(client):
    resp = client.get("/exercises/999")
    assert resp.status_code == 404


def test_delete_exercise(client):
    create_resp = client.post("/exercises", json={"name": "Sit Up", "category": "strength"})
    exercise_id = create_resp.get_json()["id"]

    delete_resp = client.delete(f"/exercises/{exercise_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/exercises/{exercise_id}")
    assert get_resp.status_code == 404


# ---------- Workouts ----------

def test_create_workout(client):
    resp = client.post("/workouts", json={"name": "Leg Day", "date": "2026-07-25"})
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "Leg Day"


def test_create_workout_missing_name(client):
    resp = client.post("/workouts", json={"date": "2026-07-25"})
    assert resp.status_code == 400


def test_get_workouts(client):
    client.post("/workouts", json={"name": "Push Day", "date": "2026-07-25"})
    resp = client.get("/workouts")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_get_single_workout_not_found(client):
    resp = client.get("/workouts/999")
    assert resp.status_code == 404


def test_delete_workout(client):
    create_resp = client.post("/workouts", json={"name": "Pull Day", "date": "2026-07-25"})
    workout_id = create_resp.get_json()["id"]

    delete_resp = client.delete(f"/workouts/{workout_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/workouts/{workout_id}")
    assert get_resp.status_code == 404


# ---------- Adding exercises to a workout ----------

def test_add_exercise_to_workout(client):
    workout_resp = client.post("/workouts", json={"name": "Full Body", "date": "2026-07-25"})
    workout_id = workout_resp.get_json()["id"]

    exercise_resp = client.post("/exercises", json={"name": "Deadlift", "category": "strength"})
    exercise_id = exercise_resp.get_json()["id"]

    resp = client.post(
        f"/workouts/{workout_id}/exercises",
        json={"exercise_id": exercise_id, "sets": 3, "reps": 8},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert len(data["workout_exercises"]) == 1
    assert data["workout_exercises"][0]["exercise"]["name"] == "Deadlift"
    assert data["workout_exercises"][0]["sets"] == 3


def test_add_exercise_invalid_sets_rejected(client):
    workout_resp = client.post("/workouts", json={"name": "Test Workout", "date": "2026-07-25"})
    workout_id = workout_resp.get_json()["id"]

    exercise_resp = client.post("/exercises", json={"name": "Curl", "category": "strength"})
    exercise_id = exercise_resp.get_json()["id"]

    resp = client.post(
        f"/workouts/{workout_id}/exercises",
        json={"exercise_id": exercise_id, "sets": -1},
    )
    assert resp.status_code == 400


def test_add_exercise_to_missing_workout(client):
    exercise_resp = client.post("/exercises", json={"name": "Row", "category": "strength"})
    exercise_id = exercise_resp.get_json()["id"]

    resp = client.post("/workouts/999/exercises", json={"exercise_id": exercise_id})
    assert resp.status_code == 404


def test_add_missing_exercise_to_workout(client):
    workout_resp = client.post("/workouts", json={"name": "Test Workout 2", "date": "2026-07-25"})
    workout_id = workout_resp.get_json()["id"]

    resp = client.post(f"/workouts/{workout_id}/exercises", json={"exercise_id": 999})
    assert resp.status_code == 404