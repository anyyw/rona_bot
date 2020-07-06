#!/usr/bin/python3
import os
import discord
import requests
import random
import json
import asyncio
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

@bot.command(name='debug', help='debug print statement')
async def print_debug(context):
    response = 'Beep Boop, I here'
    await context.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# @bot.command(name='bruh', help='Bruh, bruhh, bruuuuhhhh.')
# async def bruh(ctx, bruh_length: int):
#     await ctx.send('Bruuu' + ('h' * bruh_length))

@bot.command(name='bruh', help='Bruh in voice channel.')
async def bruh_mp3(ctx):
    # grab the user who sent the command
    voice_state = ctx.author.voice
    channel = None
    # only play music if user is in a voice channel
    if voice_state != None:
        # grab user's voice channel
        channel = voice_state.channel
        await ctx.send('User is in channel: '+ channel.name)
        # create StreamPlayer
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('sounds/bruh.mp3'))
        vc.volume = 100
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
    else:
        await ctx.send('The Bruh was not uttered, user outside of a voice channel')

@bot.command(name='rona', help='Current coronavirus stats in the US')
async def rona(ctx, state='All'):
    url = 'covidtracking.com/api/states'
    request = 'https://{}'.format(url)
    response = requests.get(request)
    await ctx.send(response)

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise NotImplementedError

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found, type !help for a list of commands')
    else:
        await ctx.send('Got unhandled error {}, error type {}. Pinging @ApatheticDino'.format(error, error.__class__))
bot.run(TOKEN)
