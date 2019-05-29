from discord.ext import commands


class _Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        conn = await self.bot.connpool.acquire()
        message_count = await conn.fetch('''SELECT messages_handled FROM bot_stats WHERE user_id=579399080799633448''')
        self.bot.message_count = int(message_count[0][0])
        self.bot.message_interval = 0
        await self.bot.connpool.release(conn)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.bot.message_interval += 1
        self.bot.message_count += 1

        if self.bot.message_interval >= 10:
            conn = await self.bot.connpool.acquire()
            await conn.execute(f"UPDATE bot_stats SET messages_handled={self.bot.message_count}"
                               f"WHERE user_id=579399080799633448")
            await self.bot.connpool.release(conn)
            self.bot.message_interval = 0


def setup(bot):
    bot.add_cog(_Stats(bot))