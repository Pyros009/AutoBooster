from bot import rodar_bot
from logger import logger
from config_manager import ensure_user_id
#from updater import check_updates

if __name__ == "__main__":
    ensure_user_id()
    try:
    #    check_updates()
        logger.info("A iniciar o autobooster")
        rodar_bot()
    except KeyboardInterrupt:
        logger.error("\n Script parado pelo utilizador.")


