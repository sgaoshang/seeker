import logging, sys
logger = logging.getLogger('seaker_logger')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)
