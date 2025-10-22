from pydantic import BaseModel
from typing import Optional, Dict

class VirtualMachineModel(BaseModel):
    instance_id: str
    machine_type: str
    region: str
    state: str # Ex: running, stopped, terminated
    tags: Optional[Dict[dict, None]] = None