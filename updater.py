import requests
import json
from config_manager import state, private
from logger import logger

program_current = state["program_version"]
targets_current = state["targets_version"]

def check_updates():
    
    response = requests.get(private["github_version"])
    repo_p_version = response.json()["program_version"]
    repo_t_version = response.json()["targets_version"]
    
    if repo_p_version > program_current:
        logger.info("Program version outdated! Updating program...")
        return True
    
    if repo_t_version > targets_current:
        logger.info("Target version outdated! Updating targets...")
        return True


if __name__ == "__main__":
    check_updates()