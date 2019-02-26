#Imports
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import asyncio
import os
import logging
import aiohttp
import datetime
import random
from random import randint
import json
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np

#starttime
start_time = time.time()
#bot version
botversion = "The bot is in version 1.3.2"
#defining client
client = Bot("d;")
#to make a custom help command
client.remove_command("help")

#Console

@client.event
async def on_ready():
    print("=================================")
    print("Username: %s"%client.user.name)
    print("ID: %s"%client.user.id)
    print("Server count : {}".format(str(len(client.servers))))
    print("Bot Version: {}".format(botversion))
    await client.change_presence(game=discord.Game(name='nothing', type=0))
    print("=================================")    

##################################COMMANDS##################################################

#ping
@client.command(aliases=['p'])
async def ping():
    pingtime = time.time()
    e = discord.Embed(title = 'Okie Wait', color = 0x1abc9c)
    pingus = await client.say(embed=e)
    ping = time.time() - pingtime
    ping1 = discord.Embed(title = 'Pong!', description = ':ping_pong: Ping time - `%.01f seconds`' % ping, colour = 0x1abc9c)
    await client.edit_message(pingus, embed=ping1)

#command1
@client.event
async def on_message(message):
    if not message.author.bot:
        member_add_exp(message.author.name, 3)
    await client.process_commands(message)


def member_add_exp(member_name: int, exp: int):
    if os.path.isfile("exp.json"):
        try:
            with open('exp.json', 'r') as f:
                members = json.load(f)
                members[member_name]['exp'] += exp
                with open('exp.json', 'w') as f:
                    json.dump(members, f, indent=2)
        except KeyError:
            with open('exp.json', 'r') as f:
                members = json.load(fp)
                members[member_name] = {}
                members[member_name]['exp'] = exp
                with open('exp.json', 'w') as fp:
                    json.dump(members, f, indent=2)

    else:
        members = {member_name: {}}
        members[member_name]['exp'] = exp
        with open('exp.json', 'w') as f:
            json.dump(members, f, indent=2)
         
            
@client.command(pass_context=True)
async def exp(ctx, *, user : discord.Member = None):
    if not user:
        user = ctx.message.author
    
    if os.path.isfile('exp.json'):
        with open('exp.json', 'r') as f:
            members = json.load(f)
            expp = int(members[user.name]['exp'])
            e = discord.Embed(title = "{}'s Experience".format(user.name), colour = 0x1abc9c)
            e.add_field(name = "Exp", value = expp)
            e.add_field(name = "Total Messages", value = expp / 3)
            await client.say(embed=e)
    else:
        return

   
#command2
@client.command(pass_context=True)
async def serverlist(ctx):
    msg = ""
    for server in client.servers:
        msg+=  "-> {}\n".format(server.name)
    await client.say(msg)
 
#command3
@client.command(pass_context=True, aliases=['k'])
async def kick(ctx, *, member : discord.Member = None):
    if not ctx.message.author.bot:
        if not ctx.message.author.server_permissions.kick_members:
            return
 
        if not member:
            return await client.say(ctx.message.author.mention + "Frikin specify a user to kick!")
        try:
            await client.kick(member)
            await client.message(member, "You have been kicked from " + ctx.message.server.name)

        except Exception as e:
            if 'Privilege is too low' in str(e):
                return await client.say(":x: The bot/you do not have permissions to do shit like this")
 
        embed = discord.Embed(description = "**%s** got a boot!!!"%member.name, color = 0x1abc9c)
        await client.say(embed = embed)
 
