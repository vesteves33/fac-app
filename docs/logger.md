# 📘 Guia de Uso da Classe Logger

## 🎯 Visão Geral

A classe `Logger` encapsula toda a funcionalidade de logging da aplicação em uma interface orientada a objetos, facilitando o uso e manutenção.

## 🏗️ Estrutura da Classe
```python
class Logger:
    - __init__()           # Inicializa o sistema de logging
    - _setup_logger()      # Configura um logger (método privado)
    - get_logger()         # Retorna um logger específico
    - log_request()        # Loga requisições HTTP
    - log_exception()      # Loga exceções com contexto
    - debug()              # Log de nível DEBUG
    - info()               # Log de nível INFO
    - warning()            # Log de nível WARNING
    - error()              # Log de nível ERROR
    - critical()           # Log de nível CRITICAL
```

## 🚀 Como Usar

### Método 1: Usando a Instância Global (Recomendado)
```python
from src.config.logger import logger

# Métodos diretos da instância
logger.info("Aplicação iniciada")
logger.debug("Valor de X: %s", x)
logger.error("Erro ao processar", exc_info=True)

# Log de requisições HTTP
logger.log_request(
    method="GET",
    path="/api/users",
    status_code=200,
    duration_ms=45.2,
    client_ip="192.168.1.100"
)

# Log de exceções
try:
    result = process_data()
except Exception as exc:
    logger.log_exception(
        exc,
        context={"user_id": 123, "action": "process_data"}
    )
```

### Método 2: Criar Instância Customizada
```python
from src.config.logger import Logger

# Logger customizado para um módulo específico
payment_logger = Logger(
    app_name="payment-service",
    logs_dir="logs/payments",
    level="INFO",
    log_to_file=True,
    log_to_console=False,
    json_format=True
)

payment_logger.info("Pagamento processado")
payment_logger.error("Falha na transação")
```

## 📝 Exemplos Práticos por Cenário

### 1. Em Rotas do FastAPI
```python
from fastapi import APIRouter, HTTPException
from src.config.logger import logger

router = APIRouter(prefix="/api/users")

@router.post("/")
async def create_user(user_data: dict):
    logger = logger("users")
    
    logger.info(f"Criando usuário: {user_data.get('email')}")
    logger.debug(f"Dados completos: {user_data}")
    
    try:
        user_id = save_to_database(user_data)
        logger.info(f"Usuário criado com sucesso: ID={user_id}")
        return {"id": user_id, "status": "created"}
    
    except ValueError as e:
        logger.warning(f"Validação falhou: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.log_exception(
            e,
            context={"email": user_data.get('email')},
            logger_name="users"
        )
        raise HTTPException(status_code=500, detail="Erro interno")
```

### 2. Em Serviços/Business Logic
```python
from src.config.logger import logger

class UserService:
    def __init__(self):
        self.logger = logger("services.users")
    
    def process_registration(self, data: dict):
        self.logger.info("Iniciando registro de usuário")
        
        if not self._validate(data):
            self.logger.warning(f"Dados inválidos: {data}")
            return None
        
        try:
            user = self._create_user(data)
            self.logger.info(f"Usuário registrado: {user.id}")
            return user
        except Exception as exc:
            logger.log_exception(
                exc,
                context={"data": data},
                logger_name="services.users"
            )
            raise
    
    def _validate(self, data: dict) -> bool:
        self.logger.debug(f"Validando dados: {list(data.keys())}")
        return "email" in data and "password" in data
```

### 3. Em Middleware
```python
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.config.logger import logger

class CustomLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logger("middleware")
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        self.logger.debug(
            f"→ Request: {request.method} {request.url.path}"
        )
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            logger.log_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                client_ip=request.client.host if request.client else None
            )
            
            return response
        
        except Exception as exc:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.error(
                f"✗ Request failed: {request.method} {request.url.path} "
                f"after {duration_ms:.2f}ms"
            )
            logger.log_exception(exc, context={
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms
            })
            raise
```

