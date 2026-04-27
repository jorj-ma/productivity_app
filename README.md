# Productivity application
This application allows users to track personal data.
It implements the following:
- Full authentication
- CRUD endpoints and pagination
- Secure access controls so users cannot view or edit each other’s data
- 
## Prerequisites
- Python 3.8+
- `pipenv`

## Install the required packages and activate the virtual environment:


```bash
pipenv install
```
```
pipenv shell
```
Note: If you encounter Python version mismatches, update your Pipfile to match your local Python version (e.g., 3.10 or 3.12).

## Database Initialization
Prepare the database schema using Flask-Migrate:

```bash
flask db init
```

```bash
flask db migrate -m "Initial migration
```

```bash
flask db upgrade
```

## Populating the Database
Run the seed script to create initial test data:

```bash
python seed.py
```

## Running the Application
The CLI client expects the backend API to be available at `http://localhost:5000`.
Start the development server:

```bash
flask run
```
or
```
python3 app.py
```

## Testing the endpoints
Based on the current CLI and tests, the API includes:
- `POST /signup` - signup user
-  `POST /login` - login user
-  `DELETE /logout` - delete an instance of user
-  `GET /me` - show my profile
-  `GET /notes` - list notes by page
-  `POST /notes` - add an instance of notes
-  `PATCH /notes/<int:note_id>` - update an instance of notes by id
-  `DELETE /notes/<int:note_id>` - delete an instance of notes by id

## Author
- Anzigale George

## Contributions
Contributions are welcome. Open an issue with  a clear description of the proposed improvements.

## License
The code is open for use.