#command4
@client.command(pass_context = True, aliases=['h'])
async def help(ctx):
    embed = discord.Embed(description= "My commands and help on other stuff.\n All commands use the prefix `d;`",title = "Help" , colour =0x1abc9c);
    embed.add_field(name = '__**Moderation**__', value = "purge; mute; unmute; timedmute, kick; ban; clearnicknames")
    embed.add_field(name = '__**Bot**__', value = "ping, help, info, setgame(owner only), uptime, stream(owner only)")
    embed.add_field(name = '__**Fun**__', value = "roll, flip, dance, spamhere, randommusic, kill, choose, embed, repeat, urbandictionary, virus, suicide, rps, slap, cat, dog")
    embed.add_field(name = '__**Others**__', value = "exp, add, multiply, subtract, divide, exponent, serverinfo, support, avatar, whatis, id, roles");
    embed.add_field(name = '__**Note**__', value = """To use the timed-mute command, make a role name `Muted`, it should be exactly the same.\n Please provide the bot administrator perms since a few commands may not work without it.""");
    embed.add_field(name = '__**Help**__', value = "Music is removed in this version, will be re-added soon.\nTo see/copy the bot's source code, have a look at the help server\nTo add your advertisement here DM Dot#4447\nFor help with any command use `help_(command name)`");
    embed.add_field(name = '__**Special**__', value = 'To get server special commands, autorole or selfroles, use the contact owner command.')
    embed.set_footer(text = "Requested by - " + ctx.message.author.name + " in - " + ctx.message.server.name + ", " + ctx.message.channel.name);

    if ctx.message.author.id == '252031624441626635':
        await client.say("Dot, I doubt you need to see your own bot's help command but here it is--")
        await asyncio.sleep(3)
        return await client.say(embed=embed)
    else:
        await client.whisper(embed = embed)
        return await client.say("Check your DMs :envelope:")


#command6
@client.command(pass_context = True, aliases=['purge'])
async def clear(ctx, number):
    if not ctx.message.author.id == '252031624441626635':
        if not ctx.message.author.server_permissions.administrator:
            return
    mgs = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)
    msg = await client.say("Purged messages")
    await asyncio.sleep(1)
    await client.delete_message(msg)

#command7
@client.command(pass_context = True, aliases=['id'])
async def ID(ctx, user : discord.Member=None):
    if not user:
        user = ctx.message.author
        
    embed = discord.Embed(title = user.name, colour = 0x1abc9c);
    embed.set_thumbnail(url = user.avatar_url);
    embed.add_field(name = 'ID', value = user.id)
    await client.say(embed=embed)

    
#command8
@client.command(pass_context=True)
async def leaveserver(ctx):
    auth = ctx.message.author
    if auth.id == '252031624441626635':
        client.leave_server(ctx.message.server)
    else:
        await client.say("No.")
        print("{} tried to make me leave a server".format(auth.name))

#command9
@client.command(pass_context=True, aliases=['dice'])
async def roll(ctx, sides : int=None):
    if not sides:
        sides = 6
    choice  = random.randint(1, int(sides))
    embed = discord.Embed(title = 'Dice', description = 'Rolled a dice with %s sides, the outcome is {}'.format(choice) %sides, colour = 0x1abc9c)
    await client.say(embed=embed)


#command10
@client.command(pass_context=True, aliases = ['coin', 'coinflip'])
async def flip(ctx):
    e = discord.Embed(title = ".....and...flip!", color = 0x1abc9c)
    e.set_image(url="https://media.giphy.com/media/6jqfXikz9yzhS/giphy.gif")
    one = await client.say(embed=e)
    asyncio.sleep(10)
    choose = ("It's Tails!", "It's Heads!")
    choice = random.choice(choose)
    if choice == "It's Tails!":
        choice2 = "https://cdn.discordapp.com/attachments/370616847328083968/371566223256715266/Tails.png"
    else:
        choice2 = "https://cdn.discordapp.com/attachments/370616847328083968/371566837701410828/Heads.png"
    e2 = discord.Embed(title = choice, color = 0x1abc9c)
    e2.set_image(url=choice2)
    await client.edit_message(one, embed=e2)

    
