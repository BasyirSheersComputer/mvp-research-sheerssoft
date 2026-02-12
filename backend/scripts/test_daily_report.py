"""
Script to manually trigger a daily report.
Usage: python -m scripts.test_daily_report
"""

import asyncio
import structlog
from datetime import date, timedelta
from app.services.scheduler import run_daily_reports

# Mock settings to avoid needing full SMTP setup if we just want to verify generation
# But integration test is better.
# For now, let's run the actual function.
# It will try to use SendGrid. If no key, it logs warning (as per email.py logic).

async def main():
    print("🚀 Triggering Daily Report Generation...")
    
    # Run for yesterday to ensure data exists (if any)
    # Be sure seed script or some data exists
    yesterday = date.today() - timedelta(days=1)
    
    try:
        await run_daily_reports(yesterday)
        print("✅ Daily report process completed successfully.")
        print("   (Check logs/console for email send status)")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
