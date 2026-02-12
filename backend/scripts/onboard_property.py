"""
Script to onboard a new property from a JSON configuration file.
Usage: python -m scripts.onboard_property --file propery_conf.json
"""

import argparse
import asyncio
import json
import sys
from decimal import Decimal
import structlog

from app.database import async_session
from app.models import Property
from app.services import ingest_knowledge_base
from sqlalchemy import select

logger = structlog.get_logger()

async def onboard_property(json_file: str):
    logger.info("Starting property onboarding", file=json_file)
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read JSON file: {e}")
        return

    # Extract fields
    name = data.get("name")
    if not name:
        logger.error("Property name is required")
        return

    async with async_session() as db:
        # Check if property exists
        result = await db.execute(select(Property).where(Property.name == name))
        existing = result.scalar_one_or_none()
        
        if existing:
            prop = existing
            logger.info("Updating existing property", property_id=str(prop.id))
        else:
            prop = Property()
            logger.info("Creating new property", name=name)

        # Update fields
        prop.name = name
        prop.whatsapp_number = data.get("whatsapp_number")
        prop.notification_email = data.get("notification_email")
        prop.website_url = data.get("website_url")
        prop.operating_hours = data.get("operating_hours")
        
        if "adr" in data:
            prop.adr = Decimal(str(data["adr"]))
        if "ota_commission_pct" in data:
            prop.ota_commission_pct = Decimal(str(data["ota_commission_pct"]))
            
        if not existing:
            db.add(prop)
        
        await db.flush()
        property_id = prop.id
        
        # Ingest KB if provided
        kb_docs = data.get("kb_documents", [])
        if kb_docs:
            logger.info("Ingesting KB documents", count=len(kb_docs))
            count = await ingest_knowledge_base(
                db=db,
                property_id=property_id,
                documents=kb_docs
            )
            logger.info("KB ingestion complete", documents_ingested=count)
            
        await db.commit()
        logger.info("Property onboarding complete", property_id=str(property_id))
        print(f"SUCCESS: Property '{name}' onboarded with ID: {property_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Onboard a property from JSON")
    parser.add_argument("--file", required=True, help="Path to JSON configuration file")
    args = parser.parse_args()
    
    asyncio.run(onboard_property(args.file))
