# Flask + Graphene + SqlAlchemy GraphQL

A starter Python GraphQL Server using
[Flask](https://github.com/graphql-python/flask-graphql) and
[Graphene](https://github.com/graphql-python/graphene).

## Exact Stack

Python 3

Postgres

## Libraries

Flask (Web framework)

Graphene (GraphQL framework)

SqlAlchemy (Postgres ORM)

## Local Development

Running the server using Docker:

```bash
docker build -t python-flask-graphene .
docker run -p 5000:5000 python-flask-graphene
```

This will start a local server on `localhost:5000`. You can hit the graphql service at `localhost:5000/graphql` which opens GraphiQL.

## Deployment