#command11
@client.command(pass_context=True)
async def dance(ctx):
    Dance = ['https://media.giphy.com/media/l2JJyDYEX1tXFmCd2/giphy.gif', 'https://media.giphy.com/media/Ve20ojrMWiTo4/giphy.gif', 'https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/giphy.gif', 'https://media.giphy.com/media/jzaZ23z45UxK8/giphy.gif', 'https://media.giphy.com/media/MVDPX3gaKFPuo/giphy.gif', 'https://media.giphy.com/media/XyAGm96eUIPsc/giphy.gif', 'https://media.giphy.com/media/xT9Igmg6f5LjztbPfW/source.gif', 'https://media.giphy.com/media/LdEeG8dsMmif6/giphy.gif', 'https://media.giphy.com/media/3rgXBvnbXtxwaWmhr2/giphy.gif', 'https://media.giphy.com/media/olAik8MhYOB9K/giphy.gif', 'https://media.giphy.com/media/Xdcj75alQutVe/giphy.gif']
    x  = random.choice(Dance)
    embed = discord.Embed(title = "{} is dancing!:".format(ctx.message.author.name), colour = 0x1abc9c)
    embed.set_image(url = x)
    await client.say(embed = embed)

    
#command16
@client.command(pass_context=True)
async def spamhere(ctx):
    await client.say("https://giphy.com/gifs/spam-xdnytp8742kg0")

#command18
@client.command(pass_context = True)
async def info(ctx):
    embed = discord.Embed(title = 'Info!', colour = 0x1abc9c)
    embed.add_field(name = '**Basic**', value = 'This is a bot developed by Dot#4447.');
    embed.add_field(name = '**Coding and hosting**', value = 'Coded in python, Discord.py[Async]');
    embed.add_field(name = '**Discord.py**', value = 'Version ' + discord.__version__);
    embed.add_field(name = '**Default Prefix**', value = '`d;`');
    embed.add_field(name = '**Feedback/Support?**', value = 'Say `d;support <text>` OR `d;feedback <text>`')
    embed.add_field(name = '**Server Count**', value = str(len(client.servers)))
    embed.add_field(name = '**Member Count**', value = (len(set(client.get_all_members()))))
    await client.say(embed = embed)
#command19
@client.command(pass_context = True)
async def mute(ctx, member : discord.Member, mutetime, reason : str):
    if not ctx.message.author.server_permissions.administrator:
        return await client.say("Only admins can mute people........")

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("" + member.mention + " has been muted for " + mutetime + "!")
    await asyncio.sleep(int(mutetime))
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    
#command20
@client.command(pass_context = True)
async def unmute(ctx, *, member : discord.Member):
    await client.say("You will have to do it yourself [Remove muted role] or wait for the mutetime to end lol.")

#command21
@client.command(pass_context=True, aliases=['music'])
async def randommusic(ctx):
    song = ['https://www.youtube.com/watch?v=HCjNJDNzw8Y', 'https://www.youtube.com/watch?v=qBB_QOZNEdc', 'https://www.youtube.com/watch?v=ugpvZ61CnD8', 'https://www.youtube.com/watch?v=O81P0dWo6yg', 'https://www.youtube.com/watch?v=Sw8tktgQwNs', 'https://www.youtube.com/watch?v=nMt7nMUcQRQ', 'https://www.youtube.com/watch?v=vicS7yysh8A', 'https://www.youtube.com/watch?v=IkYw6OSNhW8', 'https://www.youtube.com/watch?v=wf_sv-FIN0E', 'https://www.youtube.com/watch?v=ymq1WdGUcw8', 'https://www.youtube.com/watch?v=yU0tnrEk8H4', 'https://www.youtube.com/watch?v=gedMhBpceSU', 'https://www.youtube.com/watch?v=dH7iOGNBiJ8', 'https://www.youtube.com/watch?v=8wYIg7_u-Cc', 'https://www.youtube.com/watch?v=TzTfTuUR-00', 'https://www.youtube.com/watch?v=5pfDp6Wrf6Y', 'https://www.youtube.com/watch?v=eF8l2Lykmnw', 'https://www.youtube.com/watch?v=BuoOmPx1sqI', 'https://www.youtube.com/watch?v=76jARSWqcdM', 'https://www.youtube.com/watch?v=xYfn7MWU7TQ', 'https://www.youtube.com/watch?v=kSmMOsJmkfs', 'https://www.youtube.com/watch?v=iGLeGRciEaM', 'https://www.youtube.com/watch?v=mSegGCPxm4s', 'https://www.youtube.com/watch?v=IamAzj0Ogos', 'https://www.youtube.com/watch?v=UDEpRK8WL_I', 'https://www.youtube.com/watch?v=7ly0FT40Nbk', 'https://www.youtube.com/watch?v=btY0RF5E9pg', 'https://www.youtube.com/watch?v=fugQAnzL1uk', 'https://www.youtube.com/watch?v=MqUCDzom5Xw', 'https://www.youtube.com/watch?v=f2xGxd9xPYA', 'https://www.youtube.com/watch?v=jthE5swmSvY', 'https://www.youtube.com/watch?v=LE9_SBvoaZY', 'https://www.youtube.com/watch?v=8fFMjGs2mvs', 'https://www.youtube.com/watch?v=HoysDM9IeXM', 'https://www.youtube.com/watch?v=0C7d76j1dzU', 'https://www.youtube.com/watch?v=wnJ6LuUFpMo', 'https://www.youtube.com/watch?v=kJQP7kiw5Fk', 'https://www.youtube.com/watch?v=weeI1G46q0o']
    choice  = random.choice(song)
    await client.say('{}, here is your random music.\n'.format(ctx.message.author.name) + choice)

