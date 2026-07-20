import requests
import json
from config_manager import state, private, save_state
from logger import logger
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import os
import subprocess
import sys

def version_tuple(v):
    return tuple(map(int, v.split(".")))

def validating_manager():
    import time
    url = private["github_version"] + f"?t={time.time_ns()}"
    response = requests.get(url)#private["github_version"])
    
    print(response.json()["program"]["version"])

def prog_updater(program_url, version):
    
    if getattr(sys, "frozen", False):
        APP_DIR = Path(sys.executable).parent
    else:
        APP_DIR = Path(__file__).resolve().parent
        
    TEMP_DIR = APP_DIR / ".updater"
    TEMP_DIR.mkdir(exist_ok=True)

    updater_path = TEMP_DIR / "program_updater.exe"
    
    try:
        response = requests.get(program_url, timeout = 60)
        
        response.raise_for_status()
    
        # escreve o zip file
        with updater_path.open("wb") as f:
            f.write(response.content)
                      
        logger.info("Updater descarregado...")
        
        subprocess.Popen([
                            str(updater_path),
                            "--pid",
                            str(os.getpid()),
                            "--app",
                            str(APP_DIR / "AutoBooster.exe"),
                            "--version",
                            version
                        ])

        sys.exit(0)

    except requests.RequestException as e:
        logger.error(f"Falha no download: {e}")
        return False   
    
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
        #prog_updater(repo_p["updater_url"], repo_p["version"])
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