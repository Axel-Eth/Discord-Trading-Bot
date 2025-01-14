
import os
from dotenv import load_dotenv
import json
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Charger le fichier JSON
with open("definitions.json", "r", encoding="utf-8") as f:
    definitions = json.load(f)

# Fonction d'autocomplete
async def autocomplete_termes(interaction: discord.Interaction, current: str):
    # Filtrer les titres qui contiennent le texte tapé
    termes = [titre for titre in definitions.keys() if current.lower() in titre.lower()]
    return [app_commands.Choice(name=titre, value=titre) for titre in termes[:25]]  # Discord limite à 25 résultats

# Créer une commande slash avec autocomplete
@bot.tree.command(name="definition", description="Obtenez une définition depuis votre fichier JSON.")
@app_commands.describe(titre="Le titre de la définition à rechercher.")
@app_commands.autocomplete(titre=autocomplete_termes)
async def lexique(interaction: discord.Interaction, titre: str):
    # Vérifier si le titre existe dans le JSON
    if titre in definitions:
        contenu = definitions[titre]
        embed = discord.Embed(
            title=titre,
            description=contenu.get("definition", "Aucune définition disponible."),
            color=discord.Color.blue()
        )
        # Ajouter les autres champs si disponibles
        if "analogie" in contenu:
            embed.add_field(name="Analogie", value=contenu["analogie"], inline=False)
        if "caracteristiques" in contenu:
            embed.add_field(name="Caractéristiques", value=contenu["caracteristiques"], inline=False)
        if "explication" in contenu:
            embed.add_field(name="Explication", value=contenu["explication"], inline=False)
        if "importance" in contenu:
            embed.add_field(name="Pourquoi c'est important ?", value=contenu["importance"], inline=False)
        if "exemple" in contenu:
            embed.add_field(name="Exemple", value=contenu["exemple"], inline=False)
        if "utilisation" in contenu:
            embed.add_field(name="Utilisation", value=contenu["utilisation"], inline=False)
        if "note" in contenu:
            embed.add_field(name="Note", value=contenu["note"], inline=False)
        if "ressource" in contenu:
            embed.add_field(name="Ressources", value=contenu["ressource"], inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        # Si le titre n'existe pas
        await interaction.response.send_message(f"Aucune définition trouvée pour '{titre}'.", ephemeral=True)

# Synchroniser les commandes slash lors du démarrage
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s)")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes slash : {e}")

keep_alive()


# Lancer le bot
def main():
    bot.run(token)


if __name__ == "__main__":
    main()

