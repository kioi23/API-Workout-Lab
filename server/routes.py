from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server import db
from server.models import Exercise, Workout, WorkoutExercise
from server.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema

bp = Blueprint("api", __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# ---------- Workouts ----------

@bp.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@bp.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@bp.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json() or {}
    try:
        validated = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        workout = Workout(
            name=validated["name"],
            date=validated["date"],
            notes=validated.get("notes"),
        )
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(workout_schema.dump(workout)), 201


@bp.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204


# ---------- Exercises ----------

@bp.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@bp.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@bp.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json() or {}
    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        exercise = Exercise(
            name=validated["name"],
            category=validated["category"],
            equipment_needed=validated.get("equipment_needed", False),
        )
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@bp.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


# ---------- Add exercise to a workout ----------

@bp.route("/workouts/<int:id>/exercises", methods=["POST"])
def add_exercise_to_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json() or {}
    try:
        validated = workout_exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    exercise = db.session.get(Exercise, validated["exercise_id"])
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=validated.get("sets"),
            reps=validated.get("reps"),
            duration_seconds=validated.get("duration_seconds"),
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(workout_schema.dump(workout)), 201