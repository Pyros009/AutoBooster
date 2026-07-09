import cv2
import numpy as np
import os
import random
from datetime import datetime
from logger import logger
from webhook import send_image, send_message
from debug import guardar_debug_match, guardar_debug_simples_resized
from config_manager import config, state

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
    
    #imagem_resized, scale_x, scale_y = resize_image(imagem_ecra)
    #imagem_resized, scale, pad_x, pad_y = letterbox(imagem_ecra)
    
    
    #guardar_debug_simples_resized(imagem_ecra,imagem_resized)
    
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
        #x, y, w, h = scale_rect(
        #                            melhor_match["max_loc"],
        #                            melhor_match["shape"],
        #                            scale_x,
        #                            scale_y
        #)
        
        #x, y, w, h = letterbox_rect(
        #                                melhor_match["max_loc"],
        #                                melhor_match["shape"],
        #                                scale,
        #                                pad_x,
        #                                pad_y
        #                            )
        
        h, w, _ = melhor_match['shape']
        max_loc = melhor_match['max_loc']
        ficheiro = melhor_match['ficheiro']
        
        x_min, x_max = max_loc[0] + 2, max_loc[0] + w - 2
        y_min, y_max = max_loc[1] + 2, max_loc[1] + h - 2
                
        #x_min = x + 2
        #x_max = x + w - 2

        #y_min = y + 2
        #y_max = y + h - 2
        
        if x_max <= x_min: x_max = x_min + 1
        if y_max <= y_min: y_max = y_min + 1
                  
        rand_x = random.randint(x_min, x_max)
        rand_y = random.randint(y_min, y_max)
        
        if config["debug"]:
            logger.info("Debug mode: a guardar imagem")
            ficheiro = guardar_debug_match(
                                            imagem_ecra,
                                            melhor_match["max_loc"],
                                            (h, w),
                                            x_min,
                                            y_min,
                                            x_max,
                                            y_max,
                                            ficheiro,
                                            maior_precisao,
                                            click=(rand_x, rand_y),
                                            output=f"debug/{ficheiro}.png"
                                        )
            logger.info(f"Imagem guardada em: {ficheiro}")
        
        logger.debug(
                        f"Click: ({rand_x}, {rand_y}) | "
                        f"Template: {ficheiro} | "
                        f"Score: {maior_precisao:.3f}"
                    )
        device.shell(f"input tap {rand_x} {rand_y}")
        return True
        
    return False

def enviar_screenshot_erro(imagem_ecra):
    logger.critical(f"Bot Travado. A enviar ecrã de falha para o discord.")
    sucesso, buffer = cv2.imencode(".png", imagem_ecra)
    if not sucesso:
        logger.error("Falha ao codificar imagem do erro!")
        send_message("User falhou codificacao da imagem de erro!")
        return False

    if send_image("🚨 Erro no anuncio!", buffer.tobytes(), mention=False):
        logger.info("Imagem enviada para o discord")
    else:
        send_message("O user nao conseguiu enviar imagem do erro!")
        
def resize_image(imagem):
    orig_h, orig_w = imagem.shape[:2]
    REFERENCE_WIDTH, REFERENCE_HEIGHT = map(int,state["targets_size"].split("x"))
    imagem_resize = cv2.resize(
                                imagem,
                                (REFERENCE_WIDTH, REFERENCE_HEIGHT),
                                interpolation=cv2.INTER_LINEAR
                            )
    
    scale_x = orig_w / REFERENCE_WIDTH
    scale_y = orig_h / REFERENCE_HEIGHT

    return imagem_resize, scale_x, scale_y

def scale_rect(max_loc, shape, scale_x, scale_y):
    x, y = max_loc
    h, w = shape[:2]

    x = int(round(x * scale_x))
    y = int(round(y * scale_y))

    w = int(round(w * scale_x))
    h = int(round(h * scale_y))

    return x, y, w, h

def letterbox(imagem):
    ref_w, ref_h = map(int, state["targets_size"].split("x"))

    h, w = imagem.shape[:2]

    # Escala uniforme
    scale = min(ref_w / w, ref_h / h)

    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    resized = cv2.resize(
        imagem,
        (new_w, new_h),
        interpolation=cv2.INTER_LINEAR
    )

    # Canvas preto
    canvas = np.zeros((ref_h, ref_w, 3), dtype=np.uint8)

    pad_x = (ref_w - new_w) // 2
    pad_y = (ref_h - new_h) // 2

    canvas[
        pad_y:pad_y + new_h,
        pad_x:pad_x + new_w
    ] = resized

    return canvas, scale, pad_x, pad_y

def letterbox_rect(max_loc, shape, scale, pad_x, pad_y):

    x, y = max_loc
    h, w = shape[:2]

    # Remove o padding
    x -= pad_x
    y -= pad_y
    
    x = max(0, x)
    y = max(0, y)

    # Converte para a resolução original
    x = int(round(x / scale))
    y = int(round(y / scale))

    w = int(round(w / scale))
    h = int(round(h / scale))

    return x, y, w, h