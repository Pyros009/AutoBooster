import requests
import json
from config_manager import state, private, save_state
from logger import logger
from pathlib import Path
from zipfile import ZipFile, BadZipFile


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
    
    response_json = response.json()
    
    repo_p = response_json["program"]
    repo_t = response_json["targets"]
    
    logger.info("A validar a versao dos componentes.")
    
    if version_tuple(repo_p["version"]) > version_tuple(state["program_version"]):
        updates["program"]=repo_p["version"]
    
    if version_tuple(repo_t["version"]) > version_tuple(state["targets_version"]):
        updates["targets"]=repo_t["version"]
    
    if updates:
        logger.info(f"A actualizar os seguintes componentes: {', '.join(updates)}.")
    else: 
        logger.info("Os componentes estao todos actualizados.")
        
    if "program" in updates:
        #program_update()
        ...
    
    if "targets" in updates:
        targets_update(repo_t)
        ...
        
    #    logger.info(f"Versao do programa actualizado! Estamos na versao {state["program_version"]}")
    #    logger.info(f"Versao dos targets actualizado! Estamos na versao {state["targets_version"]}")

def targets_update(targets):
    
    TEMP_DIR = Path("temp")
    TEMP_DIR.mkdir(exist_ok=True)
    
    zip_path = TEMP_DIR / "targets.zip"
    
    zip_url = targets["url"]
    
    c_version = targets["version"]
    
    o_version = state["targets_version"]

    response = requests.get(zip_url)

    if response.status_code != 200:
        logger.error("Falha ao descarregar os targets.")
        return False
    
    try: 
        with zip_path.open("wb") as f:
            f.write(response.content)
        
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")

        logger.info("Novos targets descarregados")
        
    except BadZipFile:
        logger.error("O ficheiro descarregado não é um ZIP válido.")
        return False
    
    finally:
        if zip_path.exists():
            zip_path.unlink()    
            
        if TEMP_DIR.exists():
            TEMP_DIR.rmdir()
        
    state["targets_version"]=c_version
    save_state()
    
    logger.info(f"Targets atualizados: {o_version} -> {c_version}")

    return True

def program_update(program):
    
    TEMP_DIR = Path("temp")
    TEMP_DIR.mkdir(exist_ok=True)
    
    zip_path = TEMP_DIR / "program.zip"
    
    zip_url = program["url"]
    
    c_version = program["version"]
    
    o_version = state["program_version"]

    response = requests.get(zip_url)

    if response.status_code != 200:
        logger.error("Falha ao descarregar o programa.")
        return False
    
    try: 
        with zip_path.open("wb") as f:
            f.write(response.content)
        
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")

        logger.info("Versao nova do programa descarregada.")
        
    except BadZipFile:
        logger.error("O ficheiro descarregado não é um ZIP válido.")
        return False
    
    finally:
        if zip_path.exists():
            zip_path.unlink()    
            
        if TEMP_DIR.exists():
            TEMP_DIR.rmdir()
        
    state["program_version"]=c_version
    save_state()
    
    logger.info(f"Programa atualizado: {o_version} -> {c_version}")

    return True