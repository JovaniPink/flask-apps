"""Database models and Marshmallow 4 schemas."""

from datetime import datetime, timezone

from marshmallow import Schema, fields

from config import db, ma


def utc_now():
    """Return a timezone-naive UTC value for the existing SQLite columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Person(db.Model):
    __tablename__ = "person"

    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), nullable=False)
    fname = db.Column(db.String(32), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
    notes = db.relationship(
        "Note",
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)",
    )


class Note(db.Model):
    __tablename__ = "note"

    note_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(
        db.Integer,
        db.ForeignKey("person.person_id"),
        nullable=False,
    )
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


class PersonNoteSchema(Schema):
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.DateTime()


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session

    notes = fields.Nested(PersonNoteSchema, many=True, dump_default=list)


class NotePersonSchema(Schema):
    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.DateTime()


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        include_fk = True
        load_instance = True
        sqla_session = db.session

    person_id = fields.Int(dump_only=True)
    person = fields.Nested(NotePersonSchema, dump_default=None)