### 4. Em Tarefas Background/Async
```python
import asyncio
from src.config.logger import logger

class BackgroundTaskProcessor:
    def __init__(self):
        self.logger = logger("background")
    
    async def process_queue(self):
        self.logger.info("Iniciando processamento de fila")
        
        while True:
            try:
                task = await self.get_next_task()
                
                if task:
                    self.logger.debug(f"Processando task: {task.id}")
                    await self.execute_task(task)
                    self.logger.info(f"Task {task.id} concluída")
                else:
                    await asyncio.sleep(1)
            
            except Exception as exc:
                logger.log_exception(
                    exc,
                    context={"task_id": task.id if task else None},
                    logger_name="background"
                )
                await asyncio.sleep(5)  # Backoff em caso de erro
```

### 5. Em Testes Unitários
```python
import pytest
from src.config.logger import logger

@pytest.fixture
def test_logger():
    """Logger para testes"""
    return logger(
        app_name="test",
        logs_dir="logs/test",
        level="DEBUG",
        log_to_console=False,
        log_to_file=True
    )

def test_user_creation(test_logger):
    test_logger.info("Testando criação de usuário")
    
    user = create_user({"name": "Test"})
    
    assert user.name == "Test"
    test_logger.debug(f"Usuário criado: {user.id}")
```

## 🎨 Métodos Disponíveis

### `__init__()` - Inicialização

```python
logger = logger(
    app_name="minha-app",      # Nome da aplicação
    logs_dir="logs",           # Diretório de logs
    level="DEBUG",             # Nível mínimo de log
    log_to_file=True,          # Salvar em arquivo?
    log_to_console=True,       # Exibir no console?
    json_format=False          # Usar formato JSON?
)
```

### `logger(name)` - Obter Logger Específico

```python
# Logger principal
main_logger = logger()

# Logger de módulo específico
user_logger = logger("users")
auth_logger = logger("auth")
db_logger = logger("database")
```

### `log_request()` - Log de Requisições HTTP

```python
logger.log_request(
    method="POST",              # Método HTTP
    path="/api/users",          # Caminho
    status_code=201,            # Status code
    duration_ms=123.45,         # Duração em ms (Opctional)
    client_ip="192.168.1.100"   # IP do cliente (opcional)
    message="Text message"      # Mensagem adaptada ao contexto do uso (Opcional)
)
```

### `log_exception()` - Log de Exceções

```python
try:
    risky_operation()
except Exception as exc:
    logger.log_exception(
        exc,                           # Exceção capturada
        context={                      # Contexto adicional (opcional)
            "user_id": 123,
            "action": "risky_operation"
        },
        logger_name="operations"       # Nome do logger (opcional)
    )
```

### Métodos de Log por Nível

```python
# DEBUG - Informações detalhadas de debug
logger.debug("Variável X = 10", logger_name="debug")

# INFO - Informações gerais
logger.info("Operação concluída", logger_name="main")

# WARNING - Avisos
logger.warning("Recurso limitado", logger_name="resources")

# ERROR - Erros
logger.error("Falha na operação", logger_name="errors", exc_info=True)

# CRITICAL - Erros críticos
logger.critical("Sistema crítico falhou", logger_name="system")
```

## ✅ Vantagens da Classe Logger

1. **Encapsulamento**: Toda lógica de logging em um único lugar
2. **Flexibilidade**: Fácil criar múltiplas instâncias para diferentes propósitos
3. **Testabilidade**: Pode criar loggers isolados para testes
4. **Manutenibilidade**: Mudanças centralizadas na classe
5. **Compatibilidade**: Mantém funções antigas funcionando
6. **Type Hints**: Melhor autocomplete e validação de tipos

## 🎯 Recomendações

- Use `logger` diretamente para logging simples
- Use `logger(name)` quando precisar de loggers nomeados
- Sempre use `log_exception()` para capturar exceções
- Em produção, considere `json_format=True` para análise automatizada
- Mantenha `log_to_console=False` em produção (use stdout do container)

---
