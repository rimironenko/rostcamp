import logging

# Configure logger
logger = logging.getLogger("llm_app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)