#command22
@client.command(pass_context=True)
async def setgame(ctx, *, game=None):

        server = ctx.message.server

        current_status = server.me.status if server is not None else None

        if ctx.message.author.id == 252031624441626635:
            await client.change_presence(game=discord.Game(name=game),status=current_status)


#command23
@client.command(pass_context = True)
async def clearnicks(ctx):
    if not ctx.message.authour.server_permissions.Manage_Roles:
        return
    else:
        
        try:
            for member in ctx.message.server.members:
                if member is not ctx.message.server.owner:
                    name = member.name
                    await client.change_nickname(member, name)
            await client.say("This server's nicknames have been cleared!")
        except Exception as e:
            if 'Privilege is too low' in str(e):
                return await client.say("Missing permissions/Low in role hierarchy")

#command24
@client.command(pass_context = True)
async def kill(ctx, *, member : discord.Member):
    a = ['https://media.giphy.com/media/kOA5F569qO4RG/giphy.gif', 'https://media.giphy.com/media/3orif4KBFFVSc9ydAk/giphy.gif', 'https://media.giphy.com/media/uapW9a9jH3UvC/giphy.gif', 'https://media.giphy.com/media/S4DbvGJggL0pG/giphy.gif']
    b = random.choice(a)
    c = ['https://media.giphy.com/media/zqdbOacOP9Djy/giphy.gif', 'https://media.giphy.com/media/jSxK33dwEMbkY/giphy.gif']
    d = random.choice(c)
    if member.id == 358581526494969856:
        return await client.say("Muahahahaha!! Trying to kill me idiot?")
    if not member.id == ctx.message.author.id:
        e = discord.Embed(title = '{} has killed %s'.format(ctx.message.author.name) %member.name, colour = 0x1abc9c)
        e.set_image(url = b)
        return await client.say(embed=e)
    else:
        e = discord.Embed(title = '{} commited suicide!'.format(member.name), color = 0x1abc9c)
        e.set_image(url = d)
        return await client.say(embed=e)

#command25
@client.command(pass_context=True)
async def uptime(ctx): # Displays how long the bot has been running
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    t = "I've been online for %d weeks, %d days, %d hours, %d minutes, %d seconds" % (week, day, hour, minute, second) 
    embed = discord.Embed(title = 'Bot Uptime', description = t, color = 0x1abc9c)
    await client.say(embed = embed)

#command26
@client.command(pass_context=True, no_pm=True)
async def servermute(ctx, user : discord.Member, num, reason : str):
    if not ctx.message.author.server_permissions.manage_roles:
        return await client.say ("Not enough permissions.......")
    number = int(num)
    numbu = num * 60
    await client.add_roles(user, discord.utils.get(ctx.message.server.roles, name='Muted'))
    e = discord.Embed(title = 'Muted!', description = "**{}** has been muted for %s minutes. Reason: {}".format(user.name, reason)%number, color = 0x1abc9c)
    await client.say(embed=e)
    await asyncio.sleep(int(numbu))
    await client.remove_roles(user, discord.utils.get(ctx.message.server.roles, name='Muted'))

