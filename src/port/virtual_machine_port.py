from typing import List
from abc import ABC, abstractmethod
from src.model.virtual_machine_model import VirtualMachineModel

class VirtualMachinePort(ABC): 
    @abstractmethod
    async def list_instances(self, instance_infos:VirtualMachineModel) -> dict:
        ...
    
    @abstractmethod
    async def get_instance(self,instance_infos: VirtualMachineModel) -> dict:
        ...