from ppadb.client import Client
from config_manager import config, save_config
from logger import logger
from pathlib import Path
import subprocess

def connect():
    client = Client(host=config["adb"]["host"], port=config["adb"]["port"])
    logger.info(f"a ligar a {config["adb"]["host"]}:{config["adb"]["port"]}")
    devices = client.devices()
    if not devices:
        logger.critical("Nao foram detectados devices")
        return None
    logger.info(f"Dispositivo detectado: {devices[0].serial}")
    return devices[0]

def find_adb():
    location = config["adb"]["location"]

    if location:
        saved = Path(location)
        if saved.exists():
            logger.info("Localizacao do adb encontrado, continuando...")
            return saved
    
    logger.info("Localizacao do adb nao guardada, iniciando a busca...")
    POSSIBLE_PATHS = [
        Path(r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"),
        Path(r"C:\Program Files\BlueStacks X\HD-Adb.exe"),
        Path(r"C:\Program Files (x86)\BlueStacks\HD-Adb.exe"),
    ]

    for path in POSSIBLE_PATHS:
        if path.exists():
            logger.info(f"Adb encontrado em {str(path)}")
            config["adb"]["location"] = str(path)
            save_config()
            logger.info("Localizacao do adb guardada na configuracao")
            return path

    return None

def connect_emulator(path):
    result = subprocess.run(
                                [
                                    str(path),
                                    "connect",
                                    config["adb"]["device"]
                                ],
                                capture_output=True,
                                text=True
                            )
    
    
    if result.returncode == 0:
        logger.debug(result.stdout.strip())
        return True
    
    logger.error(result.stderr.strip() or result.stdout.strip())
    return False