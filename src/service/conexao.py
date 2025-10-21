from typing import Any
from src.port.conexao import ConexaoPort

class ConexaoService:
    def __init__(self, conexao_port: ConexaoPort):
        self.conexao_port = conexao_port

    async def autenticar(self) -> bool:
        return await self.conexao_port.autenticar()
    
    async def client(self) -> Any:
        return await self.conexao_port.client()