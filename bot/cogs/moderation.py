import asyncio
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

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await ctx.guild.kick(member, reason=reason)
        except:
            await ctx.error('Unable to kick member.')

        em = discord.Embed(title=f'Kicked: {member}', color=self.bot.gold, description=f'Reason: {reason}')
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, expire_after=0, *, reason='None'):
        baguette_muted_role = discord.utils.get(ctx.guild.roles, name='Baguette-Muted')

        if baguette_muted_role is None:
            baguette_muted_role = await ctx.guild.create_role(name='Baguette-Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(baguette_muted_role, send_messages=False)

        await member.add_roles(baguette_muted_role, reason=reason)

        em = discord.Embed(title=f'Muted: {member}', color=self.bot.gold)
        em.description = f'Reason: {reason} | Time: {str(expire_after)}M'

        await ctx.send(embed=em)

        if expire_after != 0:
            try:
                await asyncio.sleep(expire_after*60)
                await member.remove_roles(baguette_muted_role, reason='Mute expired.')
            except:
                pass

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, reason='None'):
        baguette_muted_role = discord.utils.get(ctx.guild.roles, name='Baguette-Muted')

        if baguette_muted_role is None:
            baguette_muted_role = await ctx.guild.create_role(name='Baguette-Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(baguette_muted_role, send_messages=False)

        try:
            await member.remove_roles(baguette_muted_role, reason=reason)
            em = discord.Embed(title=f'Unmuted: {member}', color=self.bot.gold)
            em.description = f'Reason: {reason}'
            await ctx.send(embed=em)
        except:
            await ctx.send(f"{member} is not muted.")

    @commands.command(name='[urge', aliases=['del', 'd', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages have been deleted!')


def setup(bot):
    bot.add_cog(Moderation(bot))
