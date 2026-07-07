from ppadb.client import Client
from config_manager import config
from logger import logger

def connect():
    client = Client(host=config["adb"]["host"], port=config["adb"]["port"])
    logger.info(f"a ligar a {config["adb"]["host"]}:{config["adb"]["port"]}")
    devices = client.devices()
    if not devices:
        return None
    logger.info(f"Device detectado: {devices[0].serial}")
    return devices[0]