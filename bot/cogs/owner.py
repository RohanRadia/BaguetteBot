from bot import logger
from discord.ext import commands


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("sd", "shutdown", "lo"))
    @commands.is_owner()
    async def logout(self, ctx):
        """Logout of bot"""

        await self.bot.http_session.close()

        await ctx.send("`Bot logging out... closing connections.`")
        logger.info("Logged out - all connections closed.")
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """Load a cog"""

        self.bot.load_extension(cog)
        logger.info(f"Successfully loaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully loaded.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """Unload a cog"""

        self.bot.unload_extension(cog)
        logger.info(f"Successfully unloaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully unloaded.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reload a cog"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            logger.error(f"Attempted to unload cog: {cog} which was never loaded on start up. Bypassing and attempting "
                         f"to complete function.")

        self.bot.load_extension(cog)

        logger.info(f"Successfully reloaded extension: {cog}")
        await ctx.send(f"`{cog}` successfully reloaded.")


def setup(bot):
    bot.add_cog(Owners(bot))
