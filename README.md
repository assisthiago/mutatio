# MUTATIO

## Description
This is a system that helps to manage a swallowing team.

## Installation
To install this system, follow these steps:
1. Clone the repository.
2. Navigate to the project directory.
3. Run `python -m venv .venv` to create the virtual environment.
4. Run `.venv/bin/activate` to activate the virtual environment.
5. Run `pip install -r requirements.txt` to install the dependencies.
6. Run `python manage.py migrate` to create and migrate the database.
7. Run `python manage.py runserver` to run the server.
8. Run `python manage.py createsuperuser` and follow the instructions to create a admin user.
9. System runs on `http://localhost:8000/`. Go to [admin](http://localhost:8000/admin/) page.
10. Use the admin user to login.

## Tests
To run the tests, use the following command:
```
python manage.py test
```
```
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 1.349s

OK
Destroying test database for alias 'default'...
```

## API
### Django REST Framework
All endpoins are listing on `http://localhost:8000/api/` [[link]](http://localhost:8000/api/).

### Swagger
All snippets are listing on `http://localhost:8000/swagger/` [[link]](http://localhost:8000/swagger/).
