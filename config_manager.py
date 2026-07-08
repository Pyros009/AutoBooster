import json
import random
from pathlib import Path
import uuid
import shutil
from logger import logger

BASE_PATH = Path(__file__).parent / "config"
CONFIG_PATH = BASE_PATH / "config.json"
CONFIG_DEFAULT_PATH = BASE_PATH / "config_default.json"
PRIVATE_PATH = BASE_PATH / "private.json"
PRIVATE_DEFAULT_PATH = BASE_PATH / "private_default.json"
STATE_PATH = BASE_PATH / "state.json"
STATE_DEFAULT_PATH = BASE_PATH / "state_default.json"

def ensure_config():
    if not CONFIG_DEFAULT_PATH.exists():
        raise FileNotFoundError(
            f"Ficheiro em falta: {CONFIG_DEFAULT_PATH}"
        )
        
    
    if CONFIG_PATH.exists():
        return 
    
    logger.info("config.json não encontrado. A criar a partir do template.")
    shutil.copy(CONFIG_DEFAULT_PATH, CONFIG_PATH)
    return 
    
def ensure_state():
    if not STATE_DEFAULT_PATH.exists():
        raise FileNotFoundError(
            f"Ficheiro em falta: {STATE_DEFAULT_PATH}"
        )
        
    if STATE_PATH.exists():
        return 

    logger.info("state.json não encontrado. A criar a partir do template.")
    shutil.copy(STATE_DEFAULT_PATH, STATE_PATH)
    return

def ensure_private():
    if not PRIVATE_DEFAULT_PATH.exists():
        raise FileNotFoundError(
            f"Ficheiro em falta: {PRIVATE_DEFAULT_PATH}"
        )
        
    if PRIVATE_PATH.exists():
        return 

    logger.info("private.json não encontrado. A criar a partir do template.")
    shutil.copy(PRIVATE_DEFAULT_PATH, PRIVATE_PATH)
    return       

def random_timer(name):
    timer = config["timers"][name]
    return random.randint(timer["min"],timer["max"])

def save_config():
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
def save_state():
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)
        
def ensure_user_id():
    if not config["user_id"]:
        config["user_id"] = str(uuid.uuid4())
        save_config()
        
def init_configs():
    ensure_config()
    ensure_state()
    ensure_private()

    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = json.load(f)
        
    with PRIVATE_PATH.open(encoding="utf-8") as g:
        private = json.load(g)

    with STATE_PATH.open(encoding="utf-8") as h:
        state = json.load(h)