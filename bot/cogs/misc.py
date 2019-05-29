import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("ping", "pong", "lat", "stats"))
    async def latency(self, ctx):
        emb = discord.Embed(colour=self.bot.gold)
        emb.add_field(name='Ping', value=str(round(self.bot.latency*100, 2)))
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Misc(bot))