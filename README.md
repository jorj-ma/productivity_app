# Productivity application setup guide
## 1.Install the required packages and activate the virtual environment:


`pipenv install`
`pipenv shell`
Note: If you encounter Python version mismatches, update your Pipfile to match your local Python version (e.g., 3.10 or 3.12).

## 2.Database Initialization
Prepare the database schema using Flask-Migrate:

`flask db init`

`flask db migrate -m "Initial migration`

`flask db upgrade`

## 3.Populating the Database
Run the seed script to create initial test data:

`python seed.py`

## 4.Running the Application
Start the development server:

`flask run`
