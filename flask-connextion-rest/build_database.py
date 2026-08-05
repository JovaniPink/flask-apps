"""Create and seed the development SQLite database."""

from datetime import datetime

from config import db
from models import Note, Person
from server import app

PEOPLE = [
    {
        "fname": "Doug",
        "lname": "Farrell",
        "notes": [
            ("Cool, a mini-blogging application!", "2019-01-06 22:17:54"),
            ("This could be useful", "2019-01-08 22:17:54"),
            ("Well, sort of useful", "2019-03-06 22:17:54"),
        ],
    },
    {
        "fname": "Kent",
        "lname": "Brockman",
        "notes": [
            (
                "I'm going to make really profound observations",
                "2019-01-07 22:17:54",
            ),
            (
                "Maybe they'll be more obvious than I thought",
                "2019-02-06 22:17:54",
            ),
        ],
    },
    {
        "fname": "Bunny",
        "lname": "Easter",
        "notes": [
            ("Has anyone seen my Easter eggs?", "2019-01-07 22:47:54"),
            ("I'm really late delivering these!", "2019-04-06 22:17:54"),
        ],
    },
]


def rebuild_database():
    """Reset the configured database and load the example records."""
    with app.app_context():
        db.drop_all()
        db.create_all()

        for person_data in PEOPLE:
            person = Person(
                lname=person_data["lname"],
                fname=person_data["fname"],
            )
            for content, timestamp in person_data["notes"]:
                person.notes.append(
                    Note(
                        content=content,
                        timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                    )
                )
            db.session.add(person)

        db.session.commit()


if __name__ == "__main__":
    rebuild_database()
