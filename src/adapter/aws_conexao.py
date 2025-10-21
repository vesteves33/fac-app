from typing import Any
from boto3 import Session
from src.port.conexao import ConexaoPort
from src.model.conexao import AWSConexaoModel
from src.config.logger import logger
from botocore.exceptions import NoCredentialsError, ClientError

logger = logger("aws-conector-adapter")

class AWSConexao(ConexaoPort):
    def __init__(self, conexao_model: AWSConexaoModel):
        self.conexao_model = conexao_model
        self.session = Session(
            aws_access_key_id=conexao_model.aws_access_key_id,
            aws_secret_access_key=conexao_model.aws_secret_access_key,
            region_name=conexao_model.region_name
        )
    
    #Interface methods 
    async def autenticar(self) -> bool:
        try:
            sts_client = self.session.client('sts')
            sts_client.get_caller_identity()
            logger.info("Autenticação AWS bem-sucedida.")
            return True
        
        except NoCredentialsError:
            logger.error("Erro de Autenticação AWS: Credenciais AWS não encontradas.")
            raise PermissionError("Credenciais AWS não encontradas.")
        
        except ClientError as e:
            logger.error(f"Erro de Autenticação AWS: {e}")
            return False
        
        except Exception as e:
            logger.exception(f"Falha na autenticação AWS: {e}")
            return False
    
    async def client(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str) -> Any:
        self.session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        return self.session

