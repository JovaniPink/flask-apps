FROM python:3.13

RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/FOLDER
RUN pip install /tmp/FOLDER
# CMD flask run server:app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
