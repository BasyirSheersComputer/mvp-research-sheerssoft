"""
Vivatel KL — Seed Knowledge Base

This is the first pilot property's knowledge base, built from
Zul's interview data and public hotel information.

Run this script to create the Vivatel property and seed its KB.
Usage: python -m scripts.seed_vivatel
"""

import asyncio
import uuid

# Vivatel KL knowledge base documents
# Each will be embedded and stored in pgvector for RAG retrieval
VIVATEL_KB = [
    {
        "doc_type": "rooms",
        "title": "Room Types and Rates",
        "content": (
            "Vivatel KL offers the following room types:\n"
            "- Superior Room: RM 230/night, inclusive of breakfast for 2. "
            "23 sqm, king or twin bed, city view. Max 2 adults + 1 child.\n"
            "- Deluxe Room: RM 280/night, inclusive of breakfast for 2. "
            "28 sqm, king bed, higher floor with KL skyline view. Max 2 adults + 1 child.\n"
            "- Deluxe Suite: RM 350/night, inclusive of breakfast for 2. "
            "40 sqm, separate living area, king bed, panoramic city view. Max 2 adults + 2 children.\n"
            "- Family Room: RM 320/night, inclusive of breakfast for 4. "
            "35 sqm, 2 queen beds. Max 4 adults or 2 adults + 3 children.\n"
            "All rates are subject to 10% service charge and 8% government tax."
        ),
    },
    {
        "doc_type": "rooms",
        "title": "Room Amenities",
        "content": (
            "All rooms include: Free Wi-Fi, 43-inch smart TV, individually controlled AC, "
            "in-room safe, minibar (chargeable), coffee/tea making facilities, "
            "hairdryer, iron and ironing board, rainfall shower.\n"
            "Deluxe Suite additionally includes: Nespresso machine, bathrobe and slippers, "
            "separate bathtub, work desk area."
        ),
    },
    {
        "doc_type": "facilities",
        "title": "Hotel Facilities",
        "content": (
            "Vivatel KL facilities:\n"
            "- Swimming Pool: Rooftop infinity pool, open 7am-10pm daily\n"
            "- Gym/Fitness Centre: 24-hour access for all guests\n"
            "- Restaurant: 'Viv Café' — all-day dining, breakfast served 6:30am-10:30am\n"
            "- Meeting Rooms: 3 meeting rooms available for corporate events (capacity 10-50 pax). "
            "Half-day rate from RM 500, full-day from RM 800. Includes basic AV equipment.\n"
            "- Parking: Basement parking available at RM 10/day for hotel guests\n"
            "- Laundry: Same-day laundry and dry cleaning service available"
        ),
    },
    {
        "doc_type": "faqs",
        "title": "Check-in and Check-out Times",
        "content": (
            "Check-in time: 3:00 PM\n"
            "Check-out time: 12:00 PM (noon)\n"
            "Early check-in: Subject to availability, may be requested at front desk. "
            "Available from 12:00 PM at RM 50 surcharge.\n"
            "Late check-out: Subject to availability. Until 3:00 PM at 50% of room rate. "
            "Until 6:00 PM at full room rate.\n"
            "Express check-out: Available at front desk. Leave your key card and we'll "
            "email your final bill."
        ),
    },
    {
        "doc_type": "faqs",
        "title": "Frequently Asked Questions",
        "content": (
            "Q: Is breakfast included?\n"
            "A: Yes, breakfast is included in all room rates. Served daily at Viv Café, 6:30am-10:30am.\n\n"
            "Q: Is there airport transfer?\n"
            "A: Airport transfer can be arranged. KLIA/KLIA2 to hotel is RM 120 per car (up to 3 pax). "
            "Book at least 24 hours in advance.\n\n"
            "Q: Do you have a shuttle service?\n"
            "A: Complimentary shuttle to Pavilion KL and KLCC runs every hour from 9am-9pm.\n\n"
            "Q: What is the cancellation policy?\n"
            "A: Free cancellation up to 24 hours before check-in. "
            "Cancellations within 24 hours or no-shows are charged 1 night's room rate.\n\n"
            "Q: Can I request extra bed?\n"
            "A: Extra bed is available at RM 80/night, subject to room type and availability.\n\n"
            "Q: Is the hotel halal-certified?\n"
            "A: Viv Café serves halal-certified food. Our kitchen is JAKIM-certified halal."
        ),
    },
    {
        "doc_type": "directions",
        "title": "Location and Directions",
        "content": (
            "Vivatel KL is located at Jalan Sultan Ismail, Kuala Lumpur.\n\n"
            "From KLIA/KLIA2:\n"
            "- KLIA Ekspres to KL Sentral (28 min), then Grab/taxi (10 min, ~RM 15)\n"
            "- Direct Grab from KLIA: ~RM 80-100, approximately 50-60 minutes\n\n"
            "From KL Sentral:\n"
            "- Grab/taxi: 10 minutes, ~RM 10-15\n"
            "- Monorail: 2 stops to Bukit Bintang, then 5-minute walk\n\n"
            "Nearby landmarks:\n"
            "- Pavilion KL: 5-minute walk\n"
            "- KLCC/Petronas Towers: 10-minute drive or 15-minute walk\n"
            "- Bukit Bintang: 3-minute walk\n"
            "- Jalan Alor (food street): 7-minute walk\n\n"
            "GPS coordinates: 3.1480° N, 101.7137° E"
        ),
    },
    {
        "doc_type": "policies",
        "title": "Hotel Policies",
        "content": (
            "- Minimum age for check-in: 18 years old with valid ID\n"
            "- Children under 12 stay free in existing bedding\n"
            "- Pets are not allowed\n"
            "- Smoking is prohibited in all rooms. Designated smoking area on Level 3\n"
            "- Damage deposit: RM 200 cash or credit card pre-authorization at check-in\n"
            "- Valid ID (MyKad / Passport) required at check-in for all guests\n"
            "- The hotel reserves the right to refuse check-in without valid identification"
        ),
    },
    {
        "doc_type": "rates",
        "title": "Corporate and Group Rates",
        "content": (
            "Corporate rates (minimum 10 room nights/month contract):\n"
            "- Superior Room: RM 190/night (nett)\n"
            "- Deluxe Room: RM 230/night (nett)\n"
            "- Deluxe Suite: RM 300/night (nett)\n\n"
            "Group bookings (10+ rooms):\n"
            "- 10-19 rooms: 10% discount off published rates\n"
            "- 20-49 rooms: 15% discount off published rates\n"
            "- 50+ rooms: Contact our sales team for custom pricing\n\n"
            "For group bookings and corporate rate inquiries, "
            "please contact our reservations team for a detailed proposal."
        ),
    },
    {
        "doc_type": "facilities",
        "title": "Food and Beverage",
        "content": (
            "Viv Café (All-Day Dining):\n"
            "- Breakfast: 6:30am - 10:30am (included in room rate)\n"
            "- Lunch: 12:00pm - 2:30pm (à la carte, RM 25-45 per dish)\n"
            "- Dinner: 6:30pm - 10:30pm (à la carte, RM 30-55 per dish)\n"
            "- Cuisine: Malaysian favorites and international dishes\n"
            "- Room service: Available 24 hours (limited menu after 10:30pm)\n\n"
            "V-Bar (Lobby Lounge):\n"
            "- Opening hours: 5:00pm - 12:00am daily\n"
            "- Light bites, cocktails, mocktails, coffee\n"
            "- Happy hour: 5:00pm - 7:00pm (buy 1 free 1 on selected cocktails)"
        ),
    },
]


