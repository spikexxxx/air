# 🎵 Discord Music Bot

Un bot Discord complet avec commandes musicales, de modération et de divertissement!

## 🎯 Fonctionnalités

### 🎵 Commandes Musicales
- `!play <chanson>` - Jouer une chanson
- `!skip` - Ignorer la chanson actuelle
- `!pause` - Mettre en pause
- `!resume` - Reprendre la lecture
- `!stop` - Arrêter la musique
- `!queue` - Afficher la file d'attente
- `!join` - Rejoindre un salon vocal
- `!leave` - Quitter le salon vocal
- `!volume <0-100>` - Régler le volume

### 🎮 Commandes Fun
- `!ping` - Vérifier la latence
- `!dice` - Lancer un dé
- `!choose <option1 | option2>` - Choisir aléatoirement
- `!8ball <question>` - Boule de cristal magique
- `!userinfo [utilisateur]` - Info utilisateur
- `!avatar [utilisateur]` - Avatar utilisateur

### 🛡️ Commandes de Modération
- `!kick <utilisateur> <raison>` - Expulser un utilisateur
- `!ban <utilisateur> <raison>` - Bannir un utilisateur
- `!mute <utilisateur> <raison>` - Rendre muet
- `!unmute <utilisateur>` - Retirer le silence
- `!purge <nombre>` - Supprimer des messages
- `!warn <utilisateur> <raison>` - Avertir un utilisateur

## ⚙️ Installation

### Prérequis
- Python 3.8+
- FFmpeg (pour la musique)
- Un token Discord Bot

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/spikexxxx/air.git
cd air
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**
```bash
cp .env.example .env
```

Éditez `.env` et ajoutez:
```
DISCORD_TOKEN=votre_token_ici
BOT_PREFIX=!
OWNER_ID=votre_id_discord
```

4. **Installer FFmpeg**

**Windows:**
```bash
choco install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

5. **Lancer le bot**
```bash
python main.py
```

## 🔐 Créer un Bot Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application"
3. Donnez un nom à votre bot
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. Sous TOKEN, cliquez sur "Copy"
7. Collez le token dans `.env`

## 📋 Permissions Requises

Le bot a besoin des permissions suivantes:
- Lire les messages
- Envoyer des messages
- Gérer les messages
- Lire l'historique des messages
- Se connecter au vocal
- Parler dans le vocal
- Bannir les utilisateurs
- Expulser les utilisateurs

## 📁 Structure du Projet

```
air/
├── main.py           # Fichier principal
├── requirements.txt  # Dépendances Python
├── .env.example      # Exemple de configuration
├── README.md         # Ce fichier
└── cogs/
    ├── music.py      # Commandes musicales
    ├── fun.py        # Commandes fun
    └── moderation.py # Commandes de modération
```

## 🚀 Lancer le Bot sur un Serveur

### Avec Heroku (Gratuit - Limité)
1. Créez un compte Heroku
2. Installez Heroku CLI
3. Créez un `Procfile`:
```
worker: python main.py
```
4. Créez un `runtime.txt`:
```
python-3.9.16
```
5. Déployez:
```bash
heroku login
heroku create your-app-name
heroku config:set DISCORD_TOKEN=votre_token
git push heroku main
heroku ps:scale worker=1
```

### Avec Replit (Gratuit - Maintenu en vie)
1. Fork sur Replit
2. Configurez `.env`
3. Cliquez sur "Run"

### Avec Un VPS (Meilleur)
1. Louer un VPS (Linode, DigitalOcean, etc.)
2. SSH vers le serveur
3. Installer Python et FFmpeg
4. Cloner le repo
5. Installer les dépendances
6. Utiliser `screen` ou `systemd` pour garder le bot actif

## 📝 Ajouter des Commandes

Pour ajouter une commande, créez un nouveau cog:

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mycommand')
    async def my_command(self, ctx):
        await ctx.send("Bonjour!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

Puis placez le fichier dans le dossier `cogs/`.

## 🤝 Contribution

Les contributions sont bienvenues! N'hésitez pas à ouvrir des issues ou des pull requests.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 💬 Support

Pour toute question ou problème, ouvrez une [issue](https://github.com/spikexxxx/air/issues).

## ⭐ Merci!

Si vous aimez ce projet, n'oubliez pas de le star! ⭐