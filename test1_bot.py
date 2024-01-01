import asyncio

import discord
from discord.ext import commands
from text_to_speach import text_to_speach

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
work = False


config = {
    'token': 'MTE5MTAzMTAzNjkyMzEwNTM2Mg.GiLnkm.DW6UKUiIP6XAm2zWAwjnhkwkJTI_OnIqmZt7MA',
    'prefix': '/',
}

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
#


# @bot.command()
# # async def ping(ctx):
# #     await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.author != bot.user and message.channel.id == 1188473086186622977:
        voice = message.author.voice
        if not voice:
            await message.respond("You aren't in a voice channel!")
        vc = await voice.channel.connect()
        text_to_speach(message.content)
        audio_source = discord.FFmpegPCMAudio('test1.mp3',
                                              executable='D:\\work\\ffmpeg-2023-12-28-git-c1340f3439-full_build\\bin\\ffmpeg.exe')
        vc.play(audio_source)
        await message.reply(message.content)
        await asyncio.sleep(5)
        await vc.disconnect()

bot.run(config['token'])