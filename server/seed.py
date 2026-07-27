from datetime import date

from server import create_app, db
from server.models import Exercise, Workout, WorkoutExercise

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    yoga_flow = Exercise(name="Yoga Flow", category="flexibility", equipment_needed=True)
    db.session.add_all([push_up, squat, plank, running, yoga_flow])
    db.session.commit()

    print("Seeding workouts...")
    morning_strength = Workout(
        name="Morning Strength", date=date(2026, 7, 20), notes="Full body strength session"
    )
    cardio_blast = Workout(
        name="Cardio Blast", date=date(2026, 7, 22), notes="High intensity cardio"
    )
    db.session.add_all([morning_strength, cardio_blast])
    db.session.commit()

    print("Linking exercises to workouts...")
    db.session.add_all(
        [
            WorkoutExercise(workout_id=morning_strength.id, exercise_id=push_up.id, sets=3, reps=12),
            WorkoutExercise(workout_id=morning_strength.id, exercise_id=squat.id, sets=4, reps=10),
            WorkoutExercise(workout_id=morning_strength.id, exercise_id=plank.id, duration_seconds=60),
            WorkoutExercise(workout_id=cardio_blast.id, exercise_id=running.id, duration_seconds=1800),
            WorkoutExercise(workout_id=cardio_blast.id, exercise_id=yoga_flow.id, duration_seconds=900),
        ]
    )
    db.session.commit()

    print("Done seeding!")