import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL

# Inisialisasi bot
client = commands.Bot(command_prefix='!')

# Fungsi untuk mengambil audio dari YouTube
def search(arg):
    with YoutubeDL({'format':'bestaudio', 'noplaylist':'True'}) as ydl:
        try: 
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        except:
            return False
    return {'source': info['formats'][0]['url'], 'title': info['title']}

# Command play untuk memutar musik
@client.command()
async def play(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if not voice_client:
        await voice_channel.connect()
        voice_client = get(client.voice_clients, guild=ctx.guild)

    song = search(query)

    if not song:
        await ctx.send("Maaf, saya tidak bisa memutar musik tersebut.")
    else:
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(song['source']))
            await ctx.send(f"Memutar: {song['title']}")
        else:
            await ctx.send("Sedang memutar musik, tambahkan antrian dengan command !queue")

# Command queue untuk menambahkan lagu ke antrian
@client.command()
async def queue(ctx, *, query):
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if not voice_client:
        await ctx.send("Saya tidak sedang terhubung ke channel suara manapun.")
    else:
        song = search(query)

        if not song:
            await ctx.send("Maaf, saya tidak bisa memutar musik tersebut.")
        else:
            voice_client.queue.append(song)
            await ctx.send(f"Menambahkan ke antrian: {song['title']}")

# Command skip untuk melewatkan lagu
@client.command()
async def skip(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if not voice_client:
        await ctx.send("Saya tidak sedang terhubung ke channel suara manapun.")
    elif not voice_client.is_playing():
        await ctx.send("Tidak sedang memutar musik.")
    else:
        voice_client.stop()
        await ctx.send("Lagu berhasil dilewati.")

# Command stop untuk menghentikan musik
@client.command()
async def stop(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if not voice_client:
        await ctx.send("Saya tidak sedang terhubung ke channel suara manapun.")
    else:
        voice_client.stop()
        await ctx.send("Musik berhasil dihentikan.")

# Menjalankan bot
client.run("TOKEN_DISCORD_ANDA")
