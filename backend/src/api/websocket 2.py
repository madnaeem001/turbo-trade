from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import logging
from typing import Set

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manage WebSocket connections and broadcast"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Active: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Active: {len(self.active_connections)}")
    
    async def broadcast(self, data: dict):
        """Broadcast data to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Broadcast error: {str(e)}")
                self.disconnect(connection)
    
    async def broadcast_metrics(self, metrics: dict):
        """Broadcast real-time metrics"""
        await self.broadcast({
            "type": "metrics",
            "data": metrics
        })
    
    async def broadcast_trade(self, trade: dict):
        """Broadcast executed trade"""
        await self.broadcast({
            "type": "trade",
            "data": trade
        })

# Global manager
ws_manager = WebSocketManager()

async def websocket_handler(websocket: WebSocket, engine=None):
    """
    WebSocket handler for real-time data streaming.
    
    Args:
        websocket: WebSocket connection
        engine: ExecutionEngine instance
    """
    await ws_manager.connect(websocket)
    
    try:
        while True:
            # Send metrics every 100ms
            await asyncio.sleep(0.1)
            
            if engine:
                metrics = engine.get_live_metrics()
                await ws_manager.broadcast_metrics(metrics)
            
            # Check for incoming messages
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                # Handle incoming messages if needed
            except asyncio.TimeoutError:
                pass
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        ws_manager.disconnect(websocket)