#command27
@client.command(pass_context=True)
async def ban(ctx, user : discord.Member=None, *, reason : str=None):
    if not ctx.message.author.id == '252031624441626635':
        if not ctx.message.author.server_permissions.ban_members:
            return
    if not user:
        return await client.say("Specify a user to ban!")
    embed = discord.Embed(title = 'Banned!', description = "{} got banned for reason - %s".format(user.name) %reason, colour = 0x1abc9c)
    try:
        await client.ban(user)
        await client.message(member, "You have been banned from " + ctx.message.server.name)

    except Exception as e:
        if 'Permissions too low' in str(e):
            await client.say("You/the bot does not have sufficient permissions!")
    await client.say(embed=embed)

        
#command28
@client.command(pass_context=True)
async def add(left : int, right : int):
    await client.say(left + right)

#command29
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('Hi'):
        msg = await client.send_message(message.channel, 'Hello')
        await asyncio.sleep(3)
        await message.edit(msg, 'Why the hell are you talking to a bot anyways?')
    await client.process_commands(message)

#command30
@client.command()
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await client.say(random.choice(choices))

#command31
@client.command(pass_context=True)
async def embed(ctx, *, text=None):
    if not text:
        text = 'What do I Put here'
    else:
        text = text.replace(' ',' ')
    channel = ctx.message.channel
    embed = discord.Embed(description = "**{}**".format(text), color = 0x1abc9c)
    embed.set_footer(text = "- %s" %ctx.message.author.name)
    embed.set_author(name = "--", icon_url = ctx.message.author.avatar_url)
    return await client.say(embed = embed)

#command32

#command33
@client.command(pass_context=True, aliases=['say', 'echo'])
async def repeat(ctx,*,repeat=None):
    nome = ctx.message.author
    if not repeat:
        await client.say("Repeat what you idiot <:fp:380000715952619532> ?")
    else:
        repeat = repeat.replace(' ',' ')
        channel = ctx.message.channel
        await client.say("%s says : {}".format(repeat) %nome.name)
        await client.delete_message(ctx.message)


#command33
@client.command(pass_context=True)
async def version(ctx):
    embed = discord.Embed(title= 'Version', colour = 0x1abc9c)
    embed.add_field(name = 'Version', value = botversion)
    embed.add_field(name = 'Changes', value = 'Bugs fixed.\nAdded some owner-only commands.')
    await client.say(embed=embed)

#command34
@client.command(pass_context=True, aliases=['urban'])
async def ud(ctx, *, msg):
    word = msg.replace(' ', '_')
    api = "http://api.urbandictionary.com/v0/define"
    async with aiohttp.ClientSession() as session:
        async with session.get(api, params={'term': word}) as r:
            response = await r.json()

        if len(response["list"]) == 0:
            x = "Could not find that word!"
            embed=discord.Embed(title='Nope', color=0x1abc9c)
            embed.description = x
            await client.say(embed=embed)
            
        else:
            embed = discord.Embed(title='Urban Dictionary - ' + word, color=0x1abc9c)
            embed.description = response['list'][0]['definition']
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/B4lcjSHEDA8RcuizSOAdc92ithHovZT6WkRAX-da_6o/https/erisbot.com/assets/emojis/urbandictionary.png')
            embed.add_field(name="Examples:", value=response['list'][0]["example"][:1000])
            embed.set_footer(text="Source: {}, UrbanDictionary".format('https://urbandictionary.com/define.php?term=' + msg))
            await client.say(embed=embed)
                
