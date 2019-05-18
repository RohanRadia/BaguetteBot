from bot import logger
from discord.ext import commands


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("sd", "shutdown", "lo"))
    async def logout(self, ctx):
        """Logout of bot"""

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


def setup(bot):
    bot.add_cog(Owners(bot))
    logger.info('Owners Cog Loaded!')