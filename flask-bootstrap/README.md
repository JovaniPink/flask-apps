# FlaskApp starter app

![Screenshot](https://github.com/twintechlabs/flaskapp/blob/master/app/static/images/screenshot.png)

This code base serves as starting point for writing your next Flask application.

It's based on the awesome work of the Ling Thio and includes the open source
BootStrap ThemesGuide theme and a number of enhancements to the base Flask
Starter app including adding basic user management and a separate view file for
API code. This template is designed as a way to quickly get started building a
wide variety of applications based on Python and Flask.

## Code characteristics

* Runs on Python 3.14 and Flask 3.1
* Uses Flask-Security-Too for authentication and role management
* Well organized directories with lots of comments
    * app
        * commands
        * models
        * static
        * templates
        * views
    * tests
* Includes a pytest test suite
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions

## Setting up a development environment

You need Python 3.14 and a virtual environment tool, or Docker.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/twintechlabs/flaskdash.git my_app

    # Create a virtual environment and install the locked dependencies
    cd ~/dev/my_app
    python3.14 -m venv .venv
    . .venv/bin/activate
    python -m pip install -r requirements.txt

Set unique secrets before starting the app. Do not reuse the example values in
production:

    export SECRET_KEY="replace-with-a-long-random-value"
    export SECURITY_PASSWORD_SALT="replace-with-another-random-value"


## Configuring SMTP

Set `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, and
`MAIL_PASSWORD` in the environment. Flask-Security-Too uses these settings for
confirmation and password-recovery messages. The development and test
configurations suppress delivery by default.


## Initializing the Database

    # Create DB tables and populate the roles and users tables
    flask --app wsgi:app db upgrade
    flask --app manage:app init-db


## Running the app (development)

    # Start the Flask development web server
    flask --app wsgi:app run --debug

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `member@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.

## Running the app (production)

Gunicorn is included in the locked dependencies:

    gunicorn wsgi:app

Or use the container image:

    docker build -t flask-bootstrap .
    docker run --rm -p 8000:8000 \
      -e SECRET_KEY="replace-with-a-long-random-value" \
      -e SECURITY_PASSWORD_SALT="replace-with-another-random-value" \
      flask-bootstrap

## Running the automated tests

    python -m pytest -q


## Trouble shooting

Use Flask-Migrate for schema changes. Do not delete a database that contains
data; apply and verify a migration instead.


## Acknowledgements

With thanks to the following Flask extensions:
* [ThemesGuide](https://github.com/ThemesGuide/bootstrap-themes)
* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Security-Too](https://flask-security-too.readthedocs.io/)

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.

## Authors
- Matt Hogan - matt AT twintechlabs DOT io
- Ling Thio -- ling.thio AT gmail DOT com
