import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load cogs
async def load_cogs():
    """Load all cogs from the cogs directory"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ Loaded cog: {filename}')
            except Exception as e:
                logger.error(f'❌ Failed to load cog {filename}: {e}')

@bot.event
async def on_ready():
    """Triggered when the bot is ready"""
    logger.info(f'✅ Bot connecté en tant que {bot.user}')
    logger.info(f'📊 Le bot est maintenant opérationnel dans {len(bot.guilds)} serveur(s)')
    try:
        synced = await bot.tree.sync()
        logger.info(f'🔄 Synchronisé {len(synced)} commande(s) slash globale(s)')
    except Exception as e:
        logger.error(f'❌ Erreur lors de la synchronisation des commandes: {e}')

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions nécessaires.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Commande non trouvée.")
    else:
        logger.error(f"Erreur non gérée: {error}")
        await ctx.send(f"❌ Une erreur est survenue: {error}")

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())