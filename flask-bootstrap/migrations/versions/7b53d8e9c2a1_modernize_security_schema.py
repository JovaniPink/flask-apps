"""Modernize the authentication schema without discarding existing users.

Revision ID: 7b53d8e9c2a1
Revises: 0001c8ac1a69
"""

import uuid

from alembic import op
import sqlalchemy as sa

revision = "7b53d8e9c2a1"
down_revision = "0001c8ac1a69"
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("role", "roles")
    op.rename_table("user", "users")
    op.rename_table("user_roles", "users_roles")

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("username", existing_type=sa.String(50), nullable=True)
        batch_op.alter_column(
            "reset_password_token", existing_type=sa.String(100), nullable=True
        )
        batch_op.alter_column(
            "email_confirmed_at",
            existing_type=sa.DateTime(),
            new_column_name="confirmed_at",
        )
        batch_op.alter_column(
            "is_active",
            existing_type=sa.Boolean(),
            new_column_name="active",
            existing_server_default="0",
        )
        batch_op.add_column(sa.Column("fs_uniquifier", sa.String(64), nullable=True))

    users = sa.table(
        "users",
        sa.column("id", sa.Integer()),
        sa.column("fs_uniquifier", sa.String(64)),
    )
    connection = op.get_bind()
    for user_id in connection.execute(sa.select(users.c.id)).scalars():
        connection.execute(
            users.update()
            .where(users.c.id == user_id)
            .values(fs_uniquifier=uuid.uuid4().hex)
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "fs_uniquifier", existing_type=sa.String(64), nullable=False
        )
        batch_op.create_unique_constraint(
            "uq_users_fs_uniquifier", ["fs_uniquifier"]
        )


def downgrade():
    users = sa.table(
        "users",
        sa.column("email", sa.String(255)),
        sa.column("username", sa.String(50)),
        sa.column("reset_password_token", sa.String(100)),
    )
    connection = op.get_bind()
    connection.execute(
        users.update().where(users.c.username.is_(None)).values(username=users.c.email)
    )
    connection.execute(
        users.update()
        .where(users.c.reset_password_token.is_(None))
        .values(reset_password_token="")
    )

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_fs_uniquifier", type_="unique")
        batch_op.drop_column("fs_uniquifier")
        batch_op.alter_column(
            "active",
            existing_type=sa.Boolean(),
            new_column_name="is_active",
            existing_server_default="0",
        )
        batch_op.alter_column(
            "confirmed_at",
            existing_type=sa.DateTime(),
            new_column_name="email_confirmed_at",
        )
        batch_op.alter_column(
            "reset_password_token", existing_type=sa.String(100), nullable=False
        )
        batch_op.alter_column("username", existing_type=sa.String(50), nullable=False)

    op.rename_table("users_roles", "user_roles")
    op.rename_table("users", "user")
    op.rename_table("roles", "role")
