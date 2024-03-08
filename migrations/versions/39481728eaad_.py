"""empty message

Revision ID: 39481728eaad
Revises: 
Create Date: 2023-12-19 11:49:12.297191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39481728eaad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_id'), 'department', ['id'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=False)
    op.create_table('staff_position',
    sa.Column('pk_fk_dep', sa.Integer(), nullable=False),
    sa.Column('pk_fk_post', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pk_fk_dep'], ['department.id'], ),
    sa.ForeignKeyConstraint(['pk_fk_post'], ['post.id'], ),
    sa.PrimaryKeyConstraint('pk_fk_dep', 'pk_fk_post')
    )
    op.create_table('user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('fk_department_id', sa.Integer(), nullable=False),
    sa.Column('fk_post_id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_pregnant', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['fk_department_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['fk_post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_table('dep_kurators',
    sa.Column('fk_user_id', sa.Uuid(), nullable=False),
    sa.Column('fk_dep_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fk_dep_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['fk_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('fk_user_id', 'fk_dep_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dep_kurators')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('staff_position')
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_department_id'), table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###
