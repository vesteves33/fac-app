from aioboto3 import Session
from src.config.logger import logger
from src.config.settings import settings
from src.model.conection_model import AWSConectionModel
from src.port.virtual_machine_port import VirtualMachinePort
from src.adapter.aws.aws_conection_adapter import AWSConection
from src.adapter.aws.aws_virtual_machine_adapter import AWSEC2Adapter
from src.service.virtual_machine_service import VirtualMachineService

logger = logger("dependency-injection.aws-vm")

class AWSVirtualMachineDI:
    _service_instance: VirtualMachineService | None = None

    @classmethod
    async def get_service(cls) -> VirtualMachineService:
        """
        Método de classe que atua como a função de dependência do FastAPI.
        Garante que a autenticação e a criação do serviço ocorram apenas uma vez (Singleton).
        """
        if cls._service_instance is not None:
            logger.debug("Retornando instância Singleton de VirtualMachineService (AWS).")
            return cls._service_instance

        try:
            conection_model = AWSConectionModel(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )

            aws_conector = AWSConection(conection_model=conection_model)
            await aws_conector.authenticate()
            
            aws_session: Session = await aws_conector.client()
            
            ec2_adapter: VirtualMachinePort = AWSEC2Adapter(session=aws_session)

            cls._service_instance = VirtualMachineService(vm_port=ec2_adapter)
            
            logger.info("VirtualMachineService (AWS/EC2) configurado e cacheado com sucesso.")
            return cls._service_instance

        except Exception as exc:
            logger.critical(f"Falha CRÍTICA na inicialização da dependência AWS: {exc}")
            raise exc

# Isto mantém a clareza e permite mudar a lógica interna (para a classe) sem 
# alterar a forma como o FastAPI a consome.
get_aws_virtual_machine_service = AWSVirtualMachineDI.get_service