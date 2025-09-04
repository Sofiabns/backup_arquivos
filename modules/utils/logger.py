"""
Módulo de logging para o sistema
Registra todas as operações realizadas
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(log_level=logging.INFO):
    """
    Configura o sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Cria pasta de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de log com timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"crypto_system_{timestamp}.log"
    
    # Configura o logger
    logger = logging.getLogger("CryptoSystem")
    logger.setLevel(log_level)
    
    # Remove handlers existentes para evitar duplicação
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Formatter para as mensagens de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console (apenas INFO e acima)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Apenas warnings e erros no console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info("Sistema de logging inicializado")
    logger.info(f"Arquivo de log: {log_file}")
    
    return logger

def log_operation(logger, operation_type, file_path, success=True, error_msg=None):
    """
    Registra uma operação realizada no sistema
    
    Args:
        logger: Logger configurado
        operation_type (str): Tipo de operação (encrypt, decrypt, etc.)
        file_path (str): Caminho do arquivo processado
        success (bool): Se a operação foi bem-sucedida
        error_msg (str): Mensagem de erro, se houver
    """
    if success:
        logger.info(f"{operation_type.upper()} SUCCESS: {file_path}")
    else:
        logger.error(f"{operation_type.upper()} FAILED: {file_path} - {error_msg}")

def log_system_info(logger):
    """
    Registra informações do sistema
    
    Args:
        logger: Logger configurado
    """
    import platform
    import sys
    
    logger.info("=== INFORMAÇÕES DO SISTEMA ===")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Plataforma: {platform.platform()}")
    logger.info(f"Arquitetura: {platform.architecture()}")
    logger.info(f"Processador: {platform.processor()}")
    logger.info("=" * 35)

class CryptoLogger:
    """Classe especializada para logging de operações de criptografia"""
    
    def __init__(self, logger_name="CryptoSystem"):
        self.logger = logging.getLogger(logger_name)
    
    def log_encryption_start(self, files_count):
        """Registra início do processo de criptografia"""
        self.logger.info(f"Iniciando criptografia de {files_count} arquivo(s)")
    
    def log_decryption_start(self, files_count):
        """Registra início do processo de descriptografia"""
        self.logger.info(f"Iniciando descriptografia de {files_count} arquivo(s)")
    
    def log_file_processed(self, operation, file_path, input_size, output_size):
        """Registra processamento de arquivo individual"""
        compression_ratio = (1 - output_size / input_size) * 100 if input_size > 0 else 0
        self.logger.info(
            f"{operation}: {file_path} | "
            f"Entrada: {self._format_size(input_size)} | "
            f"Saída: {self._format_size(output_size)} | "
            f"Taxa: {compression_ratio:+.1f}%"
        )
    
    def log_batch_summary(self, operation, total_files, successful, failed, total_time):
        """Registra resumo de operação em lote"""
        self.logger.info(
            f"RESUMO {operation.upper()}: "
            f"Total: {total_files} | "
            f"Sucesso: {successful} | "
            f"Falha: {failed} | "
            f"Tempo: {total_time:.2f}s"
        )
    
    def _format_size(self, size_bytes):
        """Formata tamanho em bytes para string legível"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = size_bytes
        
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"