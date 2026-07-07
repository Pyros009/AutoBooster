import logging
from config_manager import config

logging.basicConfig(
    level = logging.DEBUG if config["debug"] else logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("AutoBooster")