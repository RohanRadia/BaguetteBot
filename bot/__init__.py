import os
import socket

import asyncpg
from loguru import logger
from pathlib import Path
from aiohttp import AsyncResolver, ClientSession, TCPConnector

logger.add(Path("bot", "logs", "info.log"), level="INFO", enqueue=True)
logger.add(Path("bot", "logs", "debug.log"), level="DEBUG", enqueue=True)
logger.add(Path("bot", "logs", "error.log"), level="ERROR", enqueue=True)


def aiohttpSession():
    """Aiohttp session creator"""

    return ClientSession(connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET))


def getcogs(path: str):
    """Get all files in a directory"""
    cogs = []
    generator = Path("bot", path).glob('*.py')

    for cog in generator:
        cogs.append(f"{path}.{os.path.splitext(os.path.basename(cog))[0]}")

    return cogs


async def postgresconn():
    return await asyncpg.create_pool(host=os.environ['PG_HOST'],
                                     user=os.environ['PG_USER'],
                                     password=os.environ['PG_PASS'],
                                     database=os.environ['PG_DB'])
