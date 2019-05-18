from bot import logger

from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    """Handles errors for Baguette bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Activates when an exception arises"""

        if hasattr(ctx.command, 'on_error'):
            return logger.debug("Exception found but handled by command's own error handler.")

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return logger.error(f"{str(ctx.author.id)} called the bot's prefix but no corresponding command located.")

        if isinstance(error, commands.MissingRequiredArgument):
            logger.error(f"{str(ctx.author.id)} invoked the command '{ctx.command.name}' but missed required "
                         f"arguments.")
            return await ctx.error(f"Required arguments missed. {self.bot.command_prefix}help <command> for indepth usage.")

        elif isinstance(error, commands.CheckFailure):
            logger.debug(f"{str(ctx.author.id)} invoked the command '{ctx.command.name}' but didn't meet the checks.")
            return await ctx.error("You do not meet the relevant checks inorder to invoke this command.")

        else:
            logger.error(f"Exception '{type(error).__name__}' raised in command when {ctx.author.id} invoked "
                         f"'{ctx.command}'")


def setup(bot):
    """Loads cog"""

    bot.add_cog(CommandErrorHandler(bot))