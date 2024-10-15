"""empty message

Revision ID: 4dd3611b273e
Revises: 55928fddcb12
Create Date: 2024-10-12 02:36:10.736719

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4dd3611b273e"
down_revision = "55928fddcb12"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    # ### end Alembic commands ###
