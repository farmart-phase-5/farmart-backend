Farmart Backend – Farmer Dashboard (Flask API)
This backend handles the Farmer Dashboard functionality of the Farmart platform. It allows farmers to manage their animal listings and customer orders using a RESTful API built with Flask and SQLAlchemy.

Features Implemented
View all orders from users

Accept or deny an order

Delete animals from listing

Project Structure
arduino
Copy
Edit
farmart-backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   └── farmer_routes.py
│   └── config.py
├── migrations/
├── .env
├── Pipfile
└── run.py
Setup Instructions
1. Clone the repository
bash
Copy
Edit
git clone <your-repository-url>
cd farmart-backend
2. Set up virtual environment
Make sure you have pipenv installed:

bash
Copy
Edit
pip install pipenv
Then install dependencies and activate the environment:

bash
Copy
Edit
pipenv install
pipenv shell
3. Configure your environment
Create a .env file and include the following:

ini
Copy
Edit
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://localhost:5432/your_database_name
Update the DATABASE_URL with your actual PostgreSQL configuration.

4. Set up the database
bash
Copy
Edit
flask db init       # Only needed once
flask db migrate
flask db upgrade
Running the Application
bash
Copy
Edit
flask run
Visit the API at:
http://127.0.0.1:5000/

How to Test in Postman
Open Postman and follow the instructions below:

1. View Orders (GET)
Method: GET

URL: http://127.0.0.1:5000/farmer/orders

Headers: None required

Body: None

Expected Result: List of all orders made by customers

2. Accept or Deny an Order (PATCH)
Method: PATCH

URL: http://127.0.0.1:5000/farmer/orders/<order_id>

Headers: Content-Type: application/json

Body (raw JSON):

json
Copy
Edit
{
  "status": "accepted"
}
Replace "accepted" with "denied" to reject the order.
Replace <order_id> with the actual order ID.

3. Delete an Animal (DELETE)
Method: DELETE

URL: http://127.0.0.1:5000/farmer/animals/<animal_id>

Headers: None required

Body: None
Replace <animal_id> with the ID of the animal to be removed.

Notes
Ensure the database is seeded with test data or manually create entries before testing.

Authentication is not implemented in this version but can be added if needed.

Maintained By
Joel Peace
Backend Developer – Farmer Dashboard Module
Phase 5, Moringa School Project

