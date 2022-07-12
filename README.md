## Task for Full Stack Developer @smartflowtech

## PROJECT DIRECTORY OUTLINE

The project is being modularized to two apps which are located inside the apps folder directory.

1. config folder: This folder contains the core system settings such as the settings.py, wsgi.py,celery.py and urls.py
2. apps folder: This folder contains each of the app on the system such:
    1. core app: This app handles the user registration and all related activities of a particular user
    2. finance app: This app handles the sales related functionalities of the system.

#

## HOW TO SETUP THE PROJECT

1. Clone the project to your local directory.
2. Create a virtualenv and install the project requirement that is locate inside requirement.txt using
   ```
    pip install -r requirements.txt
    ```

3. Copy the .env_sample into .env and set the following variable
   ```
    DB_USER=
    DB_PASSWORD=
    DB_NAME=
    DB_ENGINE='django.db.backends.mysql'
    SECRET_KEY=
    ```
4. Setup the database table by running the command below
    ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a super-admin by running
    ```
   python manage.py createsuperuser
   ```
6. run the project by running the command below
    ```
   python manage.py runserver
   ```

```
8. Viola!!! visit 127.0.0.1:8000 to access the swagger ui

---
