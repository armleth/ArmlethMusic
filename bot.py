# bot.py

import os
from discord.ext import commands,tasks
import discord
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

#print(TOKEN)

intents = discord.Intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='?',intents=intents)

queue = []

# youtube scrap options
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# Bot commands
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='display', help='display the queue')
async def display(ctx):
    for i in queue:
        await ctx.send(i[0])


@bot.command(name='play', help='To play song')
async def play(ctx,url):
    try :
        voice_client = ctx.message.guild.voice_client
        videosSearch = VideosSearch(url,limit = 1)

        title = videosSearch.result()['result'][0]['title']
        url = videosSearch.result()['result'][0]['link']
        
        server = ctx.message.guild
        voice_channel = server.voice_client
        
        if len(queue) == 0:
            queue.append((title,url))
            start_playing(ctx,voice_channel)
        
        else:
            queue.append((title,url))
            await ctx.send("La musique a été mise en queue")

        #async with ctx.typing():
        #await ctx.send('**Now playing: ' + info['title'] + '**')
    except:
        await ctx.send("Ratio, gros noob")

def start_playing(ctx,voice_channel):
    i = 0
    while i < len(queue):
        try:
            url = queue[i][1]

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)

            URL = info['url']
            voice_channel.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

        except:
            pass
        i+=1

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


# Main part, initialisation of the bot
if __name__ == "__main__" :
    bot.run(TOKEN)
