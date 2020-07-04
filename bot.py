#!/usr/bin/python3
import os
import discord
import req
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
# @bot.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(
#         f'{guild.name}(id: {guild.id})'
#     )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        """Yo Whaddup! {member.name}, welcome to dis discord server!
        I'm the local discord bot, hit me up with a !help to show what
        I can do!"""
    )

@bot.command(name='booya', help='Responds with hell ya')
async def on_message(message):
    response = 'Hell ya'
    await message.channel.send(response)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
