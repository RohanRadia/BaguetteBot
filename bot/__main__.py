import os
from bot import logger, aiohttpSession, getcogs
from datetime import datetime

import discord
from discord.ext import commands
from utils.custom_context import BaguetteContext

cogs = getcogs()


class Baguette(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='d!',
                         description='A bot made for the personal use of TheMutantReaper#3615 but all of you randoms '
                                     'can use it too!')
        self.http_session = aiohttpSession()

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=BaguetteContext)
        await self.invoke(ctx)

    async def on_ready(self):
        for cog in cogs:
            try:
                self.load_extension(f"cogs.{cog}")
                logger.info(f'Successfully loaded extension: {cog}')
            except Exception as e:
                logger.error(f'Failed to load extension: {cog}\n{e}')

        logger.info(f'Client Logged in at {datetime.now()}')

        await self.change_presence(activity=discord.Game(name=f"Shard {str(self.shard_count)}"))

    def run(self):
        super().run(os.environ.get('TOKEN'), reconnect=True)


if __name__ == '__main__':
    bot = Baguette()
    bot.run()