from bot import rodar_bot
from logger import logger, configure_logger
from config_manager import ensure_user_id, config
from updater import update_manager
import sys

import psutil
import os

if __name__ == "__main__":
    
    logger.warning(f"PID: {os.getpid()}")    
    configure_logger(config["debug"])
    logger.warning("Current version................")
    ensure_user_id()
       
    if update_manager():
        sys.exit(0)
    
    logger.info("A iniciar o autobooster")

    try:
        rodar_bot()
        
    except KeyboardInterrupt:
        logger.info("Autobooster parado pelo utilizador.")
    
    logger.info("Main terminou.")

    import threading

    threads = threading.enumerate()
    logger.info(f"Threads ativas: {len(threads)}")

    for t in threads:
        logger.info(f"{t.name} daemon={t.daemon}")


