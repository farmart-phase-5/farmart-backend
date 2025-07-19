Farmart Backend – Farmer Dashboard (Flask API)
This backend powers the Farmer Dashboard of the Farmart platform. It allows farmers to manage their animal listings and view customer orders through a RESTful API built using Flask, SQLAlchemy, and PostgreSQL.

Features
View all customer orders

Accept or deny customer orders

Delete listed animals
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
1. Clone the Repository
bash
Copy
Edit
git clone git@github.com:farmart-phase-5/farmart-backend.git
cd farmart-backend
2. Set Up Virtual Environment
Make sure pipenv is installed:

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
3. Configure Environment Variables
Create a .env file in the project root and add the following:

env
Copy
Edit
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://localhost:5432/your_database_name
Replace your_database_name with your actual PostgreSQL database name.

Database Setup
Run the following commands to initialize and migrate the database:

bash
Copy
Edit
flask db init       # Run only once
flask db migrate
flask db upgrade
 Running the Application

Start the Flask server:

bash
Copy
Edit
flask run
Visit the API at: http://127.0.0.1:5000/

 Postman API Testing Guide
1. View All Orders
Method: GET

URL: http://127.0.0.1:5000/farmer/orders

Headers: None

Body: None

Response: Returns a list of customer orders

2. Accept or Deny an Order
Method: PATCH

URL: http://127.0.0.1:5000/farmer/orders/<order_id>

Headers:

Content-Type: application/json

Body:

json
Copy
Edit
{
  "status": "accepted"
}
Replace "accepted" with "denied" to reject the order. Replace <order_id> with the actual order ID.

3. Delete an Animal
Method: DELETE

URL: http://127.0.0.1:5000/farmer/animals/<animal_id>

Headers: None

Body: None

Replace <animal_id> with the ID of the animal to be deleted.


created  By
Joel Peace
Backend Developer – Farmer Dashboard Module
Phase 5, Moringa School

