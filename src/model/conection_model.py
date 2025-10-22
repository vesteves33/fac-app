from typing import Optional, Dict, Any
from pydantic import BaseModel, model_validator

class AWSConectionModel(BaseModel):
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    region_name: Optional[str] = None
    aws_session_token: Optional[str] = None # Token opcional para credenciais temporárias


class GCPConectionModel(BaseModel):
    project_id: Optional[str] = None
    service_account_path: Optional[str] = None
    service_account_info: Optional[Dict[str, Any]] = None # JSON com as informações da conta de serviço

    @model_validator(mode='before')
    @classmethod
    def check_exclusive_auth_methods(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get('service_account_path') and values.get('service_account_info'):
            raise ValueError('service_account_path e service_account_info são mutuamente exclusivos')
        return values