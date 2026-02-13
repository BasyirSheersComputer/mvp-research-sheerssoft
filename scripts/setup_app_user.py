import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.config import get_settings

async def setup_app_user():
    print("🚀 Setting up restricted 'app_user'...")
    
    # Use hardcoded superuser URL to fix user creation independent of current .env
    db_url = "postgresql+asyncpg://sheerssoft:sheerssoft_dev_password@localhost:5433/sheerssoft"
    engine = create_async_engine(db_url)
    
    async with engine.begin() as conn: # Use begin() for auto-commit transaction
        # Create user
        try:
            await conn.execute(text("CREATE USER app_user WITH PASSWORD 'app_password';"))
            print("   ✅ Created app_user.")
        except Exception as e:
            print(f"   ⚠️  app_user might already exist: {e}")
            
        # Grant permissions
        # Grant usage on schema
        await conn.execute(text("GRANT USAGE ON SCHEMA public TO app_user;"))
        # Grant all privileges on all tables (for MVP simplicity, but NOT superuser)
        await conn.execute(text("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;"))
        await conn.execute(text("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;"))
        
        # Ensure future tables also get privileges (optional but good practice)
        await conn.execute(text("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_user;"))
        
        print("   ✅ Granted privileges to app_user.")
        
        # Verify
        result = await conn.execute(text("SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = 'app_user'"))
        row = result.fetchone()
        print(f"   ℹ️  app_user: Super={row.rolsuper}, BypassRLS={row.rolbypassrls}")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(setup_app_user())
