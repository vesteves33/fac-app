from aioboto3 import Session
from src.config.logger import logger
from src.port.virtual_machine_port import VirtualMachinePort
from src.model.virtual_machine_model import VirtualMachineModel
from botocore.exceptions import ClientError


logger = logger("aws-ec2-adapter")

class AWSEC2Adapter(VirtualMachinePort):
    def __init__(self, session: Session):
        self.session = session

    # Interface methods
    async def list_instances(self, instance_infos:VirtualMachineModel) -> dict:
        logger.info("Listing EC2 instances from AWS")

        async with self.session.client('ec2') as ec2_client:
            try:
                response = await ec2_client.describe_instances()
                
                instances = []
                for reservation in response.get('Reservations', []):
                    for instance_data in reservation.get('Instances', []):
                        instances.append(instance_data)
                        
                logger.info(f"Encontradas {len(instances)} instâncias EC2.")
                return instances
            
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Erro ao listar instâncias EC2: {error_code} - {e}")
                raise RuntimeError(f"Falha na API EC2: {error_code}") from e
            
            except Exception as e:
                logger.exception(f"Erro inesperado ao listar instâncias EC2: {e}")
                raise ConnectionError("Erro ao comunicar com o serviço EC2") from e
    
    async def get_instance(self, instance_infos: VirtualMachineModel) -> dict:
        if not instance_infos.instance_id:
            raise ValueError("O ID da instância é obrigatório para a busca.")

        logger.info(f"Buscando instância EC2: {instance_infos.instance_id}")

        async with self.session.client('ec2') as ec2_client:
            try:
                response = await ec2_client.describe_instances(
                    InstanceIds=[instance_infos.instance_id]
                )

                reservations = response.get('Reservations', [])
                if not reservations or not reservations[0].get('Instances'):
                    logger.warning(f"Instância {instance_infos.instance_id} não encontrada.")
                    raise FileNotFoundError(f"Instância EC2 com ID {instance_infos.instance_id} não encontrada.")

                instance_data = reservations[0]['Instances'][0]
                logger.info(f"Instância {instance_infos.instance_id} encontrada. Estado: {instance_data.get('State', {}).get('Name')}")
                return instance_data
                
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Erro ao buscar instância EC2: {error_code} - {e}")
                raise RuntimeError(f"Falha na API EC2: {error_code}") from e
            
            except Exception as e:
                logger.exception(f"Erro inesperado ao buscar instância EC2: {e}")
                raise ConnectionError("Erro ao comunicar com o serviço EC2") from e