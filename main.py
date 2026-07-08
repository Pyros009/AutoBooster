from bot import rodar_bot
from logger import logger
from config_manager import ensure_user_id
from updater import update_manager

if __name__ == "__main__":
    
    ensure_user_id()
    
    update_manager()
    
    logger.info("A iniciar o autobooster")

    try:
        rodar_bot()
    
    except KeyboardInterrupt:
        logger.info("Autobooster parado pelo utilizador.")


