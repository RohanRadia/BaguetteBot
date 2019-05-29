import time
from datetime import timedelta

import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("ping", "pong", "lat", "latency", "uptime", "up"))
    async def stats(self, ctx):
        users = 0
        for user in self.bot.get_all_members():
            users = users + 1

        time_difference = time.time() - self.bot.launch_time
        hours, rem = divmod(int(time_difference), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        uptime = f'{days}D {hours}H {minutes}M {seconds}S'

        emb = discord.Embed(colour=self.bot.gold, title=f"Shard {self.bot.shard_count} Stats")

        emb.add_field(name='Guilds \U00002694', value=str(len(self.bot.guilds)))
        emb.add_field(name='Users \U0001f642', value=str(users))
        emb.add_field(name='Ping \U0001f3d3', value=str(round(self.bot.latency*100, 2)))
        emb.add_field(name='Uptime \U0001f550', value=uptime)
        emb.add_field(name='Cogs \U00002699 ', value=str(len(self.bot.cogs)))
        emb.add_field(name='Commands \U0001f50e ', value=str(len(self.bot.commands)))
        emb.add_field(name='Messages \U0001f4e5', value=self.bot.message_count)

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Misc(bot))