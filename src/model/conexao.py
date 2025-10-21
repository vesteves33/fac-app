from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AWSConexaoModel(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    aws_session_token: Optional[str] = None # Token opcional para credenciais temporárias

class GCPConexaoModel(BaseModel):
    project_id: str
    service_account_path: str
    service_account_info: dict # JSON com as informações da conta de serviço
