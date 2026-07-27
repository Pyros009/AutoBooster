from logger import logger
import requests
import argparse
import sys
import psutil
from pathlib import Path

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
            
        #with ZipFile(zip_path, "r") as zip_ref:
        #    zip_ref.extractall(".")
            
        logger.info("Ficheiro descarregado e extraido...")
        
        # install
        ...        

    except requests.RequestException as e:
        logger.error(f"Falha no download: {e}")
        return False
    
    #finally:
    #    # limpa as pastas temporarias
    #    if zip_path.exists():
    #        zip_path.unlink()    
    #        
    #    if TEMP_DIR.exists():
    #        TEMP_DIR.rmdir()

    logger.info("Versao nova do programa descarregada.")
    return True        
######################

parser = argparse.ArgumentParser()

parser.add_argument("--pid", type=int, required=True)
parser.add_argument("--app", required=True)
parser.add_argument("--updater_exec", required=True)

args = parser.parse_args()


# 1. Esperar que o AutoBooster termine
parent_pid = args.pid
if not wait_for_process(args.pid):
    sys.exit(1)

release_url = args.updater_exec
download_install_version(release_url)

# 4. Reiniciar o AutoBooster

app_path = args.app
