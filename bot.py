from adb_manager import find_adb, connect_emulator, connect
from vision import capturar_ecra_bg, procurar_template, procurar_e_clicar_qualquer, enviar_screenshot_erro
import time
from config_manager import config, random_timer, private
from logger import logger
import sys

def rodar_bot():
    
    path = find_adb()
    
    if path is None:
        logger.critical("A inicializacao foi interrompida!")
        sys.exit(1)    
        
    if not connect_emulator(path):
        logger.critical("A inicializacao foi interrompida!")
        sys.exit(1)
    
    device = connect()
    
    if device is None:
        logger.critical("A inicializacao foi interrompida!")
        sys.exit(1)
        
    logger.info("Bot inicializado!.")

    
    detect = config["matching"]["deteccao"]
    click = config["matching"]["click"]
    failed_matches = 0

    while True:
        try:
            ecra = capturar_ecra_bg(device)
        except RuntimeError:
            logger.warning("Ligação ADB perdida. A tentar reconectar...")
            time.sleep(5)
            device = connect()
            continue
        
        if ecra is None:
            time.sleep(2)
            continue
        
        logger.info(f"Screenshot shape: {ecra.shape}")
        no_lobby = procurar_template(ecra, "targets/lobby.png", precisao=detect)

        if no_lobby:
            logger.info("[Step 1] Confirmado: Estamos no Lobby.")

            em_cooldown = procurar_template(ecra, "targets/cooldown_ativo.png", precisao=detect)
            runtime_full = procurar_template(ecra, "targets/runtime_full.png", precisao=detect)
            
            if runtime_full:
                logger.info("Runtime full. Bot parado!")
                time.sleep(3)
                break
            
            if em_cooldown:
                tempo_cooldown = random_timer("cooldown")
                logger.info(f"[Step 2] Cooldown ativo. A dormir {tempo_cooldown // 60} minutos...")
                time.sleep(tempo_cooldown)
                continue
            else:
                logger.info("[Step 2] Sem Cooldown detetado. Pronto para avançar.")

                logger.info("[Step 3] A tentar clicar no Boost...")
                if procurar_e_clicar_qualquer(device, ecra, pasta_templates="targets", precisao=click):
                    tempo_anuncio = random_timer("anuncio")
                    logger.info(f"Boost clicado! A aguardar {tempo_anuncio}s para o anúncio correr...")
                    time.sleep(tempo_anuncio)
                    failed_matches = 0 
                else:
                    logger.warning("Falha ao clicar no botão Boost (Padrão não encontrado no Lobby).")
                    time.sleep(5)
                continue

        else:
            logger.info(f"[Step 4] Anúncio Ativo detetado.")
            
            if failed_matches < config["tolerancia"]:
                if procurar_e_clicar_qualquer(device, ecra, pasta_templates="targets", precisao=click):
                    tempo_transicao = random_timer("espera")
                    logger.info(f"Padrão de fecho acionado! Aguarda {tempo_transicao}s pela próxima fase/ecrã...")
                    time.sleep(tempo_transicao)
                    failed_matches = 0 
                    continue 
                else:
                    tempo_espera_extra = random_timer("espera_botao")
                    failed_matches += 1
                    logger.warning(f"Nenhum padrão visível (Tentativa {failed_matches}/{config['tolerancia']}). Aguarda {tempo_espera_extra}s para o botão aparecer...")
                    time.sleep(tempo_espera_extra)
                    continue
            else:
                logger.error("Anúncio bloqueado ou padrão novo detetado!")
                if private.get("discord_integration", False):
                    enviar_screenshot_erro(ecra)
                time.sleep(5)
                
                break
