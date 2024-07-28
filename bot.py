import os
import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
messages = {}

# Flask server setup
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():  
    t = Thread(target=run)
    t.start()

@bot.command()
async def send(ctx, *, message):
    recipient_id = int(os.getenv('FRIEND_USER_ID'))  # Get from environment variable
    if recipient_id not in messages:
        messages[recipient_id] = []
    messages[recipient_id].append(message)
    await ctx.send("Message stored for your friend.")


@bot.command()
async def break_time(ctx):
    # Check if the user invoking the command is the FRIEND_USER_ID
    if ctx.author.id == int(os.getenv('FRIEND_USER_ID')):
        # Get all stored messages for the user
        msg = "\n".join(messages.get(ctx.author.id, []))
        
        if msg:
            await ctx.send(f"Your messages:\n{msg}")
            # Clear the stored messages
            messages[ctx.author.id] = []
        else:
            await ctx.send("You don't have any stored messages.")
    else:
        await ctx.send("Sorry, only the designated friend can clear the messages.")


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
keep_alive()

bot.run(os.getenv('BOT_TOKEN'))
