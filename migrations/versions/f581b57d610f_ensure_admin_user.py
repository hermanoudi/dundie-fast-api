"""ensure admin_user

Revision ID: f581b57d610f
Revises: 2515f7a66044
Create Date: 2023-06-23 20:36:40.679773

"""
from sqlite3 import IntegrityError
from alembic import op
import sqlalchemy as sa
import sqlmodel

from dundie.models.user import User
from sqlmodel import Session

# revision identifiers, used by Alembic.
revision = 'f581b57d610f'
down_revision = '2515f7a66044'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    admin = User(
        name="Admin",
        username="admin",
        email="admin@dm.com",
        dept="management",
        password="admin", # envvar/secret - colocar password em settings
        currency="USD"
    )

    try:
        session.add(admin)
        session.commit()
    except sa.exc.IntegrityError:
        session.rollback()


def downgrade() -> None:
    pass
