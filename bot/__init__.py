from loguru import logger
from pathlib import Path

logger.add(Path("bot", "logs", "info.log"), level="INFO", enqueue=True)
logger.add(Path("bot", "logs", "debug.log"), level="DEBUG", enqueue=True)
logger.add(Path("bot", "logs", "error.log"), level="ERROR", enqueue=True)