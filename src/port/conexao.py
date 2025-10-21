from typing import Any
from abc import ABC, abstractmethod

class ConexaoPort(ABC):

    @abstractmethod
    async def autenticar(self) -> bool:
        ...
    
    @abstractmethod
    async def client(self) -> Any:
        ...