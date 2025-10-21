from pathlib import Path
from fastapi import FastAPI
from pkgutil import iter_modules
from importlib import import_module
from src.config.logger import logger
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="FaC - FinOps as Code application",
    description="Application looking into FinOps automations, resource management, cost optimization and best practices",
    version="1.0",
    root_path='./'
)

logger = logger("main")

def load_routes() -> None:
    path = Path(__file__).parent / "router"

    if not path.exists():
        logger.error('Modulo de rotas da aplicação não encontrado')
        return
    
    # Detecta o prefixo do módulo baseado em __package__
    # Se __package__ é 'src', usa 'src.router', senão usa 'router'
    module_prefix = f"{__package__}.router" if __package__ else "router"
    
    for module_info in iter_modules([str(path)]):
        if module_info.name.startswith("_"):
            continue
        
        try:
            module_name = f'{module_prefix}.{module_info.name}'
            module = import_module(module_name)

            if hasattr(module, 'router'):
                app.include_router(module.router)
                
                logger.info(f"Rota carregada: {module_name}")
            
            else:
                logger.warning(f"Módulo 'router.{module_name}' não possui objeto 'router' ")
        
        except Exception as e:
            logger.exception(f"Erro ao carregar router.{module_name}: {e}")
                
@app.get('/', include_in_schema=False, tags=["Root"])
async def redirect_root() -> dict:
    '''Redireciona rota raiz para o Swagger da aplicação (/docs) '''
    logger.info("Redirecionando '/' para '/docs'")
    return RedirectResponse(url='/docs')

load_routes()