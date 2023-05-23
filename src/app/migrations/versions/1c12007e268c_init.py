"""init

Revision ID: 1c12007e268c
Revises: 
Create Date: 2023-05-24 00:00:13.370661

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1c12007e268c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "investment_account",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_investment_account_id"), "investment_account", ["id"], unique=False)
    op.create_table(
        "operations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("cost", sa.Float(), nullable=False),
        sa.Column("investment_account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["investment_account_id"], ["investment_account.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_operations_id"), "operations", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_operations_id"), table_name="operations")
    op.drop_table("operations")
    op.drop_index(op.f("ix_investment_account_id"), table_name="investment_account")
    op.drop_table("investment_account")
    # ### end Alembic commands ###
