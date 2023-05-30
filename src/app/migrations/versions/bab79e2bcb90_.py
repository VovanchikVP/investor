"""empty message

Revision ID: bab79e2bcb90
Revises: 3463057ac0c1
Create Date: 2023-05-30 19:57:12.231226

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bab79e2bcb90"
down_revision = "3463057ac0c1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("assets", "code", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint("assets_code_key", "assets", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("assets_code_key", "assets", ["code"])
    op.alter_column("assets", "code", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###
