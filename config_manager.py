import json
import random
from pathlib import Path
import uuid

BASE_PATH = Path(__file__).parent / "config"

CONFIG_PATH = BASE_PATH / "config.json"
PRIVATE_PATH = BASE_PATH / "private.json"
STATE_PATH = BASE_PATH / "state.json"

with CONFIG_PATH.open(encoding="utf-8") as f:
    config = json.load(f)
    
with PRIVATE_PATH.open(encoding="utf-8") as g:
    private = json.load(g)

with STATE_PATH.open(encoding="utf-8") as h:
    state = json.load(h)
    
def random_timer(name):
    timer = config["timers"][name]
    return random.randint(timer["min"],timer["max"])

def save_config():
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
def ensure_user_id():
    if not config["user_id"]:
        config["user_id"] = str(uuid.uuid4())
        save_config()
        
def save_state():
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)