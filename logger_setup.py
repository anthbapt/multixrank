import logging

logger = logging.getLogger("multixrank")
handler = logging.StreamHandler()
formatter_str = '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'
formatter_obj = logging.Formatter(formatter_str)
handler.setFormatter(formatter_obj)
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # set root's level
