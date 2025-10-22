from src.config.logger import Logger
from fastapi import APIRouter, HTTPException

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
async def list_ec2_instances():
    logger.log_request(method="GET", path="/ec2/instances", status_code=200, message="List EC2 Instances")
    
    try:
        instances = ['instance1', 'instance2', 'instance3']
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
# @router.get("/gce/instances")
# async def list_gce_instances(
#     region: Optional[str] = Query(None, description="Região AWS"),
#     state: Optional[InstanceState] = Query(None, description="Filtrar por estado"),
#     tag_key: Optional[str] = Query(None, description="Chave da tag para filtro"),
#     tag_value: Optional[str] = Query(None, description="Valor da tag para filtro"),
#     include_terminated: bool = Query(False, description="Incluir instâncias terminadas"),
#     service: EC2Service = Depends(get_ec2_service)
# ):
#     logger.log_request(f"GET /gce/instances - Region: {region}, State: {state}")
    
#     try:
#         ...
    
#     except Exception as exc:
#         logger.log_exception(exc, logger_name="router.ec2")
#         raise HTTPException(status_code=500, detail="Erro interno ao listar instâncias")

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
