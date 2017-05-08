import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Boolean,Integer,String


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    instances  = Table('instances', meta, autoload=True)
    shadow_instances = Table('shadow_instances', meta, autoload=True)
 
    compute_nodes  = Table('compute_nodes', meta, autoload=True)
    shadow_compute_nodes = Table('shadow_compute_nodes', meta, autoload=True)


    sgx_enabled  = Column('sgx_enabled', Boolean, server_default=sqlalchemy.sql.expression.false(), nullable=False)
    sgx_memory_mb  = Column('sgx_memory_mb',Integer,server_default="0", nullable=False)
    sgx_memory_mb_used = Column('sgx_memory_mb_used',Integer,server_default="0", nullable=False)
    sgx_extra_params  = Column('sgx_extra_params',String(255),server_default="")
    sgx_migration_support  = Column('sgx_migration_support',Boolean, server_default=sqlalchemy.sql.expression.false(), nullable=False)
    
    instances.create_column(sgx_enabled)
    shadow_instances.create_column(sgx_enabled.copy())
    instances.create_column(sgx_memory_mb)
    shadow_instances.create_column(sgx_memory_mb.copy())
    instances.create_column(sgx_extra_params)
    shadow_instances.create_column(sgx_extra_params.copy())
    instances.create_column(sgx_migration_support)
    shadow_instances.create_column(sgx_migration_support.copy())
	
	
    compute_nodes.create_column(sgx_enabled.copy())
    shadow_compute_nodes.create_column(sgx_enabled.copy())
    compute_nodes.create_column(sgx_memory_mb.copy())
    shadow_compute_nodes.create_column(sgx_memory_mb.copy())
    compute_nodes.create_column(sgx_memory_mb_used)
    shadow_compute_nodes.create_column(sgx_memory_mb_used.copy())
    compute_nodes.create_column(sgx_migration_support.copy())
    shadow_compute_nodes.create_column(sgx_migration_support.copy())
