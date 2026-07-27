from marshmallow import Schema, fields, validate

from server.models import ALLOWED_CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(
        required=True, validate=validate.OneOf(ALLOWED_CATEGORIES)
    )
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    date = fields.Date(required=True)
    notes = fields.Str(
        allow_none=True, validate=validate.Length(max=255), load_default=None
    )
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)