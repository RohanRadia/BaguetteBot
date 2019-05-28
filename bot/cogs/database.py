from bot import logger
from bot import postgresexecute, postgresfetch
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await postgresexecute(f"""INSERT INTO server_info(server_id, prefix) VALUES({guild.id}, 'b!')""")
        logger.info(f"Bot joined guild: {guild.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await postgresexecute(f"""DELETE FROM server_info WHERE server_id={guild.id}""")
        logger.info(f"Bot joined left: {guild.id}")

    @commands.group(name="pg", invoke_without_command=False)
    @commands.is_owner()
    async def pg(self, ctx):
        pass

    @pg.command()
    @commands.is_owner()
    async def execute(self, ctx, *, query):
        try:
            await postgresexecute(f"""{query}""")
            await ctx.message.add_reaction('\U00002705')
        except:
            await ctx.message.add_reaction('\U0000274c')

    @pg.command()
    @commands.is_owner()
    async def fetch(self, ctx, *, query):
        try:
            data = await postgresfetch(f"""{query}""")
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(f"```\n{data}```")
        except Exception as e:
            await ctx.message.add_reaction('\U0000274c')


def setup(bot):
    bot.add_cog(Database(bot))
