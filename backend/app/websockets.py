import uuid
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, set_db_context
from app.services.conversation import process_guest_message

logger = structlog.get_logger()
router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, property_id: str, session_id: str):
    """
    WebSocket endpoint for Web Widget chat.
    URl: ws://domain/api/v1/ws/chat?property_id=...&session_id=...
    """
    await websocket.accept()
    
    # We can't use Depends(get_db) easily in generic WebSocket route without a bit of work 
    # or using the context manager manually inside the loop.
    # For simplicity/reliability in FastAPi WebSockets, manual session creation is often safer/clearer.
    from app.database import async_session
    
    logger.info("WEBSOCKET_CONNECT", session_id=session_id, property_id=property_id)
    
    try:
        pid = uuid.UUID(property_id)
        guest_identifier = f"web:{session_id}"
        
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Message from User
            user_text = payload.get("text")
            if not user_text:
                continue
                
            # Process with AI
            async with async_session() as db:
                await set_db_context(db, property_id)
                
                result = await process_guest_message(
                    db=db,
                    property_id=pid,
                    guest_identifier=guest_identifier,
                    channel="web",
                    message_text=user_text,
                    guest_name="Web Guest" # Could be passed in connection params
                )
                
                response_text = result["response"]
                
                # Send AI Reply
                await websocket.send_text(json.dumps({
                    "type": "message",
                    "text": response_text,
                    "sender": "ai"
                }))
                
    except WebSocketDisconnect:
        logger.info("WEBSOCKET_DISCONNECT", session_id=session_id)
    except Exception as e:
        logger.error("WEBSOCKET_ERROR", error=str(e), session_id=session_id)
        await websocket.close()
