from typing import List
from src.config.logger import logger
from src.port.virtual_machine_port import VirtualMachinePort
from src.model.virtual_machine_model import VirtualMachineModel

logger = logger("virtual-machine-service")

class VirtualMachineService:
    def __init__(self, vm_port: VirtualMachinePort):
        self.vm_port = vm_port

    async def list_instances(self, instance_infos: VirtualMachineModel) -> dict:
        logger.info("Listing virtual machine instances")
        instances = await self.vm_port.list_instances(instance_infos)
        return instances

    async def get_instance(self, instance_infos: VirtualMachineModel) -> dict:
        logger.info(f"Getting virtual machine instance: {instance_infos.instance_id}")
        instance = await self.vm_port.get_instance(instance_infos)
        return instance