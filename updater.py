import requests
import json
from config_manager import state, private
from logger import logger

def version_tuple(v):
    return tuple(map(str, v.split(".")))

def check_updates():
    updates = dict()    
    response = requests.get(private["github_version"])
    repo_p_version = response.json()["program_version"]
    repo_t_version = response.json()["targets_version"]
    
    if version_tuple(repo_p_version) > version_tuple(state["program_version"]):
        logger.info("Versao do programa desactualizado! A actualizar programa...")
        updates["program"]=repo_p_version
    
    logger.info((repo_t_version))
    logger.info((state["targets_version"]))
    
    if version_tuple(repo_t_version) > version_tuple(state["targets_version"]):
        logger.info("Targets desactualizado! A actualizar targets...")
        updates["targets"]=repo_t_version
        
    if "program" in updates:
        #program_update()
        ...
    
    if "targets" in updates:
        #targets_update()
        ...
    
    print(updates)
    
    #    logger.info(f"Versao do programa actualizado! Estamos na versao {state["program_version"]}")
    #    logger.info(f"Versao dos targets actualizado! Estamos na versao {state["targets_version"]}")


if __name__ == "__main__":
    check_updates()