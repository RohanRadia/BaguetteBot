import os
from bot import logger
from datetime import datetime

from discord.ext import commands
from utils.custom_context import BaguetteContext

cogs = ["cogs.errorhandler", "cogs.owner", "cogs.coding"]


class Baguette(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='?',
                         description='A bot made for the personal use of TheMutantReaper#3615 but all of you randoms '
                                     'can use it too!')

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=BaguetteContext)
        await self.invoke(ctx)

    async def on_ready(self):
        for cog in cogs:
            try:
                self.load_extension(cog)
                logger.info(f'Successfully loaded extension: {cog}')
            except Exception as e:
                logger.error(f'Failed to load extension: {cog}\n{e}')

        logger.info(f'Client Logged in at {datetime.now()}')

    def run(self):
        super().run(os.environ.get('TOKEN'), reconnect=True)


if __name__ == '__main__':
    bot = Baguette()
    bot.run()