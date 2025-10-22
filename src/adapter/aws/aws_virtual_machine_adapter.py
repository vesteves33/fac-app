from typing import List
from src.config.logger import logger
from src.port.virtual_machine_port import VirtualMachinePort
from src.model.virtual_machine_model import VirtualMachineModel


logger = logger("aws-ec2-adapter")

class AWSEC2Adapter(VirtualMachinePort):
    def __init__(self, virtual_machine_model: VirtualMachineModel):
        self.virtual_machine_model = virtual_machine_model

    # Interface methods
    async def list_instances(self, instance_infos:VirtualMachineModel) -> List[dict]:
        ...
    
    async def get_instance(self,instance_infos: VirtualMachineModel) -> dict:
        ...