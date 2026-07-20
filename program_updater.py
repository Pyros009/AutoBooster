import json
import requests
import time
from config_manager import config, save_config, save_state, state, private

## 1) first check if version changes

# 2a ) if so, do update, then 3

# 2b) if not, exit and launch the main

## 3) after update, loopback to 1

## 1 - checking for version

current_version = state["program_version"]
url = private["github_version"] + f"?t={time.time_ns()}"
response = requests.get(url)#private["github_version"])

print(response.json()["program"]["version"])