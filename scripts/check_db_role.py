import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.config import get_settings

async def check_role():
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"))
        row = result.fetchone()
        print(f"User: {row.rolname}")
        print(f"Superuser: {row.rolsuper}")
        print(f"Bypass RLS: {row.rolbypassrls}")

if __name__ == "__main__":
    asyncio.run(check_role())
