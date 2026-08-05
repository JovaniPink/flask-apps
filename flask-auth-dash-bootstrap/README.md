# Dash on flask with flask_login
An example of a seamless integration of a Dash app into an existing Flask app based on the application factory pattern.

For details and how to use, please read: [How to embed a Dash app into an existing Flask app](https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b)

## Run locally

The example targets Python 3.14. Direct dependencies live in
`requirements.in`; `requirements.txt` is the reproducible compiled lock.

```sh
python -m pip install -r requirements.txt
export SECRET_KEY='replace-me'
gunicorn --bind 127.0.0.1:8000 dashapp:server
```

SQLite is used by default. Set `DATABASE_URL` to a PostgreSQL URL when needed.
Every runtime must provide a unique `SECRET_KEY`; startup fails when it is absent.

## Validate

```sh
docker build -t flask-auth-dash-bootstrap .
docker run --rm flask-auth-dash-bootstrap python -m pytest -q
```

## Deploy on Heroku (free)
First, edit the app.json and replace the value of the `repository`:
```
"repository": "https://github.com/okomarov/dash_on_flask"
```
with the URL to the forked repository.

Then click on the button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
