"""Description of changes

Revision ID: f5a661cb4824
Revises: fbf70bd6ded9
Create Date: 2025-01-25 04:07:03.589009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = 'f5a661cb4824'
down_revision: Union[str, None] = 'fbf70bd6ded9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role_permissions')
    op.drop_table('employees_salaries')
    op.drop_table('user_role_mapping')
    op.drop_table('user_roles')
    op.drop_table('calls_status')
    op.drop_table('client_meetings')
    op.drop_table('module_features')
    op.drop_table('employees_info')
    op.drop_table('company_info')
    op.drop_table('leads_info')
    op.drop_table('leads_stage')
    op.drop_table('modules')
    op.drop_table('client_calls')
    op.drop_table('meetings_status')
    op.drop_table('leads_types')
    op.drop_table('leads_status')
    op.alter_column('user_info', 'first_name',
               existing_type=sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('user_info', 'last_name',
               existing_type=sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('user_info', 'email',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('user_info', 'phone',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
    op.create_index(op.f('ix_user_info_id'), 'user_info', ['id'], unique=False)
    op.drop_constraint('FK_user_roles_company_info_company_domain_task', 'user_info', type_='foreignkey')
    op.drop_column('user_info', 'password_hash')
    op.drop_column('user_info', 'uid')
    op.drop_column('user_info', 'gender')
    op.drop_column('user_info', 'username')
    op.drop_column('user_info', 'date_added')
    op.drop_column('user_info', 'middle_name')
    op.drop_column('user_info', 'company_domain')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('middle_name', sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('username', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False))
    op.add_column('user_info', sa.Column('gender', sa.VARCHAR(length=10, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('uid', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('password_hash', sa.VARCHAR(length=200, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.create_foreign_key('FK_user_roles_company_info_company_domain_task', 'user_info', 'company_info', ['company_domain'], ['company_domain'])
    op.drop_index(op.f('ix_user_info_id'), table_name='user_info')
    op.alter_column('user_info', 'phone',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
    op.alter_column('user_info', 'email',
               existing_type=sa.String(),
               type_=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=False)
    op.alter_column('user_info', 'last_name',
               existing_type=sa.String(),
               type_=sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=False)
    op.alter_column('user_info', 'first_name',
               existing_type=sa.String(),
               type_=sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=False)
    op.create_table('leads_status',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lead_status', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__leads_sta__compa__4AB81AF0'),
    sa.PrimaryKeyConstraint('company_domain', 'id', name='PK__leads_st__E3441192FF20418B')
    )
    op.create_table('leads_types',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lead_type', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__leads_typ__compa__4E88ABD4'),
    sa.PrimaryKeyConstraint('company_domain', 'id', name='PK__leads_ty__E34411925046B740')
    )
    op.create_table('meetings_status',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('meeting_status', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__meetings___compa__52593CB8'),
    sa.PrimaryKeyConstraint('company_domain', 'id', name='PK__meetings__E3441192DC55DE76')
    )
    op.create_table('client_calls',
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('assigned_to', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('lead_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('call_date', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.Column('call_status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('call_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['assigned_to'], ['user_info.id'], name='FK__client_ca__assig__6B24EA82'),
    sa.ForeignKeyConstraint(['company_domain', 'call_status'], ['calls_status.company_domain', 'calls_status.id'], name='FK__client_calls__6C190EBB'),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__client_ca__compa__693CA210'),
    sa.ForeignKeyConstraint(['lead_id'], ['leads_info.lead_id'], name='FK__client_ca__lead___6A30C649'),
    sa.PrimaryKeyConstraint('call_id', name='PK__client_c__427DCE68F58FA3F9')
    )
    op.create_table('modules',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('display_name', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(length=2147483647, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('available', mssql.BIT(), autoincrement=False, nullable=True),
    sa.Column('comming_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('color', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('url', sa.TEXT(length=2147483647, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__modules__3213E83F05E4B041')
    )
    op.create_table('leads_stage',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lead_stage', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('is_assigned', mssql.BIT(), autoincrement=False, nullable=True),
    sa.Column('is_not_assigned', mssql.BIT(), autoincrement=False, nullable=True),
    sa.Column('is_action_taken', mssql.BIT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__leads_sta__compa__46E78A0C'),
    sa.PrimaryKeyConstraint('company_domain', 'id', name='PK__leads_st__E344119209CA1C7D')
    )
    op.create_table('leads_info',
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('lead_id', sa.BIGINT(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('lead_phone', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('name', sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('assigned_to', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=10, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('job_title', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('lead_stage', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lead_type', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lead_status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['assigned_to'], ['user_info.id'], name='FK__leads_inf__assig__5BE2A6F2'),
    sa.ForeignKeyConstraint(['company_domain', 'lead_stage'], ['leads_stage.company_domain', 'leads_stage.id'], name='FK__leads_info__5CD6CB2B'),
    sa.ForeignKeyConstraint(['company_domain', 'lead_status'], ['leads_status.company_domain', 'leads_status.id'], name='FK__leads_info__5EBF139D'),
    sa.ForeignKeyConstraint(['company_domain', 'lead_type'], ['leads_types.company_domain', 'leads_types.id'], name='FK__leads_info__5DCAEF64'),
    sa.PrimaryKeyConstraint('lead_id', name='PK__leads_in__B54D340BA8A68C89')
    )
    op.create_table('company_info',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('name', sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('field', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('address', sa.NVARCHAR(length=500, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('telephone_number', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('company_domain', name='PK__company___00652F113278E797')
    )
    op.create_table('employees_info',
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('employee_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('contact_name', sa.NVARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('business_phone', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('personal_phone', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('business_email', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('personal_email', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=10, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('is_company_admin', mssql.BIT(), autoincrement=False, nullable=True),
    sa.Column('user_uid', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__employees__compa__6FE99F9F'),
    sa.PrimaryKeyConstraint('company_domain', 'employee_id', name='PK__employee__9C37CFAB513CB547')
    )
    op.create_table('module_features',
    sa.Column('module_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('feature_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('display_name', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], name='FK_module_features_modules_module_id'),
    sa.PrimaryKeyConstraint('module_id', 'feature_id', name='PK_module_features_module_id_feature_id')
    )
    op.create_table('client_meetings',
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('assigned_to', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('lead_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('meeting_date', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.Column('meeting_status', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('meeting_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['assigned_to'], ['user_info.id'], name='FK__client_me__assig__6477ECF3'),
    sa.ForeignKeyConstraint(['company_domain', 'meeting_status'], ['meetings_status.company_domain', 'meetings_status.id'], name='FK__client_meetings__656C112C'),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__client_me__compa__628FA481'),
    sa.ForeignKeyConstraint(['lead_id'], ['leads_info.lead_id'], name='FK__client_me__lead___6383C8BA'),
    sa.PrimaryKeyConstraint('meeting_id', name='PK__client_m__C7B91CABA3CE192A')
    )
    op.create_table('calls_status',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('call_status', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK__calls_sta__compa__5629CD9C'),
    sa.PrimaryKeyConstraint('company_domain', 'id', name='PK__calls_st__E344119240C3E498')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('module_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], name='FK_user_roles_company_info_company_domain_task3'),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], name='FK_user_roles_modules_module_id'),
    sa.PrimaryKeyConstraint('id', name='PK__user_rol__3213E83F3E29888C')
    )
    op.create_table('user_role_mapping',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['user_roles.id'], name='FK_user_role_mapping_user_roles_role_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], name='FK_user_role_mapping_user_info_user_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id', name='PK_user_role_mapping_user_id_role_id')
    )
    op.create_table('employees_salaries',
    sa.Column('company_domain', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gross_salary', mssql.MONEY(), autoincrement=False, nullable=True),
    sa.Column('insurance', mssql.MONEY(), autoincrement=False, nullable=True),
    sa.Column('taxes', mssql.MONEY(), autoincrement=False, nullable=True),
    sa.Column('net_salary', mssql.MONEY(), autoincrement=False, nullable=True),
    sa.Column('due_year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('due_month', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(getdate())'), autoincrement=False, nullable=True),
    sa.Column('due_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_domain', 'employee_id'], ['employees_info.company_domain', 'employees_info.employee_id'], name='FK__employees_salari__73BA3083'),
    sa.PrimaryKeyConstraint('company_domain', 'employee_id', 'due_year', 'due_month', name='PK__employee__9C301A362769CE77')
    )
    op.create_table('user_role_permissions',
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('permission_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('module_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('feature_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('d_read', mssql.BIT(), server_default=sa.text('((0))'), autoincrement=False, nullable=True),
    sa.Column('d_write', mssql.BIT(), server_default=sa.text('((0))'), autoincrement=False, nullable=True),
    sa.Column('d_edit', mssql.BIT(), server_default=sa.text('((0))'), autoincrement=False, nullable=True),
    sa.Column('d_delete', mssql.BIT(), server_default=sa.text('((0))'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['module_id', 'feature_id'], ['module_features.module_id', 'module_features.feature_id'], name='FK_user_role_permissions_module_features_module_id_feature_id'),
    sa.ForeignKeyConstraint(['role_id'], ['user_roles.id'], name='FK_user_role_permissions_user_roles_role_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role_id', 'permission_id', name='PK_user_role_permissions_role_id_permissions_id')
    )
    # ### end Alembic commands ###
