🌌 Planetarium API

A REST API for online ticket booking at a planetarium.
You can browse shows, check the schedule, book seats, and view your reservations.

🚀 Stack

Python 3.11

Django 4.2

Django REST Framework

SQLite (easily switchable to PostgreSQL)

Docker

⚙️ How to run

Clone the repository

git clone https://github.com/your-username/planetarium-api.git
cd planetarium-api


Create a .env file (optional)

Start the project

docker-compose up --build


Open in browser:

http://127.0.0.1:8000/api/


Create a superuser (optional, for admin panel access):

docker-compose run app python manage.py createsuperuser

📌 Main Endpoints
| Method | URL                   | Description          |
| ------ | --------------------- | -------------------- |
| GET    | /api/shows/           | List of shows        |
| GET    | /api/sessions/        | List of sessions     |
| GET    | /api/reservations/my/ | My reservations      |
| POST   | /api/reservations/    | Create a reservation |

✨ Features

Seat availability validation

Poster upload support

Filters in the admin panel

View only your own reservations

🖼️ Screenshots & Database Structure

Screenshots and diagrams are available in the docs/ folder

🔮 Future improvements

JWT authentication

Payment integration

Email notifications for reservations

CI/CD pipeline setup

📌 The project was created as a portfolio to demonstrate work with Django REST Framework and Docker.