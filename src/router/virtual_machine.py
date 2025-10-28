from src.config.logger import Logger
from src.config.settings import settings
from fastapi import APIRouter, HTTPException, Depends
from src.model.virtual_machine_model import VirtualMachineModel
from src.service.virtual_machine_service import VirtualMachineService
from src.dependencies.aws_vm_di import get_aws_virtual_machine_service

router = APIRouter(
    prefix="/virtual-machine",
    tags=["AWS EC2 - Elastic Compute Cloud", 
          "GCP GCE - Google Compute Engine",]
)

logger = Logger()
logger.get_logger("router.virtual-machine")

# ===== Health Check Virtual Machine Endpoint =====
@router.get("/")
async def check_virtual_machine_router() -> dict:
    logger.log_request(method="GET", path="/", status_code=200, message="Health Check Virtual Machine Router")
    return {
        "health": True,
        "message": "Virtual Machine Router healthy"
        }


# # ===== Endpoints AWS EC2 =====
@router.get("/ec2/instances")
async def list_ec2_instances(
    service: VirtualMachineService = Depends(get_aws_virtual_machine_service)
):
    logger.log_request(method="GET", path="/ec2/instances", status_code=200, message="List AWS EC2 Instances")
    
    try:
        params = VirtualMachineModel(region=settings.AWS_REGION)
        
        instances = await service.list_instances(params)
        return {'instances': instances}
    
    except Exception as exc:
        logger.log_exception(exc, logger_name="router.virtual-machine.ec2")
        raise HTTPException(status_code=500, detail="Erro interno ao listar instâncias")

# @router.get("/ec2/instances/{instance_id}")
# async def get_ec2_instance(
#     instance_id: str,
#     region: Optional[str] = Query(None),
#     service: EC2Service = Depends(get_ec2_service)
# ):
#     """
#     Obtém detalhes de uma instância específica
    
#     Args:
#         instance_id: ID da instância EC2 (ex: i-1234567890abcdef0)
#         region: Região AWS
#     """
#     logger.info(f"GET /ec2instances/{instance_id}")
    
#     try:
#         ...
    
#     except Exception as exc:
#         logger.log_exception(exc, logger_name="router.ec2")
#         raise HTTPException(status_code=500, detail="Erro interno")
# # =============================

# # ===== Endpoints GCP GCE =====
@router.get("/gce/instances")
async def list_gce_instances():
    logger.log_request(method="GET", path="/gce/instances", status_code=200, message="List GCP GCE Instances")
    
    try:
        ...
    
    except Exception as exc:
        logger.log_exception(exc, logger_name="router.gce")
        raise HTTPException(status_code=500, detail="Erro interno ao listar instâncias")

# @router.get("/gce/instances/{instance_id}")
# async def get_gce_instance(
#     instance_id: str,
#     region: Optional[str] = Query(None),
#     service: EC2Service = Depends(get_ec2_service)
# ):
#     """
#     Obtém detalhes de uma instância específica
    
#     Args:
#         instance_id: ID da instância EC2 (ex: i-1234567890abcdef0)
#         region: Região AWS
#     """
#     logger.info(f"GET /gce/instances/{instance_id}")
    
#     try:
#         ...
    
#     except Exception as exc:
#         logger.log_exception(exc, logger_name="router.ec2")
#         raise HTTPException(status_code=500, detail="Erro interno")
# # =============================
