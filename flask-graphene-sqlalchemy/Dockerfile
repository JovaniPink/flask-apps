FROM python:3.9@sha256:da5aee29682d12a6649f51c8d6f15b87deb3e6c524b923c41d0cb3304d07c913

RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/FOLDER
RUN pip install /tmp/FOLDER
# CMD flask run server:app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