#command36
@client.command(pass_context = True)
async def shutdown(ctx):
    if ctx.message.author.id == '252031624441626635':
        await client.say("[yes/no] Are you sure you want to stop the bot?\nIt will have to be started again manually.")
        answer = await client.wait_for_message(timeout = 30, author=ctx.message.author)
        answer = str(answer)
        if answer.lower() in ("y", "yes"):
            await client.say("Shutting down...")
            await client.logout()
            exit()
        elif answer.lower() in ("n", "no"):
            await client.say("Bot not stopped!")
        else:
            await client.say("Invalid answer! Bot not stopped!")
    else:
        await client.say("You don't have permission to do that!")

#command37
@client.command(pass_context=True)
async def stream(ctx, *, name:str):
    if not ctx.message.author.id == 252031624441626635:
        return await client.say("No I won't.")
    await client.change_presence(game=discord.Game(name=name, type=1, url="https://www.twitch.tv/dot4447"))
    await client.say("Now streaming `%s`"%name)
#command28
@client.command(pass_context = True, aliases =['feedback', 'contactowner'])
async def support(ctx, *, message : str):
    invite = await client.create_invite(ctx.message.channel,max_uses=1,xkcd=True)
    if message is None:
        return
        await client.say(ctx.message.channel, ctx.message.author.mention + " Please enter some feedback.")
    else:
        msg = "**NAEM** : {}\n**SERBER**: {}\n**FEDBECK**: {}\n**Invite**: {}".format(ctx.message.author, ctx.message.server, message, invite.url)
        await client.send_message(discord.User(id="252031624441626635"), msg)
        return await client.say(ctx.message.author.mention + " Your feedback is sent to Dot. It will be taken into consideration")

#command29
@client.command(pass_context=True)
async def spam(ctx, user:discord.Member=None):
    if not ctx.message.author.id == '252031624441626635':
        return
    if not user:
        user = ctx.message.author
    for x in range(51):
        await client.send_message(user, "Spam")
    await client.say("Done.")
    await client.send_message(user, "That was 50 messages. Thank You, I'm done.")

#command30
@client.command(pass_context = True, aliases=['sinfo'])
async def serverinfo(ctx):
        server = ctx.message.server
        roles = [x.name for x in server.role_hierarchy]
        role_length = len(roles)
        roles = ', '.join(roles);
        channels = len(server.channels);
        time = str(server.created_at); time = time.split(' '); time= time[0];

        embed = discord.Embed(description= "Info on this server",title = ':thinking:', colour = 0x1abc9c);
        embed.set_thumbnail(url = server.icon_url);
        embed.add_field(name = '**Server Name**', value = server)
        embed.add_field(name = '**Server ID**', value = server.id)
        embed.add_field(name = '**Owner**', value = server.owner);
        embed.add_field(name = '**Owner ID**', value = server.owner.id)
        embed.add_field(name = '**Members**', value = server.member_count);
        embed.add_field(name = '**Text/Voice Channels**', value = channels);
        embed.add_field(name = '**Roles**', value = '%s'%role_length);
        embed.add_field(name = '**Server Region**', value = '%s'%server.region);
        embed.add_field(name = '**AFK Timeout(in seconds)**', value = server.afk_timeout);
        embed.add_field(name = '**AFK Channel**', value = server.afk_channel);
        embed.add_field(name = '**Verification Level**', value = server.verification_level)
        embed.add_field(name = '**Created on**', value = server.created_at.__format__('Date - %d %B %Y at time - %H:%M:%S'))
        
        await client.say(embed = embed);

#command31
@client.command(pass_context=True)
async def avatar(ctx, user: discord.Member = None):
    if not user:
        user = ctx.message.author
    if user.avatar_url[54:].startswith('a_'):
        x = 'https://cdn.discordapp.com/avatars/' + user.avatar_url[35:-10]
    else:
        x = user.avatar_url
    embed = discord.Embed(title = f"{user.name}'s avatar", colour = 0x1abc9c)
    embed.set_image(url = x)
    await client.say(embed = embed)




