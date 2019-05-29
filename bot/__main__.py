import os
import time
from bot import logger, aiohttpSession, getcogs, postgresconn
from datetime import datetime

import asyncpg
import discord
from discord.ext import commands
from utils.custom_context import BaguetteContext

cogs = []

for cog in getcogs("cogs"):
    cogs.append(cog)

for cog in getcogs("utility_cogs"):
    cogs.append(cog)


async def prefix(client, message):
    conn = await asyncpg.connect(host=os.environ['PG_HOST'],
                                 user=os.environ['PG_USER'],
                                 password=os.environ['PG_PASS'],
                                 database=os.environ['PG_DB'])

    data = await conn.fetch(f"""SELECT * FROM server_info WHERE server_id={message.guild.id}""")

    await conn.close()

    if dict(data).get(message.guild.id) is None:
        return 'b!'

    return data[0][1]


class Baguette(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=prefix,
                         description='A bot made for the personal use of TheMutantReaper#3615 but all of you randoms '
                                     'can use it too!')
        self.http_session = aiohttpSession()
        self.gold = 0xF9A602
        self.launch_time = time.time()
        self.message_interval = 0
        self.message_count = 0

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=BaguetteContext)
        await self.invoke(ctx)

    async def on_ready(self):
        self.connpool = await postgresconn()

        for cog in cogs:
            try:
                self.load_extension(cog)
                logger.info(f'Successfully loaded extension: {cog}')
            except Exception as e:
                logger.error(f'Failed to load extension: {cog}\n{e}')

        self.load_extension('jishaku')

        logger.info(f'Client Logged in at {datetime.now()}')

        await self.change_presence(activity=discord.Game(name=f"Shard {str(self.shard_count)} | "
        f"{str(len(self.guilds))} Guilds"))

        conn = await self.connpool.acquire()
        message_count = await conn.fetch('''SELECT messages_handled FROM bot_stats WHERE user_id=579399080799633448''')
        self.message_count = int(message_count[0][0])
        await self.connpool.release(conn)

    def run(self):
        super().run(os.environ.get('TOKEN'), reconnect=True)


if __name__ == '__main__':
    bot = Baguette()
    bot.run()