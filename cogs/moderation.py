import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Moderation commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison"):
        """Kick a user from the server"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Utilisateur expulsé",
                color=discord.Color.orange()
            )
            embed.add_field(name="Utilisateur", value=member)
            embed.add_field(name="Raison", value=reason)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison"):
        """Ban a user from the server"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Utilisateur banni",
                color=discord.Color.red()
            )
            embed.add_field(name="Utilisateur", value=member)
            embed.add_field(name="Raison", value=reason)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name='mute')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison"):
        """Mute a user"""
        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False)
            
            await member.add_roles(role)
            embed = discord.Embed(
                title="🔇 Utilisateur rendu muet",
                color=discord.Color.red()
            )
            embed.add_field(name="Utilisateur", value=member)
            embed.add_field(name="Raison", value=reason)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name='unmute')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a user"""
        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if role and role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"🔊 {member} a été rendu au silence!")
            else:
                await ctx.send(f"❌ {member} n'est pas rendu muet!")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name='purge', aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """Delete messages from the channel"""
        if amount < 1 or amount > 100:
            await ctx.send("❌ Spécifiez un nombre entre 1 et 100!")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"✅ {len(deleted)} message(s) supprimé(s)!")