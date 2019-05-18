import discord
from discord.ext import commands


class BaguetteContext(commands.Context):
    async def error(self, err: str, delete_after=None):
        em = discord.Embed(title=':x: Error',
                           color=discord.Color.dark_red(),
                           description=err.format())

        await self.send(embed=em, delete_after=delete_after)