async def seed_vivatel():
    """Create the Vivatel property and seed its knowledge base."""
    from app.database import async_session, engine
    from app.models import Base, Property
    from app.services import ingest_knowledge_base
    from sqlalchemy import text

    # Ensure pgvector extension
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Check if Vivatel already exists
        from sqlalchemy import select
        result = await db.execute(
            select(Property).where(Property.name == "Vivatel KL")
        )
        existing = result.scalar_one_or_none()

        if existing:
            property_id = existing.id
            print(f"Vivatel KL already exists (ID: {property_id})")
        else:
            from decimal import Decimal
            prop = Property(
                name="Vivatel Kuala Lumpur",
                whatsapp_number="",  # Set after WhatsApp Business API setup
                website_url="https://vivatelhotels.com",
                notification_email="reservations@vivatel.com.my",
                operating_hours={
                    "start": "09:00",
                    "end": "18:00",
                    "timezone": "Asia/Kuala_Lumpur",
                },
                adr=Decimal("230.00"),
                ota_commission_pct=Decimal("20.00"),
            )
            db.add(prop)
            await db.flush()
            property_id = prop.id
            print(f"Created Vivatel KL (ID: {property_id})")

        # Ingest KB
        count = await ingest_knowledge_base(
            db=db,
            property_id=property_id,
            documents=VIVATEL_KB,
        )
        await db.commit()
        print(f"Ingested {count} KB documents for Vivatel KL")

    return property_id


if __name__ == "__main__":
    asyncio.run(seed_vivatel())
