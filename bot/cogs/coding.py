import aiohttp

from bot import logger
from discord.ext import commands


class Coding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mystbin(self, ctx, *, content: str):
        """Send data to MystBin"""

        if content.startswith("```python") and content.endswith("```"):
            content = content[10:len(content)-3]
        elif content.startswith("```py") and content.endswith("```"):
            content = content[6:len(content)-3]

        for x in range(0, 3):
            if content[0] == '`':
                content = content[1:]
            if content[-1] == '`':
                content = content[:len(content) - 1]

        url = 'https://mystb.in/'
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}/documents', data=content) as resp:
                holder = await resp.json()
                await ctx.send(f"{url}{holder.get('key')}")


def setup(bot):
    bot.add_cog(Coding(bot))
