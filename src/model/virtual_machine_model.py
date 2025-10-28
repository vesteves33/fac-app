from pydantic import BaseModel
from typing import Optional, Dict

class VirtualMachineModel(BaseModel):
    instance_id: Optional[str] = None
    machine_type: Optional[str] = None
    region: str
    state: Optional[str] = None # Ex: running, stopped, terminated
    tags: Optional[Dict[str, str]] = None