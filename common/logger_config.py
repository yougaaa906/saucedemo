# common/logger_config.py
import os
import logging
from datetime import datetime

def configure_logger(name="saucedemo_logger"):
    # Create saucedemo exclusive log directory
    log_dir = "logs-saucedemo"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log file with timestamp
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Get logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    # Create stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    
    # Set log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger
