
import json
from app.core.redis import get_redis

HANDOFF_CHANNEL_PREFIX = "handoff"
DASHBOARD_CHANNEL = "dashboard:events"

class RealtimeService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if not self.redis:
            self.redis = await get_redis()
        return self.redis

    async def publish_handoff(self, property_id: str, conversation_id: str, guest_name: str, channel: str, summary: str):
        """
        Publish a handoff event to the dashboard channel.
        """
        redis = await self._get_redis()
        
        event = {
            "type": "handoff_alert",
            "property_id": str(property_id),
            "data": {
                "conversation_id": str(conversation_id),
                "guest_name": guest_name,
                "channel": channel,
                "summary": summary,
                "timestamp": None # You might want to add a timestamp here
            }
        }
        
        # Publish to a global dashboard channel (or property specific if needed)
        # For now, simplistic global channel that frontend subscribes to and filters
        await redis.publish(DASHBOARD_CHANNEL, json.dumps(event))
        
        # Also publish to specific property channel if we implement granular sub later
        # await redis.publish(f"{HANDOFF_CHANNEL_PREFIX}:{property_id}", json.dumps(event))

realtime_service = RealtimeService()
