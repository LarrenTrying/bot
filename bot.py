import discord
from discord import app_commands

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print("Bot online")

@tree.command(name="vc", description="Toggle mute/unmute for everyone in your VC")
async def vc(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message(
            "You must be in a voice channel.", ephemeral=True
        )
        return

    channel = interaction.user.voice.channel

    should_mute = any(
        not m.bot and not m.voice.mute
        for m in channel.members
    )

    for member in channel.members:
        if not member.bot:
            await member.edit(mute=should_mute)

    await interaction.response.send_message(
        "🔇 Everyone muted." if should_mute else "🔊 Everyone unmuted."
    )

client.run("YOUR_BOT_TOKEN")
