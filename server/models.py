from datetime import date as date_cls

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from server import db

ALLOWED_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", name="uq_exercise_name"),
        CheckConstraint("length(name) > 0", name="ck_exercise_name_not_empty"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )

    # -- model validations --
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or value.lower() not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {ALLOWED_CATEGORIES}")
        return value.lower()

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date_cls.today)
    notes = db.Column(db.String(255))

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_workout_name_not_empty"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise", secondary="workout_exercises", viewonly=True
    )

    # -- model validations --
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty")
        return value.strip()

    def __repr__(self):
        return f"<Workout {self.id} {self.name}>"


class WorkoutExercise(db.Model):
    """Association object joining Workout <-> Exercise, carrying set/rep/duration data."""

    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint("sets IS NULL OR sets > 0", name="ck_sets_positive"),
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_reps_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_duration_positive",
        ),
    )

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # -- model validations --
    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("sets must be a positive integer")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("reps must be a positive integer")
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_seconds must be a positive integer")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>"