import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Fun commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latence: {latency}ms")
    
    @commands.command(name='dice', aliases=['roll'])
    async def dice(self, ctx, sides: int = 6):
        """Roll a dice"""
        if sides < 2:
            await ctx.send("❌ Le dé doit avoir au moins 2 faces!")
            return
        result = random.randint(1, sides)
        await ctx.send(f"🎲 {ctx.author.mention} a lancé un d{sides} et obtenu: **{result}**")
    
    @commands.command(name='choose')
    async def choose(self, ctx, *, options):
        """Choose randomly between options (separated by |)"""
        choices = options.split('|')
        if len(choices) < 2:
            await ctx.send("❌ Fournissez au moins 2 options séparées par |")
            return
        choice = random.choice(choices).strip()
        await ctx.send(f"🎯 Choix: **{choice}**")
    
    @commands.command(name='8ball')
    async def magic_8ball(self, ctx, *, question):
        """Ask the magic 8 ball a question"""
        responses = [
            "Oui, définitivement.",
            "Non, jamais.",
            "Peut-être...",
            "Outlook bon.",
            "C'est certain.",
            "Doubtful.",
            "Demande plus tard.",
            "Ne comptez pas là-dessus.",
            "Les signes pointent vers oui.",
            "Très douteux."
        ]
        answer = random.choice(responses)
        embed = discord.Embed(title="🎱 Magic 8 Ball", description=answer, color=discord.Color.purple())
        embed.add_field(name="Question", value=question)
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', aliases=['user', 'info'])
    async def userinfo(self, ctx, user: discord.User = None):
        """Get user information"""
        user = user or ctx.author
        embed = discord.Embed(title=f"👤 {user}", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Bot", value="✅ Oui" if user.bot else "❌ Non")
        embed.add_field(name="Créé le", value=user.created_at.strftime("%d/%m/%Y"))
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar')
    async def avatar(self, ctx, user: discord.User = None):
        """Get user avatar"""
        user = user or ctx.author
        if not user.avatar:
            await ctx.send("❌ Cet utilisateur n'a pas d'avatar!")
            return
        embed = discord.Embed(title=f"Avatar de {user}", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))