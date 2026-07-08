import requests, json
from config_manager import config, state, private
from datetime import datetime
from logger import logger

def _build_header():
    return (
                    f"```Userid: {config["user_id"]}\n" + 
                    f"Program Version: {state["program_version"]}\n" +
                    f"Target Version:{state["targets_version"]}\n" +
                    f"Event time: {datetime.now()}```"
                    )
    
def send_message(message, mention=False):
    payload =   {
                "content": _build_header() + message
                }
    
    if mention:
        owner_id = private["owner_discord_id"]
        payload["content"] = f"<@{owner_id}>\n{_build_header()}\n{message}"
        payload["allowed_mentions"] = {
            "users": [owner_id]
        }
    
    try:
        response = requests.post(
                                private["webhook"],
                                json=payload,
                                timeout=10
                            )
        if response.status_code == 204:
            logger.info("Webhook enviado com sucesso.")
            return True
        else:
            logger.error(
                f"Falha ao enviar webhook ({response.status_code}): {response.text}"
            )
            return False
        
    except requests.RequestException as e:
        logger.error(f"Erro ao contactar Discord: {e}")
        return False
    
def send_image(message, image, mention=False):

    payload = {
                "content": f"{_build_header()}\n {message}   \n\n   Screenshot:"
    }
    
    if mention:
        owner_id = private["owner_discord_id"]
        payload ["content"] = f"<@{owner_id}>\n{_build_header()}\n\n{message}\n\nScreenshot:"
        payload["allowed_mentions"] =   {
                                            "users": [owner_id]
                                        }

    try:
        response = requests.post(
                                private["webhook"],
                                data={
                                    "payload_json": json.dumps(payload)
                                },
                                files={
                                        "file": (
                                                    "screenshot.png",
                                                    image,
                                                    "image/png"
                                                )
                                },
                                timeout=10
                            )
            

        if response.ok:
            logger.info("Webhook enviado com sucesso.")
            return True
        else:
            logger.error(
                f"Falha ao enviar webhook ({response.status_code}): {response.text}"
            )
            return False
            
    except requests.RequestException as e:
        logger.error(f"Erro ao contactar Discord: {e}")
        return False
            