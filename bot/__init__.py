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


def getcogs():
    """Get all files in a directory"""
    cogs = []
    generator = Path("bot", "cogs").glob('*.py')

    for cog in generator:
        cogs.append(os.path.splitext(os.path.basename(cog))[0])

    return cogs


async def postgresconn():
    return await asyncpg.connect(host=os.environ['PG_HOST'],
                           user=os.environ['PG_USER'],
                           password=os.environ['PG_PASS'],
                           database=os.environ['PG_DB'])


async def postgresexecute(query):
    conn = await postgresconn()
    try:
        await conn.execute(query)
        return True
    except Exception as e:
        logger.error(f"Error occured when accessing PG DB: {e}")
        return False
    finally:
        await conn.close()


async def postgresfetch(query):
    conn = await postgresconn()
    try:
        data = await conn.fetch(query)
        return data
    except Exception as e:
        logger.error(f"Error occured when accessing PG DB: {e}")
        return False
    finally:
        await conn.close()


async def prefix(client, message):
    data = await postgresfetch(f"""SELECT * FROM server_info WHERE server_id={message.guild.id}""")
    return dict(data).get(message.guild.id)
