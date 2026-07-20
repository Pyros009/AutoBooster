from logger import logger
import json
import requests
import time
from config_manager import save_state, state, private ## private para debug only
import argparse
import sys
import time
import os
import psutil
from pathlib import Path
from zipfile import ZipFile, BadZipFile

def version_tuple(v):
    return tuple(map(int, v.split(".")))

def wait_for_process(pid, timeout=30):
    try:
        process = psutil.Process(pid)
        process.wait(timeout=timeout)

    except psutil.TimeoutExpired:
        logger.error("O processo principal não terminou dentro do tempo limite.")
        return False

    except psutil.NoSuchProcess:
        pass

    return True

def download_install_version(url):
    # cria uma temp folder
    TEMP_DIR = Path("temp")
    TEMP_DIR.mkdir(exist_ok=True)

    # cria o zip file
    zip_path = TEMP_DIR / "program.zip"
    
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Falha ao descarregar o programa.")
        return False
    
    try: 
        # escreve o zip file
        with zip_path.open("wb") as f:
            f.write(response.content)
            
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")
            
        logger.info("Ficheiro descarregado e extraido...")
        
        ...        

    except BadZipFile:
        logger.error("O ficheiro descarregado não é um ZIP válido.")
        return False

    except requests.RequestException as e:
        logger.error(f"Falha no download: {e}")
        return False
    
    finally:
        # limpa as pastas temporarias
        if zip_path.exists():
            zip_path.unlink()    
            
        if TEMP_DIR.exists():
            TEMP_DIR.rmdir()

    logger.info("Versao nova do programa descarregada.")
    return True        
######################

parser = argparse.ArgumentParser()

parser.add_argument("--pid", type=int, required=True)
parser.add_argument("--app", required=True)
parser.add_argument("--version", required=True)

args = parser.parse_args()


# 1. Esperar que o AutoBooster termine
parent_pid = args.pid
if not wait_for_process(args.pid):
    sys.exit(1)


# 2. Consultar versão/download -- a versao e o url vem do codigo, isto é debug only
# get url - temp usado para correr o program_updater em standalone
url = private["github_version"] + f"?t={time.time_ns()}"
response = requests.get(url)#private["github_version"])
new_version = response.json()["program"]["version"] ## args.version

current_version = state["program_version"]

logger.info(f"Versao actual: {current_version}.\nVersão encontrada: {new_version}.")

if version_tuple(new_version) > version_tuple(current_version):
    logger.info(f"Nova versão encontrada, a actualizar...")
else:
    logger.info(f"Versao actual é a mais recente...")
    sys.exit(1)

# 3. Preparar a extraccao e download do ZIP + instalar
#app_url = args.url

# temp url
release_url = (
    private["github_releases"]
    + f"v{new_version}/AutoBooster.zip"
)

download_install_version(release_url)

# 4. Reiniciar o AutoBooster

app_path = args.app

def program_update(url, o_version, n_version):
    
    
        
        
            

               
    state["program_version"]=n_version
    save_state()
    
    logger.info(f"Programa atualizado: {o_version} -> {n_version}")

    return True
