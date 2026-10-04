FROM python:3-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR app
COPY auth-webhook.py auth-webhook.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "auth-webhook:app"]
