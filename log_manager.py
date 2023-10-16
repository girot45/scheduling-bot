import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="py_log.log",
    filemode="a"
)
logger = logging.getLogger(__name__)
