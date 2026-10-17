FROM python:3-alpine@sha256:5a02b6cf2cc372357e17ffde3f5f87afa4659a783d949d8320c005f506cf11e9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR app
COPY auth-webhook.py auth-webhook.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "auth-webhook:app"]