#command62
@client.command(pass_context=True)
async def virus(ctx,user: discord.Member=None,*,hack=None):
        name = ctx.message.author
        if not hack:
            hack = 'some'
        else:
            hack = hack.replace(' ',' ')
        channel = client.message.channel
        x = await client.send_message(channel, '``[¦¦¦                    ] / Getting {} virus ready.``'.format(hack))
        await asyncio.sleep(0.5)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦                ] - Getting {} virus ready..``'.format(hack))
        await asyncio.sleep(0.3)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦¦¦¦¦¦           ] \ Getting {} virus ready....``'.format(hack))
        await asyncio.sleep(1.2)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦¦¦¦¦¦¦¦         ] | Initializing.``')
        await asyncio.sleep(1)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦      ] / Initializing..``')
        await asyncio.sleep(1.5)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦   ] - {} virus Finishing.``'.format(hack))
        await asyncio.sleep(1)
        x = await message.edit(x,'``[¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦ ] \ {} virus Finishing..``'.format(hack))
        await asyncio.sleep(1)
        x = await message.edit(x,'``{} virus ready.``'.format(hack))
        await asyncio.sleep(1)
        x = await message.edit(x,'``Injecting virus.   |``')
        await asyncio.sleep(0.5)
        x = await message.edit(x,'``Injecting virus..  /``')
        await asyncio.sleep(0.5)
        x = await message.edit(x,'``Injecting virus... -``')
        await asyncio.sleep(0.5)
        x = await message.edit(x,'``Injecting virus....\``')
        await client.delete_message(x)
       
        if user:
            await client.say('`{} virus` successfully injected into **{}**\'s system.'.format(hack,user.name))
            await client.send_message(user,'**Alert!**\nYou may have been hacked. {} virus has been found in your system\'s operating system.\nThis kind of viruses are usually found with people like %s.\nPlease do something about your system'.format(hack)%ctx.message.author.name)
        else:
            await client.say('**{}** has hacked him/herself.'.format(name.name))
            await client.send_message(name,'**Alert!**\nYou may have been hacked. {} virus has been found in your system\'s operating system.\nThis kind of viruses are usually found with people like %s.\nPlease do something about your system'.format(hack)%ctx.message.author.name)

#command63
@client.command(pass_context = True)
async def whatis(ctx, user : discord.Member):
    if user.id == '252031624441626635':
        return await client.say("pr0")
    if user.id == '153601583869853698':
        await client.say("{} is an idiot".format(user.name))
    if user.id == ctx.message.server.owner.id:
        await client.say("This server's owner.")
    else:
        outcomes = ['a n00b', 'pr0', 'pretty uncool', 'not needed', 'something I don\'t think is allowed to say']
        choice = random.choice(outcomes)
        await client.say("{} is ".format(user.name) + choice + " I think. :thinking:")

#command64
@client.command(pass_context=True)
async def suicide(ctx):
    death = ['You jumped off a bridge =(', 'You shot yourself =(', 'You drank poison =(', 'You asked your friend to kill you =(', 'You hung yourself =(', 'You did some shit that ended up killing you =(']
    choice = random.choice(death)
    await client.say(choice)
    await client.say("May your soul rest in peace. :om_symbol:")
       
#command67
@client.command(pass_context=True)
async def servericon(ctx):
    server = ctx.message.server
    icon = discord.Embed(title = '{}\'s icon'.format(server.name), color = 0x1abc9c)
    icon.set_image(url = server.icon_url)
    return await client.say(embed=icon)

#command68
@client.command(pass_context=True)
async def roles(ctx):
    server = ctx.message.server
    roles = "\n".join([x.name for x in server.role_hierarchy])
    await client.say("Check your DMs for this server's role list.")
    e = discord.Embed(title = '{}\'s Roles'.format(server.name), description = roles, color = 0x1abc9c)
    await client.whisper(embed=e)
#command69
@client.command(pass_context=True)
async def roleinfo(ctx, *, role : discord.Role):
    rid = role.id
    rname = role.name
    perms = role.permissions
    color = role.color
    if role.hoist:
        hoist = "Yes"
    if not role.hoist:
        hoist = "No"
    if role.mentionable:
        ment = "Yes"
    if not role.mentionable:
        ment = "No"
    ro = discord.Embed(title = rname, colour = 0x1abc9c)
    ro.add_field(name = 'Role ID', value = rid);
    ro.add_field(name = 'Role Colour', value = color)
    ro.add_field(name = 'Visible seperately', value = hoist);
    ro.add_field(name = 'Mentionable', value = ment)
    return await client.say(embed=ro)

    
