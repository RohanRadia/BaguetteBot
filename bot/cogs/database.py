from bot import logger
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        conn = await self.bot.connpool.acquire()

        await conn.execute(f"""INSERT INTO server_info(server_id, prefix) VALUES({guild.id}, 'b!')""")

        await self.bot.connpool.release(conn)
        logger.info(f"Bot joined guild: {guild.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        conn = await self.bot.connpool.acquire()

        await conn.execute(f"""DELETE FROM server_info WHERE server_id={guild.id}""")

        await self.bot.connpool.release(conn)
        logger.info(f"Bot left guild: {guild.id}")

    @commands.group(name="pg", invoke_without_command=False)
    @commands.is_owner()
    async def pg(self, ctx):
        pass

    @pg.command()
    @commands.is_owner()
    async def execute(self, ctx, *, query):
        conn = await self.bot.connpool.acquire()

        try:
            await conn.execute(f"""{query}""")
            await ctx.message.add_reaction('\U00002705')
            logger.info(f"Successfully executed query: '{query}' on PG DB")
        except Exception as e:
            await ctx.message.add_reaction('\U0000274c')
            logger.error(f"Failed execute of query: '{query}' on PG DB - Error: {e}")
        finally:
            await self.bot.connpool.release(conn)

    @pg.command()
    @commands.is_owner()
    async def fetch(self, ctx, *, query):
        conn = await self.bot.connpool.acquire()

        try:
            data = await conn.fetch(f"""{query}""")
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(f"```\n{data}```")
            logger.info(f"Successfully executed fetch: '{query}' on PG DB")
        except Exception as e:
            await ctx.message.add_reaction('\U0000274c')
            logger.error(f"Failed execute of fetch: '{query}' on PG DB - Error: {e}")
        finally:
            await self.bot.connpool.release(conn)


def setup(bot):
    bot.add_cog(Database(bot))
