# Workout Tracker API

## Project Description

Workout Tracker API is a RESTful backend application built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

The API allows personal trainers to:

- Create workouts
- View workouts
- Delete workouts
- Create exercises
- View exercises
- Delete exercises
- Add exercises to workouts
- Store workout details such as sets, reps, and duration

The application demonstrates relational database design using a many-to-many relationship through a join table.

---

## Technologies Used

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Marshmallow
- SQLite
- Pipenv

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/workout-tracker-api.git
```

Move into the project

```bash
cd workout-tracker-api
```

Install dependencies

```bash
pipenv install
```

Activate the virtual environment

```bash
pipenv shell
```

---

## Database Setup

Initialize migrations

```bash
flask db init
```

Create migration

```bash
flask db migrate -m "Initial migration"
```

Apply migration

```bash
flask db upgrade
```

Seed the database

```bash
python server/seed.py
```

---

## Running the Application

```bash
python server/app.py
```

The API runs on

```
http://localhost:5555
```

---

## API Endpoints

### Workouts

GET /workouts

Returns all workouts.

GET /workouts/<id>

Returns a single workout.

POST /workouts

Creates a workout.

DELETE /workouts/<id>

Deletes a workout.

---

### Exercises

GET /exercises

Returns all exercises.

GET /exercises/<id>

Returns one exercise.

POST /exercises

Creates an exercise.

DELETE /exercises/<id>

Deletes an exercise.

---

### WorkoutExercises

POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Adds an exercise to a workout.

---

## Database Tables

Exercise

- id
- name
- category
- equipment_needed

Workout

- id
- date
- duration_minutes
- notes

WorkoutExercise

- id
- workout_id
- exercise_id
- reps
- sets
- duration_seconds

---

## Author

Your Name

Software Engineering Student