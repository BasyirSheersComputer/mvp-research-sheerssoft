"""enable_rls

Revision ID: enable_rls_001
Revises: 237140312085
Create Date: 2026-02-13 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'enable_rls_001'
down_revision = '2323898380cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Enable RLS on tables
    tables = ["properties", "conversations", "messages", "leads", "kb_documents", "analytics_daily"]
    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")

    # 2. Create Policy for 'properties'
    # Owners can only see their own property
    op.execute("""
        CREATE POLICY tenant_isolation_policy ON properties
        USING (id = current_setting('app.current_property_id', true)::uuid)
    """)

    # 3. Create Policy for tables with property_id
    # Rows must match the current_property_id
    for table in ["conversations", "leads", "kb_documents", "analytics_daily"]:
        op.execute(f"""
            CREATE POLICY tenant_isolation_policy ON {table}
            USING (property_id = current_setting('app.current_property_id', true)::uuid)
            WITH CHECK (property_id = current_setting('app.current_property_id', true)::uuid)
        """)

    # 4. Create Policy for messages (via conversation_id)
    # Relies on the fact that conversations are strictly filtered by RLS
    op.execute("""
        CREATE POLICY tenant_isolation_policy ON messages
        USING (conversation_id IN (SELECT id FROM conversations))
        WITH CHECK (conversation_id IN (SELECT id FROM conversations))
    """)
        
    # 5. Force RLS for superuser safety
    op.execute("ALTER TABLE properties FORCE ROW LEVEL SECURITY")
    # Note: We won't FORCE on others yet to allow some system-level queries if needed, 
    # but strictly speaking we should. For MVP, enabling is the critical step.


def downgrade() -> None:
    tables = ["properties", "conversations", "messages", "leads", "kb_documents", "analytics_daily"]
    for table in tables:
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
