import asyncio
import os
import sys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models import Property
from app.schemas import PropertyResponse
from app.config import get_settings

async def debug_props():
    print("🚀 Debugging Properties...")
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    from app.database import set_db_context
    async with async_session() as db:
        # Set context to bypass RLS (if policy allows specific ID access) or just to see if it works
        # Vivatel ID
        pid = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
        try:
            await set_db_context(db, pid)
        except Exception as e:
            print(f"Failed to set context: {e}")

        result = await db.execute(select(Property))
        props = result.scalars().all()
        print(f"Found {len(props)} properties.")
        
        for p in props:
            print(f"Checking Property {p.id}:")
            print(f"  - Name: {p.name}")
            print(f"  - Whatsapp: {p.whatsapp_number}")
            print(f"  - Created At: {p.created_at}")
            
            try:
                model = PropertyResponse.model_validate(p)
                print("  ✅ Validation OK")
            except Exception as e:
                print(f"  ❌ Validation Failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_props())
