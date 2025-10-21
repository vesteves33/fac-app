import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(
        self,
        app_name: str = "fac-app",
        logs_dir: str = "logs",
        level: str = "DEBUG",
        log_to_file: bool = True,
        log_to_console: bool = False,
        json_format: bool = True
    ):
        """
        Inicializa o sistema de logging
        
        Args:
            app_name: Nome da aplicação para identificação nos logs
            logs_dir: Diretório onde os arquivos de log serão salvos
            level: Nível mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Se True, salva logs em arquivos
            log_to_console: Se True, exibe logs no console
            json_format: Se True, usa formato JSON nos arquivos
        """
        self.app_name = app_name
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
        
        self.level = level
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.json_format = json_format
        
        self.standard_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(module)s:%(funcName)s:%(lineno)d | %(message)s"
        )
        
        self._main_logger = self._setup_logger(app_name)
    
    def _setup_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, self.level.upper()))
        
        logger.handlers.clear()
        
        if self.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_formatter = ColoredFormatter(
                self.standard_format,
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # File Handler - Logs gerais
        if self.log_to_file:
            general_log_file = self.logs_dir / "app.log"
            file_handler = RotatingFileHandler(
                general_log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)
            
            if self.json_format:
                file_formatter = JSONFormatter()
            else:
                file_formatter = logging.Formatter(
                    self.standard_format,
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            # Log de erros separado
            error_log_file = self.logs_dir / "errors.log"
            error_handler = RotatingFileHandler(
                error_log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            logger.addHandler(error_handler)
        
        logger.propagate = False
        
        return logger
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        if name:
            return logging.getLogger(f"{self.app_name}.{name}")
        return self._main_logger
    
    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        client_ip: Optional[str] = None
    ) -> None:
        """
        Loga informações de requisição HTTP
        
        Args:
            method: Método HTTP (GET, POST, etc)
            path: Caminho da requisição
            status_code: Código de status da resposta
            duration_ms: Duração da requisição em milissegundos
            client_ip: Endereço IP do cliente (opcional)
        """
        logger = self.get_logger("http")
        
        log_message = (
            f"[{method}] {path} - Status: {status_code} - "
            f"Duration: {duration_ms:.2f}ms"
        )
        
        if client_ip:
            log_message += f" - Client: {client_ip}"
        
        if status_code >= 500:
            logger.error(log_message)
        elif status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def log_exception(
        self,
        exc: Exception,
        context: Optional[Dict[str, Any]] = None,
        logger_name: Optional[str] = None
    ) -> None:
        logger = self.get_logger(logger_name or "exceptions")
        
        error_msg = f"Exception: {type(exc).__name__} - {str(exc)}"
        
        if context:
            error_msg += f" | Context: {json.dumps(context, ensure_ascii=False)}"
        
        logger.exception(error_msg)
    
    def debug(self, message: str, logger_name: Optional[str] = None) -> None:
        logger = self.get_logger(logger_name)
        logger.debug(message)
    
    def info(self, message: str, logger_name: Optional[str] = None) -> None:
        logger = self.get_logger(logger_name)
        logger.info(message)
    
    def warning(self, message: str, logger_name: Optional[str] = None) -> None:
        logger = self.get_logger(logger_name)
        logger.warning(message)
    
    def error(self, message: str, logger_name: Optional[str] = None, exc_info: bool = False) -> None:
        logger = self.get_logger(logger_name)
        logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, logger_name: Optional[str] = None) -> None:
        logger = self.get_logger(logger_name)
        logger.critical(message)

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        record.levelname = f"{color}{record.levelname:8}{reset}"
        record.name = f"{color}{record.name}{reset}"
        
        return super().format(record)


# Função retornando uma instancia padrão do Logger facilitando uso e instanciação na aplicação
def logger(name: Optional[str] = None) -> logging.Logger:
    logger = Logger()
    return logger.get_logger(name)