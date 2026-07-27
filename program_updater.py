from logger import logger
import requests
import argparse
import sys
import psutil
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import shutil
import subprocess


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

def download_install_version(url, app_dir):
    # cria uma temp folder
    TEMP_DIR = app_dir / "temp"
    TEMP_DIR.mkdir(exist_ok=True)

    # cria o zip file
    zip_path = TEMP_DIR / "program.zip"
    
    # cria a pasta de extraccao
    EXTRACT_DIR = TEMP_DIR / "extracted"
    EXTRACT_DIR.mkdir(exist_ok=True)
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        # escreve o zip file
        with zip_path.open("wb") as f:
            f.write(response.content)
            
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
            
        logger.info("Ficheiro descarregado e extraido...")
        
        NEW_APP_DIR = EXTRACT_DIR / "AutoBooster"
        
        new_exe = NEW_APP_DIR / "AutoBooster.exe"
        new_internal = NEW_APP_DIR / "_internal"
        
        old_exe = app_dir / "AutoBooster.exe"
        old_internal = app_dir / "_internal"
        
        if not new_exe.exists():
            logger.error("O AutoBooster.exe não foi encontrado no ZIP.")
            return False
        
        if not new_internal.exists():
            logger.error("A pasta _internal não foi encontrada no ZIP.")
            return False
        
        shutil.copy2(
            new_exe,
            old_exe
        )

        if old_internal.exists():
            shutil.rmtree(old_internal)
            
        shutil.copytree(
                            new_internal,
                            old_internal
                        )
        
        logger.info("Nova versão instalada.")
        return True
    
    except BadZipFile:
        logger.error("O ficheiro descarregado não é um ZIP válido.")
        return False  
    
    except requests.RequestException as e:
        logger.error(f"Falha no download: {e}")
        return False

    except OSError as e:
        logger.error(f"Falha durante a instalação: {e}")
        return False
    
    finally:
        # limpa os temporarios           
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            logger.info("Ficheiros temporários removidos.")
    
######################

parser = argparse.ArgumentParser()

parser.add_argument("--pid", type=int, required=True)
parser.add_argument("--app", required=True)
parser.add_argument("--url", required=True)

args = parser.parse_args()

app_path = Path(args.app)
app_dir = app_path.parent

# 1. Esperar que o AutoBooster termine
if not wait_for_process(args.pid):
    sys.exit(1)

if not download_install_version(args.url, app_dir):
    logger.error("A atualização falhou. A iniciar a versão atual.")
    subprocess.Popen(
                    [str(app_path)],
                    cwd=app_dir
                )
    sys.exit(1)
    
logger.info("Atualização concluída. A iniciar a nova versão.")

subprocess.Popen(
    [str(app_path)],
    cwd=app_dir
)

sys.exit(0)    
