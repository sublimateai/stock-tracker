from pydantic import ValidationError
from steam.client.builtins.web import Web
from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect
from ...schemas.webserver import WebSocketClientCreate, CandleCreate
from ...database.models import Candle
from ...database import get_db_session

router = APIRouter()

class ConnectionManager():
    """
    Manages connections
    """
    def __init__(self):
        self.active_connections = {}

    async def attempt_connect(self, ws: WebSocket) -> WebSocketClientCreate | None:
        """
        Manage the validation of if the websocket is allowed to connect
        """
        initial_data: dict = await ws.receive_json()
        try:
            client_data: WebSocketClientCreate = WebSocketClientCreate(**initial_data)
            if self.active_connections.get(client_data.market_name):
                await ws.send_json({
                    "response" : False,
                    "detail" : "Client for this market already exists"
                })
                await ws.close()
                return None
            else:
                await ws.send_json({
                    "response" : True,
                    "detail" : "Connected successfully"
                })
                await ws.accept()
                self.active_connections[client_data.market_name] = ws
                return client_data
        except ValidationError:
            await ws.send_json({
                "response" : False,
                "detail" : "Invalid data"
            })
            await ws.close()
            return None

    async def disconnect_websocket(self, ws: WebSocket):
        for market_name, connection in self.active_connections.items():
            if ws == connection:
                del self.active_connections[market_name]
        

connection_manager = ConnectionManager() 

@router.websocket("/ws")
async def _get_websocket(ws: WebSocket):
    """
    Allow a client to connect with a WebSocket, they request initial market_name
    and if that market is not already an active connection, accept the socket
    else deny the socket.
    """
    ws_client_data = await connection_manager.attempt_connect(ws)
    if ws_client_data:
        try:
            while True:
                candle: dict = await ws.receive_json()
                try:
                    candle: Candle = Candle(**ws_client_data.model_dump(), **candle)
                    db= await get_db_session()
                    db.add(candle)
                    await db.commit()
                except ValidationError as e:
                    print(e)
        except WebSocketDisconnect:
            await connection_manager.disconnect_websocket(ws)



