import asyncio
from google.auth import default
from src.config.logger import logger
from typing import Optional, Any, Tuple
from google.oauth2 import service_account
from google.auth.credentials import Credentials
from src.port.conection_port import ConectionPort
from google.auth.exceptions import  GoogleAuthError
from src.model.conection_model import GCPConectionModel

logger = logger("gcp-conector-adapter")

class GCPConection(ConectionPort):
    def __init__(self, conection_model: GCPConectionModel):
        self.conection_model = conection_model
        self.credentials: Optional[Credentials] = None
        self.project_id: Optional[str] = conection_model.project_id

        self._authenticated = False
    
    #Interface methods
    async def authenticate(self) -> bool:
        try:
            if self.conection_model.service_account_info:
                logger.info("Autenticação GCP realizada com service_account_info.")
                self.credentials = service_account.Credentials.from_service_account_info(
                    self.conection_model.service_account_info
                )
            
                if not self.project_id and hasattr(self.credentials, 'project_id'):
                    self.project_id = self.credentials.project_id

            elif self.conection_model.service_account_path:
                logger.info(f"Autenticação GCP realizada com service_account_path: {self.conection_model.service_account_path}...")
                
                self.credentials = await asyncio.to_thread(service_account.Credentials.from_service_account_file,
                    self.conection_model.service_account_path
                )
                if not self.project_id and hasattr(self.credentials, 'project_id'):
                    self.project_id = self.credentials.project_id
        
            else:
                logger.info("Autenticação GCP sendo realizada via Aplication Default Credentials (ADC)...")

                credentials_tuple: Tuple[Credentials, Optional[str]] = await asyncio.to_thread(
                    default
                )
                self.credentials, default_project_id = credentials_tuple

                if not self.project_id and default_project_id:
                    self.project_id = default_project_id

            if not self.credentials:
                raise GoogleAuthError("Nenhuma credencial encontrada via Application Default Credentials (ADC).")
        
            if not self.project_id:
                logger.warning("Autenticação GCP realizada, mas o project_id não foi fornecido.")
            
            logger.info(f"Autenticação GCP realizada com sucesso. Projeto: {self.project_id}")
            self._authenticated = True
            return True
        
        except FileNotFoundError:
            logger.error(f"Arquivo de conta de serviço não encontrado: {self.conection_model.service_account_path}")
            raise FileNotFoundError(f"Arquivo de conta de serviço não encontrado: {self.conection_model.service_account_path}")

        except GoogleAuthError as e:
            logger.error(f"Erro de autenticação GCP. Falha ao carregar credenciais: {e}")
            raise PermissionError(f"Falha ao carregar / autenticar credenciais GCP: {e}")

        except Exception as e:
            logger.exception(f"Erro inesperado durante a autenticação GCP: {e}")
            raise ConnectionError(f"Erro inesperado durante a autenticação GCP: {e}")
        
    async def client(self) -> Any:
        if not self._authenticated or not self.credentials:
            raise ConnectionError("Sessão não autenticada. Chame o método 'autenticar()' primeiro.")
        
        return {
            'credentials': self.credentials, 
            'project_id': self.project_id
            }