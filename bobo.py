import asyncio

import discord
import wave
from discord.ext import commands
import dotenv
from text_to_speach import text_to_speach
from translitter import translitter
from yan_speechkit import *
import ytplay
import os
#!!!!!!!!!!!!!!!!!!!!!ffmpeg нужно установить !!!!!!!!!!!!

dotenv.load_dotenv()
num = int(os.environ.get('num'))

token = "MTE4ODQ2NjEzNzc2MDAyNjY2NA.Gj6OjG.IJJAPOPKeEO6-8DNgJzqRnMOUSWzGewv4LEfhk"
# token = 'MTE5MDU3NjYwMzExODQ0NDU2NA.Gdb6Jf.n1ysN3mIgzWD7FDuEi7b-6q3zurV-Cd6KNBvrs'

intents = discord.Intents.default()  # Подключаем "Разрешения"
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

voice = discord.VoiceChannel

connections = {}
works = False
i = 700

voice_ch = None

@client.command()
async def record(ctx):  # If you're using commands.Bot, this will also work.
    global works
    global voice_ch
    if not works:
        works = True
        voice_ch = ctx.author.voice

        if not voice_ch:
            await ctx.respond("You aren't in a voice channel!")

        vc = await voice_ch.channel.connect()  # Connect to the voice channel the author is in.
        connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.

        vc.start_recording(
            discord.sinks.WaveSink(),  # The sink type to use.
            once_done,  # What to do once done.
            ctx.channel  # The channel to disconnect from.
        )
        await ctx.send("Started recording!")
    else:
        await ctx.send('already playing, stop and try again')


async def once_done(sink: discord.sinks.WaveSink, channel: discord.TextChannel,
                    *args):  # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    global i
    global works
    works = False
    await sink.vc.disconnect()  # Disconnect from the voice channel.
    for user_id, audio in sink.audio_data.items():
        print(user_id)
        channel = client.get_channel(1188457263829110845)
        with open(f"sample{i}.wav", "wb") as f:
            f.write(audio.file.getbuffer())
            i += 1
        audio_data = audio.file.getbuffer()
        filename = f"sample{i}.wav"
        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            wav_file.writeframesraw(audio_data)
        i += 1
        text = translitter(filename)
        await channel.send(f'<@1079058118534758530>  {text}')

    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in
             sink.audio_data.items()]  # List down the files.
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.",
                       files=files)  # Send a message with the accumulated files.


@client.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
    else:
        await ctx.send("I am currently not recording here.")  # Respond with this if we aren't recording.


@client.command()
async def horny(ctx):
    global works
    if not works:
        works = True
        voice = ctx.author.voice
        audio_source = discord.FFmpegPCMAudio('imhorny.mp3', executable='D:\\work\\ffmpeg-2023-12-28-git-c1340f3439-full_build\\bin\\ffmpeg.exe')
        if not voice:
            await ctx.respond("You aren't in a voice channel!")

        vc = await voice.channel.connect()
        vc.play(audio_source)
    else:
        await ctx.send('stop the splaying and try again')

@client.command()
async def yt(ctx, url):
    global works
    if not works:
        works = True
        """Plays from a url (almost anything youtube_dl supports)"""
        voice = ctx.author.voice
        if not voice:
            await ctx.respond("You aren't in a voice channel!")
        vc = await voice.channel.connect()

        async with ctx.typing():
            player = await ytplay.YTDLSource.from_url(url)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))
    else:
        await ctx.send("you need to stop the playing first, then try again")

@client.command()
async def join(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
    vc = await voice.channel.connect()

@client.command()
async def stop(ctx):
    global works
    works = False
    await ctx.voice_client.disconnect()

cnt = 0
gl_voice = ''
@client.event
async def on_message(message):
    # if message.author == 1079058118534758530 and\
    # if message.channel.id == 1188457263829110845:
    # global cnt
    # if cnt == 0:
    #     global gl_voice
    #     gl_voice = message.author.voice
    #     cnt = 1
    global voice_ch
    if message.author.id == 346580428506923010:
        # gl_voice = message.author.voice

        if not voice_ch:
            await message.channel.send("You aren't in a voice channel!")
        vc = await voice_ch.channel.connect()
        # text_to_speach(message.content)
        global num
        yan_speech(f'{message.content}', num)
        print(f'{message.content}')
        print(message.content)
        print(message)
        audio_source = discord.FFmpegPCMAudio(f'test{num}.mp3',
                                              executable='D:\\work\\ffmpeg-2023-12-28-git-c1340f3439-full_build\\bin\\ffmpeg.exe')
        num += 1
        os.environ['num'] = str(num)

        vc.play(audio_source)
        # await message.reply(message.content)
        await asyncio.sleep(5)
        await vc.disconnect()
    await client.process_commands(message)
    # if str(message.author) == 'ChatGPT#2924':
    #     print('hi')
    #
    # await client.process_commands(message)


client.run(token)