#command70
@client.command(pass_context=True)
async def rps(ctx, *, choice : str):
    if not choice:
        return await client.say("Select something.")
    
    choice = choice.replace(' ','_')

    m2 = ("I win!!", "Another win for me!", "You lost!")
    result = random.choice(m2)
    
    if choice == 'rock':
        await client.say("I choose paper")
        await client.say(result)
    elif choice == 'paper':
        await client.say("I choose scissors")
        await client.say(result)
    elif choice == 'scissors':
        await client.say("I choose rock")
        await client.say(result)
    elif choice == 'your mom':
        await client.say("No your mom")
        await client.say(result)
    else:
        await client.say("No, I ain't playing.")
    


#command71
@client.event
async def on_message(message):
    if message.content.startswith('delete'):
        embed = discord.Embed(title = 'DELETEEEEEE', color = 0x1abc9c)
        embed.set_image(url = 'https://zippy.gfycat.com/UnsungLonelyChafer.gif')
        await client.delete_message(message)
        await client.send_message(message.channel, embed=embed)
    await client.process_commands(message)
    
#command72
@client.event
async def on_message(message):
    if message.content.startswith('DELETE'):
        embed = discord.Embed(title = 'DELETEEEEEE', color = 0x1abc9c)
        embed.set_image(url = 'https://zippy.gfycat.com/UnsungLonelyChafer.gif')
        await client.delete_message(message)
        await client.send_message(message.channel, embed=embed)
    await client.process_commands(message)


#command73

#command74
@client.command(pass_context=True)
async def slap(ctx, member : discord.Member, *, reason=None):
    gif = ('https://cdn.discordapp.com/attachments/373486650812268546/381451940682399744/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452206035173376/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452371953451010/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452480589987840/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452594247106560/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452777282600960/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452861856284673/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381452956177924096/slap.gif', 'https://cdn.discordapp.com/attachments/373486650812268546/381453063220887553/slap.gif')
    gif2 = random.choice(gif)
    if reason:
        await client.say('%s , you were slapped by {} because {}. \n{}'.format(ctx.message.author.name, reason, gif2) %member.mention)
    if not reason:
        await client.say('%s , you were slapped by {}. \n{}'.format(ctx.message.author.name, gif2) %member.mention)


    
#command75
@client.command(pass_context=True, aliases=['text-art'])
async def ascii(ctx, *, text : str):
    myfont = ImageFont.truetype("verdanab.ttf", 12)
    size = myfont.getsize(text)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white", font=myfont)
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','#'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    await client.say("```\n" + ( "\n".join(strings)) + "\n ```")
    

#command76
@client.command(pass_context=True)
async def serverinvite(ctx):
    invite = await client.create_invite(ctx.message.channel,max_uses=1,xkcd=True)
    embed = discord.Embed(title = 'Invite', description = 'I made an invite with 1 limiteed use.', color = 0x1abc9c)
    embed.add_field(name = 'This is the invite', value = invite)
    await client.say(embed=embed)

#command77
@client.command(pass_context=True)
async def cat(ctx):

    catPicture = requests.get('http://thecatapi.com/api/images/get.php')
    if catPicture.status_code == 200:
        catPicture = catPicture.url
    embed = discord.Embed(title = "Here you go.", color = 0x1abc9c)
    embed.set_image(url = catPicture)
    await client.say(embed=embed)

                
#command78
@client.command(pass_context=True)
async def dog(ctx):
    api = "https://api.thedogapi.co.uk/v2/dog.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            if r.status == 200:
                response = await r.json()
                embed = discord.Embed(title = "Here you go.", color = 0x1abc9c)
                embed.set_image(url = response['data'][0]["url"])
                await client.say(embed = embed)

#Run
client.run("NDU1MDkxOTI1NDM1OTQwODY0.D0rgsQ.6It2hnmdP02OK7ovPfQLETTQ2ns")
