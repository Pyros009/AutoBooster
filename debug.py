import cv2
from pathlib import Path

def guardar_debug_match(imagem,max_loc,shape,x_min,y_min,x_max,y_max,ficheiro,score,click=None,output="debug.png"):

    debug = imagem.copy()
    h, w = shape[:2]
    x, y = max_loc

    # 1. Retângulo do template encontrado (verde)
    cv2.rectangle(
        debug,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    # 2. Zona onde o clique pode ser escolhido (azul)
    cv2.rectangle(
        debug,
        (x_min, y_min),
        (x_max, y_max),
        (255, 0, 0),
        2
    )

    # 3. Clique efetivo (vermelho)
    if click:
        cv2.circle(
            debug,
            click,
            5,
            (0, 0, 255),
            -1
        )
        
    cv2.putText(
                debug,
                f"{ficheiro} | {score*100:.1f}%",
                (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
                )
            
    cv2.imwrite(output, debug)
    
    return output

def guardar_debug_simples_resized(imagem,resized,output1="debug_simple.png",output2="debug_simple_resized.png"):
            
    cv2.imwrite(output1, imagem)
    cv2.imwrite(output2, resized)
    
    return output1, output2