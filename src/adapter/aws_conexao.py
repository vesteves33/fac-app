from typing import Any
from aioboto3 import Session
from src.config.logger import logger
from src.port.conexao import ConexaoPort
from src.model.conexao import AWSConexaoModel
from botocore.exceptions import NoCredentialsError, ClientError

logger = logger("aws-conector-adapter")

class AWSConexao(ConexaoPort):
    def __init__(self, conexao_model: AWSConexaoModel):
        self.conexao_model = conexao_model
       
        # Utilizando Session da lib aioboto3 que permite Assincronismos
        session_kwargs = conexao_model.model_dump(exclude_none=True)
        self.session = Session(**session_kwargs)
        self._authenticated = False

    #Interface methods
    async def autenticar(self) -> bool:
        try:
            async with self.session.client('sts') as sts_client:
                await sts_client.get_caller_identity()
            logger.info("Autenticação AWS bem-sucedida.")
            self._authenticated = True
           
            return True
       
        except NoCredentialsError:
            logger.error("Erro de Autenticação AWS: Credenciais AWS não encontradas.")
            raise PermissionError("Credenciais AWS não encontradas.")
       
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
           
            if error_code == "InvalidClientTokenId":
                logger.error(f"Erro de autenticação AWS: Credenciais inválidas.")
                raise PermissionError(f"Credenciais AWS inválidas: {e}")
           
            logger.error(f"Erro de Cliente AWS: {e}")
            raise PermissionError(f"Falha ao autenticar com AWS: {e}")
       
        except Exception as e:
            logger.exception(f"Erro inesperado na autenticação AWS: {e}")
            raise ConnectionError(f"Erro de conexão AWS: {e}")
   
    async def client(self) -> Any:
        if not self._authenticated:
            raise ConnectionError('Sessão não autenticada. Utilize o metodo autenticar() primeiro')
       
        return self.session
