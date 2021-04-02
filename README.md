# Flask Apps

> A huge folder where I could store flask template applications.

## Overview

Currently I use Flask in multiple situations:

- Need a RESTful API for my Next.js app.
- Need a GraphQL API for my Gatsby.js app.
- Need to persistent data and have long running processes compute datasets.
- Need to create a server HTML app over basics forms.
- Need to create a Dash/Plot.ly dashboard for presenting some analysis.
- etc.

I've created a series folders as starters with my past Flask use.

## Features

Its not just Flask but an ecosystem to properly create a RESTful API service:

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) is a lightweight WSGI web application framework in Python. It is designed to make getting started very quickly and very easily.
- [Connexion](https://connexion.readthedocs.io/en/latest/index.html) is a framework on top of Flask that automatically handles HTTP requests defined using OpenAPI (formerly known as Swagger), supporting both v2.0 and v3.0 of the specification.
- [Graphene](https://github.com/graphql-python/graphene)
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/) is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) is a thin integration layer for Flask and marshmallow that adds additional features to marshmallow.
- [SQLAlchemy](https://www.sqlalchemy.org/library.html) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask.
- [Alembic](http://alembic.zzzcomputing.com/)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python.
- [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)
- [Celery](https://docs.celeryproject.org/en/latest/index.html) is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with focus on real-time processing, while also supporting task scheduling.

This project integrates other Flask libraries using:

- [Blueprints](https://flask.palletsprojects.com/en/1.0.x/blueprints/) for scalability.
- [flask_login](https://flask-login.readthedocs.io/en/latest/) for the login system (passwords hashed with bcrypt).
- [Flask-Script](https://flask-script.readthedocs.io/)
- [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)

## Links

- https://flask.palletsprojects.com/en/1.1.x/
- https://github.com/humiaozuzu/awesome-flask#readme

### Learn

- https://flask.palletsprojects.com/en/1.1.x/api/#api
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- https://blog.appseed.us/flask-how-to-code-simple-tasks/

## Server Architecture

YES!!!

## 🤝 Contributing

1. Fork this repository;
2. Create your branch: `git checkout -b my-new-feature`;
3. Commit your changes: `git commit -m 'Add some feature'`;
4. Push to the branch: `git push origin my-new-feature`.

**After your pull request is merged**, you can safely delete your branch.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for more information.
