import socket

from loguru import logger
from pathlib import Path
from aiohttp import AsyncResolver, ClientSession, TCPConnector

logger.add(Path("bot", "logs", "info.log"), level="INFO", enqueue=True)
logger.add(Path("bot", "logs", "debug.log"), level="DEBUG", enqueue=True)
logger.add(Path("bot", "logs", "error.log"), level="ERROR", enqueue=True)


def aiohttpSession():
    """aiohttp session creator"""
    return ClientSession(connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET))
