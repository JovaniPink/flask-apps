FROM python:3-alpine@sha256:c6ead215bfd31f1e433d968853b7a769989117115b728874824e6c0a27cb96fc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR app
COPY auth-webhook.py auth-webhook.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "auth-webhook:app"]
