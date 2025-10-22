from typing import Any
from abc import ABC, abstractmethod

class ConectionPort(ABC):

    @abstractmethod
    async def authenticate(self) -> bool:
        ...
    
    @abstractmethod
    async def client(self) -> Any:
        ...