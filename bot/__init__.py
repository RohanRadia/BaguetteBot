import os
from glob import glob
import socket

from loguru import logger
from pathlib import Path
from aiohttp import AsyncResolver, ClientSession, TCPConnector

logger.add(Path("bot", "logs", "info.log"), level="INFO", enqueue=True)
logger.add(Path("bot", "logs", "debug.log"), level="DEBUG", enqueue=True)
logger.add(Path("bot", "logs", "error.log"), level="ERROR", enqueue=True)


def aiohttpSession():
    """Aiohttp session creator"""

    return ClientSession(connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET))


def getcogs():
    """Get all files in a directory"""
    cogs = []
    generator = Path("bot", "cogs").glob('*.py')

    for cog in generator:
        cogs.append(os.path.splitext(os.path.basename(cog))[0])

    return cogs
