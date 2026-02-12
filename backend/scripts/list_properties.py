import asyncio
from sqlalchemy import select
from app.database import async_session
from app.models import Property

async def list_props():
    async with async_session() as db:
        result = await db.execute(select(Property))
        props = result.scalars().all()
        for p in props:
            print(f"{p.name}: {p.id}")

if __name__ == "__main__":
    asyncio.run(list_props())
