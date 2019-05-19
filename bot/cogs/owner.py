import json
import os

from bot import logger
import discord
from discord.ext import commands
from pathlib import Path


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("sd", "shutdown", "lo"))
    async def logout(self, ctx):
        """Logout of bot"""

        await self.bot.http_session.close()

        await ctx.send("`Bot logging out... closing connections.`")
        logger.info("Logged out - all connections closed.")
        await self.bot.logout()

    @commands.command()
    async def load(self, ctx, cog: str):
        """Load a cog"""

        self.bot.load_extension(cog)
        logger.info(f"Successfully loaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully loaded.")

    @commands.command()
    async def unload(self, ctx, cog: str):
        """Unload a cog"""

        self.bot.unload_extension(cog)
        logger.info(f"Successfully unloaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully unloaded.")

    @commands.command()
    async def reload(self, ctx, cog: str):
        """Reload a cog"""

        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        logger.info(f"Successfully reloaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully reloaded.")

    @commands.command()
    async def test(self, ctx):
        with open(Path("bot", "resources", "commandPerms.json"), 'r', encoding="utf8") as f:
            perms = json.load(f)

        for command in self.bot.commands:
            if str(command) not in perms:
                perms[str(command)] = []

        with open(Path("bot", "resources", "commandPerms.json"), 'w', encoding="utf8") as f:
            json.dump(perms, f)

    @commands.group(name="perms", invoke_without_command=True)
    async def perms(self, ctx):
        with open(Path("bot", "resources", "commandPerms.json"), 'r', encoding="utf8") as f:
            perms = json.load(f)

        emb = discord.Embed(colour=discord.Colour.gold(), title="Command Permissions")
        for command in perms:
            emb.add_field(name=command.title(), value=["Public" if 0 in perms[command] else "Authorised Only"][0])
        await ctx.send(embed=emb)

    @perms.command()
    async def add(self, ctx, command, user: discord.Member = 0):
        with open(Path("bot", "resources", "commandPerms.json"), 'r', encoding="utf8") as f:
            perms = json.load(f)

        if user != 0:
            if user.id not in perms[command]:
                perms[command].append(user.id)
        else:
            perms[command].append(0)

        with open(Path("bot", "resources", "commandPerms.json"), 'w', encoding="utf8") as f:
            json.dump(perms, f)

        if user == 0:
            await ctx.send(f"`{command.title()}` made public.")
        else:
            await ctx.send(f"`{command.title()}` added to `{str(user.id)}`")

    @perms.command()
    async def remove(self, ctx, command, user: discord.Member = 0):
        with open(Path("bot", "resources", "commandPerms.json"), 'r', encoding="utf8") as f:
            perms = json.load(f)

        if user != 0:
            if user.id in perms[command]:
                perms[command].remove(user.id)
        else:
            perms[command].remove(0)

        with open(Path("bot", "resources", "commandPerms.json"), 'w', encoding="utf8") as f:
            json.dump(perms, f)

        if user == 0:
            await ctx.send(f"`{command.title()}` made private.")
        else:
            await ctx.send(f"`{command.title()}` removed from `{str(user.id)}`")

    async def bot_check(self, ctx):
        with open(Path("bot", "resources", "commandPerms.json"), 'r', encoding="utf8") as f:
            perms = json.load(f)

        if ctx.command.name not in perms:
            perms[ctx.command.name] = []
            with open(Path("bot", "resources", "commandPerms.json"), 'w', encoding="utf8") as f:
                json.dump(perms, f)

        if ctx.author.id == int(os.environ.get("OWNER")):
            return True

        if 0 in perms[ctx.command.name]:
            return True

        if ctx.author.id in perms[ctx.command.name]:
            return True

        return False


def setup(bot):
    bot.add_cog(Owners(bot))
