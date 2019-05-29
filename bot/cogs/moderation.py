import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='prefix', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx):
        conn = await self.bot.connpool.acquire()

        data = await conn.fetch(f"SELECT prefix FROM server_info WHERE server_id={ctx.guild.id}")

        await self.bot.connpool.release(conn)

        emb = discord.Embed(colour=self.bot.gold)
        emb.add_field(name='Prefix', value=f"{data[0][0]}")
        await ctx.send(embed=emb)

    @prefix.command(aliases=["change", "modify", "set"])
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, prefix: str):
        conn = await self.bot.connpool.acquire()

        await conn.execute(f"UPDATE server_info SET prefix='{prefix}' WHERE server_id={ctx.guild.id}")
        data = await conn.fetch(f"SELECT prefix FROM server_info WHERE server_id={ctx.guild.id}")

        await self.bot.connpool.release(conn)

        emb = discord.Embed(colour=self.bot.gold)
        emb.add_field(name='Prefix', value=f"{data[0][0]}")
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(ban=True)
    async def ban(self, ctx):
        ctx.ban()


def setup(bot):
    bot.add_cog(Moderation(bot))
