import cv2
import numpy as np
import os
import random
from datetime import datetime
from logger import logger
from webhook import send_image, send_message

def capturar_ecra_bg(device, salvar_imagem=False):
    image_bytes = device.screencap()
    if not image_bytes:
        return None
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if salvar_imagem and img is not None:
        cv2.imwrite("teste_captura.png", img)
    return img

def procurar_template(imagem_ecra, caminho_template, precisao=0.75):
    """Apenas verifica se uma imagem existe no ecrã (Retorna True/False)"""
    template = cv2.imread(caminho_template, cv2.IMREAD_COLOR)
    if template is None:
        return False
    resultado = cv2.matchTemplate(imagem_ecra, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(resultado)
    return max_val >= precisao

def procurar_e_clicar_qualquer(device, imagem_ecra, pasta_templates="targets", precisao=0.75):
    """Procura padrões numa pasta e clica no que tiver a maior percentagem de match"""
    if not os.path.exists(pasta_templates):
        os.makedirs(pasta_templates)
        
    melhor_match = None
    maior_precisao = precisao

    for ficheiro in os.listdir(pasta_templates):
        if "lobby" in ficheiro or "cooldown" in ficheiro:
            continue
            
        caminho_completo = os.path.join(pasta_templates, ficheiro)
        template = cv2.imread(caminho_completo, cv2.IMREAD_COLOR)
        if template is None:
            continue
            
        resultado = cv2.matchTemplate(imagem_ecra, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)
        
        if max_val > maior_precisao:
            maior_precisao = max_val
            melhor_match = {
                'ficheiro': ficheiro,
                'max_loc': max_loc,
                'shape': template.shape
            }
            
    if melhor_match:
        h, w, _ = melhor_match['shape']
        max_loc = melhor_match['max_loc']
        ficheiro = melhor_match['ficheiro']
        
        x_min, x_max = max_loc[0] + 2, max_loc[0] + w - 2
        y_min, y_max = max_loc[1] + 2, max_loc[1] + h - 2
        
        if x_max <= x_min: x_max = x_min + 1
        if y_max <= y_min: y_max = y_min + 1
        
        rand_x = random.randint(x_min, x_max)
        rand_y = random.randint(y_min, y_max)
        
        logger.info(f"[+] Melhor padrão detetado: '{ficheiro}' ({maior_precisao*100:.1f}%).")
        device.shell(f"input tap {rand_x} {rand_y}")
        return True
        
    return False

def enviar_screenshot_erro(imagem_ecra):
    logger.critical(f"[!!!] Bot Travado. A enviar ecrã de falha para o discord.")
    sucesso, buffer = cv2.imencode(".png", imagem_ecra)
    if not sucesso:
        logger.error("Falha ao codificar imagem do erro!")
        send_message("User falhou codificacao da imagem de erro!")
        return False
    
    files = {
                "file": (
                    "screenshot.png",
                    buffer.tobytes(),
                    "image/png"
                )
            }
    if send_image("🚨 Erro no anuncio!", files, mention=False):
        logger.info("Imagem enviada para o discord")
    else:
        send_message("O user nao conseguiu enviar imagem do erro!")