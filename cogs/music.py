import discord
from discord.ext import commands
import yt_dlp
import asyncio
import logging

logger = logging.getLogger(__name__)

# Configure yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch',
    'quiet': True,
    'no_warnings': True,
}

class Music(commands.Cog):
    """Music commands for the bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}  # Store queues per guild
        self.currently_playing = {}  # Track current song per guild
    
    def get_queue(self, guild_id):
        """Get or create a queue for a guild"""
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]
    
    async def play_next(self, ctx):
        """Play the next song in queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if len(queue) > 0:
            url = queue.pop(0)
            await self.play_song(ctx, url)
        else:
            self.currently_playing[guild_id] = None
            await ctx.send("✅ Queue terminée!")
    
    async def play_song(self, ctx, url):
        """Play a song from URL"""
        guild_id = ctx.guild.id
        
        try:
            # Download audio info
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
                title = info.get('title', 'Unknown')
            
            self.currently_playing[guild_id] = title
            
            # Create FFmpeg audio source
            audio_source = discord.FFmpegPCMAudio(
                audio_url,
                before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                options='-vn'
            )
            
            # Play audio
            voice_client = ctx.voice_client
            voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx), self.bot.loop
                )
            )
            
            await ctx.send(f"🎵 Lecture en cours: **{title}**")
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture: {e}")
            await ctx.send(f"❌ Erreur: {e}")
            await self.play_next(ctx)
    
    @commands.command(name='join', aliases=['j'])
    async def join(self, ctx):
        """Join the user's voice channel"""
        if not ctx.author.voice:
            await ctx.send("❌ Vous n'êtes pas connecté à un salon vocal!")
            return
        
        channel = ctx.author.voice.channel
        try:
            await channel.connect()
            await ctx.send(f"✅ Connecté à {channel.name}")
        except Exception as e:
            await ctx.send(f"❌ Erreur de connexion: {e}")
    
    @commands.command(name='leave', aliases=['l'])
    async def leave(self, ctx):
        """Leave the voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.queue[ctx.guild.id] = []
            self.currently_playing[ctx.guild.id] = None
            await ctx.send("✅ Déconnecté du salon vocal")
        else:
            await ctx.send("❌ Je ne suis pas connecté à un salon vocal!")
    
    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query):
        """Play a song by name or URL"""
        if not ctx.author.voice:
            await ctx.send("❌ Vous n'êtes pas connecté à un salon vocal!")
            return
        
        if not ctx.voice_client:
            await ctx.invoke(self.join)
        
        await ctx.send(f"🔍 Recherche de '{query}'...")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                url = info['url']
                title = info.get('title', 'Unknown')
            
            if ctx.voice_client.is_playing():
                self.get_queue(ctx.guild.id).append(url)
                await ctx.send(f"⏸️ Ajouté à la queue: **{title}**")
            else:
                await self.play_song(ctx, url)
        
        except Exception as e:
            logger.error(f"Erreur: {e}")
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name='skip', aliases=['s', 'next'])
    async def skip(self, ctx):
        """Skip the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Chanson ignorée")
        else:
            await ctx.send("❌ Aucune chanson en lecture!")
    
    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Musique en pause")
        else:
            await ctx.send("❌ Aucune chanson en lecture!")
    
    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the paused song"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Musique reprise")
        else:
            await ctx.send("❌ Aucune chanson en pause!")
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop playing music and clear queue"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            self.get_queue(ctx.guild.id).clear()
            self.currently_playing[ctx.guild.id] = None
            await ctx.send("⏹️ Musique arrêtée et queue vidée")
        else:
            await ctx.send("❌ Je ne suis pas en train de jouer!")
    
    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx):
        """Show the current queue"""
        queue_list = self.get_queue(ctx.guild.id)
        
        if not queue_list and not self.currently_playing.get(ctx.guild.id):
            await ctx.send("📭 La queue est vide!")
            return
        
        embed = discord.Embed(title="🎵 Queue Musicale", color=discord.Color.blue())
        
        if self.currently_playing.get(ctx.guild.id):
            embed.add_field(
                name="Actuellement",
                value=self.currently_playing[ctx.guild.id],
                inline=False
            )
        
        if queue_list:
            queue_text = "\n".join([f"{i+1}. {url[:50]}..." for i, url in enumerate(queue_list[:10])])
            embed.add_field(
                name=f"Prochains ({len(queue_list)})",
                value=queue_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='volume', aliases=['v'])
    async def volume(self, ctx, volume: int = None):
        """Set the volume (0-100)"""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("❌ Aucune chanson en lecture!")
            return
        
        if volume is None:
            await ctx.send(f"🔊 Volume actuel: {int(ctx.voice_client.source.volume * 100)}%")
        else:
            if 0 <= volume <= 100:
                ctx.voice_client.source.volume = volume / 100
                await ctx.send(f"🔊 Volume réglé à {volume}%")
            else:
                await ctx.send("❌ Le volume doit être entre 0 et 100!")

async def setup(bot):
    await bot.add_cog(Music(bot))