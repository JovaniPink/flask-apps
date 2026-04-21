FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY auth_webhook.py ./

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "auth_webhook:app"]
