FROM python:3-alpine@sha256:a0f2e268f2ce8f3709611a90054ec6a8ae31f6251f5896b8648b9bb99835e30a

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR app
COPY auth-webhook.py auth-webhook.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "auth-webhook:app"]
