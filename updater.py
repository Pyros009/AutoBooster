import requests
import json
from config_manager import state, private
from logger import logger

def version_tuple(v):
    return tuple(map(str, v.split(".")))

def validating_manager():
    import time
    url = private["github_version"] + f"?t={time.time_ns()}"
    response = requests.get(url)#private["github_version"])
    
    print(response.json()["program"]["version"])
    
def update_manager():
    updates = dict()
    
    import time
    url = private["github_version"] + f"?t={time.time_ns()}"
    response = requests.get(url)#private["github_version"])
    
    repo_p_version = response.json()["program"]["version"]
    repo_t_version = response.json()["targets"]["version"]
    
    logger.info("A validar a versao dos componentes.")
    
    if version_tuple(repo_p_version) > version_tuple(state["program_version"]):
        updates["program"]=repo_p_version
    
    if version_tuple(repo_t_version) > version_tuple(state["targets_version"]):
        updates["targets"]=repo_t_version
    
    if updates:
        logger.info(f"A actualizar os seguintes componentes: {', '.join(updates)}.")
    else: 
        logger.info("Os componentes estao todos actualizados.")
        
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
    update_manager()