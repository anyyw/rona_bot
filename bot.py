#!/usr/bin/python3
import os
import discord
import requests
import random
import json
import asyncio
from io import BytesIO
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

@bot.command(name='roll_dice', help='Simulates rolling dice, ex usage !roll_dice <num_dice> <num_sides>')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# @bot.command(name='bruh', help='Bruh, bruhh, bruuuuhhhh.')
# async def bruh(ctx, bruh_length: int):
#     await ctx.send('Bruuu' + ('h' * bruh_length))

@bot.command(name='bruh', help='Bruh in voice channel with ability to add length, ex !bruh <bruh_length>')
async def bruh_mp3(ctx, length: int = 1):
    # grab the user who sent the command
    voice_state = ctx.author.voice
    channel = None
    # validation
    # There should prob be handling of invalid input types, but whatever
    if length > 10:
        await ctx.send('Bruh too long, pls stop')
    elif length <= 0:
        await ctx.send('Bruh too short or negative, wat')
    elif voice_state == None:
        await ctx.send('The Bruh was uttered but it did not make a sound, user outside of a voice channel')
    else:
        # grab user's voice channel
        channel = voice_state.channel
        # await ctx.send('Channel {}: bruh{} '.format(channel.name, 'hhh' * length))
        # create StreamPlayer
        vc = await channel.connect()
        atempo_option = 'atempo=0.8'
        clip_length = []
        for n in range(length):
            clip_length.append(atempo_option)
        options = '-filter:a "{}"'.format(','.join(clip_length))
        vc.play(discord.FFmpegPCMAudio(
            source='sounds/bruh.mp3', 
            options=options))
        vc.volume = 100
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
        

@bot.command(name='rough', help="For when your friend's girlfriend turns into the moon. Usage: !rough")
async def rough(ctx):
    # grab the user who sent the command
    voice_state = ctx.author.voice
    channel = None
    # validation
    if voice_state == None:
        await ctx.send('User outside of a voice channel')
    else:
        # grab user's voice channel
        channel = voice_state.channel
        # await ctx.send('Channel {}: bruh{} '.format(channel.name, 'hhh' * length))
        # create StreamPlayer
        vc = await channel.connect()
        options = '-ss 5'
        vc.play(discord.FFmpegPCMAudio(
            source='sounds/rough.mp3', 
            options=options))
        vc.volume = 100
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

@bot.command(name='ohno', help='Oh no, usage: !ohno')
async def ohno(ctx):
    # grab the user who sent the command
    voice_state = ctx.author.voice
    channel = None
    # validation
    if voice_state == None:
        await ctx.send('The Bruh was uttered but it did not make a sound, user outside of a voice channel')
    else:
        # grab user's voice channel
        channel = voice_state.channel
        # await ctx.send('Channel {}: bruh{} '.format(channel.name, 'hhh' * length))
        # create StreamPlayer
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            source='sounds/ono.mp3'))
        vc.volume = 100
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

@bot.command(name='airhorn', help='Brrrrrrr! Usage: !airhorn <num_airhorn_blasts>')
async def airhorn_mp3(ctx, count: int = 1):
    # grab the user who sent the command
    voice_state = ctx.author.voice
    channel = None
    # validation
    if count > 10:
        await ctx.send('Too many airhorns!')
    elif count <= 0:
        await ctx.send('Too few airhorns')
    elif voice_state == None:
        await ctx.send('The Airhorn was blasted but it did not make a sound, user outside of a voice channel')
    else:
        # grab user's voice channel
        channel = voice_state.channel
        # await ctx.send('Channel {}: bruh{} '.format(channel.name, 'hhh' * length))
        # create StreamPlayer
        vc = await channel.connect()
        # because discord ffmpeg implementation can only read files, not concat filters,
        # we need to write to a temp file and send that in for concatnating airhorns
        with open("temp.txt", "a") as file:
            file.write("{}file './sounds/airhorn.wav'".format(
            "file './sounds/airhorn-short.wav'\n" * (count - 1)))
        clip = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
            source="temp.txt",
            before_options='-f concat -safe 0'))
        clip.volume = 0.3
        vc.play(clip)
        while vc.is_playing():
            await asyncio.sleep(0.1)
        os.remove("temp.txt")
        await vc.disconnect()

'''
Command that shows stats on current coronavirus, hopefully this will be outdated soon
TODO: Current implementation makes a request per command, since the website likely updates
daily, we should just be able to cache the json and update it every day on command read
'''
@bot.command(name='rona', help='Current coronavirus stats in the US, Work in progress')
async def rona(ctx, state='all'):
    url = 'covidtracking.com/api/states'
    request = 'https://{}'.format(url)
    response = requests.get(request)
    rona_json = json.load(response.json())
    if state == all:
        for state in rona_json:
            await ctx.send(rona_json)
    

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise NotImplementedError

'''
Error handling
'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found, type !help for a list of commands')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send('Invalid argument, please refer to help for specific command')
    else:
        await ctx.send('Got unhandled error {}, error type {}. Pinging @ApatheticDino'.format(error, error.__class__))
bot.run(TOKEN)
