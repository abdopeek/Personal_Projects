import discord
import random
from discord.ext import commands

TOKEN = BOT_TOKEN

hi = ['hi', 'hello', 'hey']
bye = ['bye', 'bye bye', 'cya']

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print("--------------------------------------------")

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    if message.author != client.user:
        print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return 
    
    if message.channel.name == 'general':
        if user_message.lower() in hi:
            await message.channel.send(f'Hello {username}!')
            return
        elif user_message.lower() in bye:
            await message.channel.send("Bye Bye")
            return
    await client.process_commands(message)
        

@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Not in a voice channel")

@client.command(pass_context = True)
async def leave(ctx):
    vc = client.voice_clients
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("Not in a voice channel")
    else:
        for channel in vc:
            await channel.disconnect()

@client.command(pass_context = True)
async def play(ctx, url):
    vc = client.voice_clients
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            cc = await channel.connect()
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=1)
            player = cc.play(source)
            return
        await ctx.send("User not in a voice channel")
        return
    else:
        vc = vc[0]
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file), volume=1)
        player = vc.play(source)
        return

@client.command(pass_context = True)
async def pause(ctx):
    vc = client.voice_clients
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("Not connected to voice channel.")
        return
    vc = vc[0]
    if not vc.is_playing() or vc.is_paused():
        await ctx.send("Nothing playing")
        return
    elif vc.is_playing():
        vc.pause()
        return

@client.command(pass_context = True)
async def resume(ctx):
    vc = client.voice_clients
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("Not connected to voice channel.")
        return
    vc = vc[0]
    if vc.is_playing():
        await ctx.send("Already playing")
        return
    elif not vc.is_playing():
        vc.resume()
        return

@client.command(pass_context = True)
async def volume(ctx, vol : float):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("Not connect to a voice channel")
        return
    if not voice.is_playing():
        await ctx.send("Nothing playing")
        return
    new_vol = vol / 100
    voice.source.volume = new_vol
    await ctx.send(f"Volume set to {vol}")
    return


@volume.error
async def volume_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Volume argument required (!volume (0-100))")
        return
    return

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, member: discord.Member):
    if member.guild_permissions.administrator:
        await ctx.send("Target is an admin")
        return
    else:
        try:
            await member.kick()
            await ctx.send(f"{member} kicked.")
            await ctx.message.delete()
            return
        except Exception:
            await ctx.send("Something went wrong")
            return
        
@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, target: discord.Member):
    if target.guild_permissions.administrator:
        await ctx.send("Target is an admin")
        return
    else:
        try:
            await target.ban()
            await ctx.send(f"{target} banned.")
            await ctx.message.delete()
            return
        except Exception:
            await ctx.send("Something went wrong")
            return

@commands.has_permissions(ban_members=True)
@client.command()
async def unban(ctx, target: int):
    banned = [entry async for entry in ctx.guild.bans()]
    for entry1 in banned:
        user = entry1.user
        id = user.id
        if id == target:
            await ctx.guild.unban(user)
            await ctx.send(f"{user} unbanned.")
            return
    return
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing (ID) argument")
        return

@client.command()
async def purge(ctx, amount:str):
    if amount.lower() == 'all':
        await ctx.channel.purge()
        return
    else:
        try:
            amount = int(amount) + 1
            await ctx.channel.purge(limit=amount)
        except:
            await ctx.send("Amount has to be a valid integer")


client.run(TOKEN)
