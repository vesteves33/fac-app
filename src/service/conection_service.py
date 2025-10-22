from typing import Any
from src.port.conection_port import ConectionPort

class ConectionService:
    def __init__(self, conection_port: ConectionPort):
        self.conection_port = conection_port

    async def authenticate(self) -> bool:
        return await self.conection_port.authenticate()
    
    async def client(self) -> Any:
        return await self.conection_port.client()