import discord
from discord.ext.commands import Bot
from discord.ext import commands
import json
import os.path
import datetime
import time
import asyncio
from shutil import copyfile
import json
import os
import copy
import subprocess
import random
from random import randint
import requests
import logging
import aiohttp


client = Bot("d;")
TOKEN = "NDU0OTg3MDUwNjI2NTgwNDgw.Df1q6w.e99bENzeK5NfPYo4V7UoyjEP5cE"

@client.event
async def on_ready():
    print(client.user.name)
    print("===================")

@client.command()
async def ping():
    pingtime = time.time()
    embed = discord.Embed(Title = 'Ping', color = 0x1abc9c)
    embed.add_field(name = 'Pong', value = 'Calculating...')
    ping3 = await client.say(embed=embed)
    ping2 = time.time() - pingtime
    ping1 = discord.Embed(Title = 'Ping', color = 0x1abc9c)
    ping1.add_field(name = 'Pong', value = "{} seconds".format(ping2)   )
    await client.edit_message(ping3, embed = ping1)

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
            expp = members[user.name]['exp']
            e = discord.Embed(title = "{}'s Experience".format(user.name), colour = 0x1abc9c)
            e.add_field(name = "Exp", value = expp)
            e.add_field(name = "Total Messages", value = expp / 3)
            await client.say(embed=e)
    else:
        return

@client.command(pass_context=True, aliases=['gb'])
async def getbans(ctx):
    x = await server.bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "The following are banned here", description = x, color = 0x1abc9c)
    return await client.say(embed = embed)

@client.command(pass_context=True, aliases=['k'])
async def kick(ctx, *, member : discord.Member = None):
    if not ctx.message.author.bot:
        if not ctx.message.author.server_permissions.administrator:
            return
 
        if not member:
            return await client.say(ctx.message.author.mention + "Frikin specify a user to kick!")
        try:
            await client.kick(member)
        except Exception as e:
            if 'Privilege is too low' in str(e):
                return await client.say(":x: The bot/you do not have permissions to do shit like this")
 
        embed = discord.Embed(description = "**%s** got a boot!!!"%member.name, color = 0x1abc9c)
        return await client.say(embed = embed)

@client.command(pass_context = True, aliases=['purge'])
async def clear(ctx, number):
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

@client.command(pass_context = True, aliases=['id'])
async def ID(ctx, user : discord.Member=None):
    if not user:
        user = ctx.message.author
        
    embed = discord.Embed(title = user.name, colour = 0x1abc9c);
    embed.set_thumbnail(url = user.avatar_url);
    embed.add_field(name = 'ID', value = user.id)
    await client.say(embed=embed)

@client.command(pass_context=True, aliases = ['coin', 'coinflip'])
async def flip(ctx):
    e = discord.Embed(title = ".....and...flip!", color = 0x1abc9c)
    e.set_image(url="https://media.giphy.com/media/6jqfXikz9yzhS/giphy.gif")
    one = await client.say(embed=e)
    asyncio.sleep(8)
    choose = ("It's Tails!", "It's Heads!")
    choice = random.choice(choose)
    if choice == "It's Tails!":
        choice2 = "https://cdn.discordapp.com/attachments/370616847328083968/371566223256715266/Tails.png"
    else:
        choice2 = "https://cdn.discordapp.com/attachments/370616847328083968/371566837701410828/Heads.png"
    e2 = discord.Embed(title = choice, color = 0x1abc9c)
    e2.set_image(url=choice2)
    await client.edit_message(one, embed=e2)

@client.command(pass_context=True, aliases=['dice'])
async def roll(ctx, sides : int=None):
    if not sides:
        sides = 6
    choice  = random.randint(1,[sides])
    embed = discord.Embed(title = 'Dice', description = 'Rolled a dice with %s, the outcome is {}'.format(choice) %sides, colour = 0x1abc9c)
    await client.say(embed=embed)

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

@client.command(pass_context = True)
async def kill(ctx, *, member : discord.Member):
    a = ['https://media.giphy.com/media/kOA5F569qO4RG/giphy.gif', 'https://media.giphy.com/media/3orif4KBFFVSc9ydAk/giphy.gif', 'https://media.giphy.com/media/uapW9a9jH3UvC/giphy.gif', 'https://media.giphy.com/media/S4DbvGJggL0pG/giphy.gif']
    b = random.choice(a)
    c = ['https://media.giphy.com/media/zqdbOacOP9Djy/giphy.gif', 'https://media.giphy.com/media/jSxK33dwEMbkY/giphy.gif']
    d = random.choice(c)
    if member.id == client.id:
        return await client.say("Muahahahaha!! Trying to kill me idiot?")
    if member.id == ctx.message.author.id:
        e = discord.Embed(title = '{} has killed %s'.format(ctx.message.author.name) %member.name, colour = 0x1abc9c)
        e.set_image(url = d)
        return await client.say(embed=e)
    else:
        e = discord.Embed(title = '{} commited suicide!'.format(member.name), color = 0x1abc9c)
        e.set_image(url = b)
        return await client.say(embed=e)

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

@client.command(pass_context=True)
async def ban(ctx, user : discord.Member, *, reason : str):
    if not ctx.message.author.server_permissions.ban_members:
        return
    if not user:
        return await client.say("Specify a user to ban!")
    embed = discord.Embed(title = 'Banned!', description = "{} got banned for reason - %s".format(user.name) %reason, colour = 0x1abc9c)
    try:
        await client(user)
    except Exception as e:
        if 'Permissions too low' in str(e):
            await client.say("You/the bot does not have sufficient permissions!")
    await client.say(embed=embed)

        
@client.command(pass_context=True)
async def add(left : int, right : int):
    await client.say(left + right)

client.command(pass_context=True)
async def multiply(left : int, right : int):
    await client.say(left * right)

@client.command(pass_context=True)
async def subtract(left : int, right : int, aliases=['minus']):
    await client.say(left - right)

@client.command(pass_context=True)
async def divide(left : int, right : int):
    await client.say(left / right)

@client.command()
async def choose(*, choices : str):
    await client.say(random.choice(choices))

@client.command(pass_context=True)
async def embed(ctx, *, text=None):
    if not text:
        text = 'What do I Put here'
    else:
        text = text.replace(' ',' ')
    channel = ctx.message.channel
    embed = discord.Embed(description = "**{}**".format(text), color = 0x1abc9c)
    embed.set_author(name = "{}".format(ctx.message.author.name))
    await client.say(embed = embed)

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
            embed.set_footer(text="Tags: " + ', '.join(response['tags']))
            await client.say(embed=embed)

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
        
        await client.say(embed = embed)

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

@client.command(pass_context = True, aliases=['8ball'])
async def eightball(ctx):
    result = ["Yes", "No", "Definitely", "Thinking in process :Thinking:", "Let me think....", "Why not?", "Try again later", "Nope", "What makes you think that will happen n00b.", "Ye", "I'm awesome", "Dot is amazing", "Try again later maybe?"]
    choice = random.choice(result)
    await client.say(choice)

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
            return await client.send_message(name,'**Alert!**\nYou may have been hacked. {} virus has been found in your system\'s operating system.\nThis kind of viruses are usually found with people like %s.\nPlease do something about your system'.format(hack)%ctx.message.author.name)

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
        return await client.say("{} is ".format(user.name) + choice + " I think. :thinking:")

@client.command(pass_context=True)
async def suicide(ctx):
    death = ['You jumped off a bridge =(', 'You shot yourself =(', 'You drank poison =(', 'You asked your friend to kill you =(', 'You hung yourself =(', 'You did some shit that ended up killing you =(']
    choice = random.choice(death)
    await client.say(choice)
    return await client.say("May your soul rest in peace. :om_symbol:")

@client.command(pass_context=True)
async def servericon(ctx):
    server = ctx.message.server
    icon = discord.Embed(title = '{}\'s icon'.format(server.name), color = 0x1abc9c)
    icon.set_image(url = server.icon_url)
    return await client.say(embed=icon)

@client.command(pass_context=True)
async def roles(ctx):
    server = ctx.message.server
    roles = "\n".join([x.name for x in server.role_hierarchy])
    await client.say("Check your DMs for this server's role list.")
    e = discord.Embed(title = '{}\'s Roles'.format(server.name), description = roles, color = 0x1abc9c)
    return await client.whisper(embed=e)

@client.command(pass_context=True)
async def invite(ctx):
    invite = await client.create_invite(ctx.message.channel,max_uses=1,xkcd=True)
    e = discord.Embed(title = 'Server Invite', color = 0x1abc9c)
    e.add_field(name = 'I made an invite to this server with 1 max use.', value = invite)
    await client.say(embed=e)

@client.command(pass_context=True)
async def dog(ctx):
    api = "https://api.thedogapi.co.uk/v2/dog.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as r:
            if r.status == 200:
                response = await r.json()
                embed = discord.Embed(title = "Woof", color = 0x1abc9c)
                embed.set_image(url = response['data'][0]["url"])
                await client.say(embed = embed)

@client.command(pass_context=True)
async def cat(ctx):

    catPicture = requests.get('http://thecatapi.com/api/images/get.php')
    if catPicture.status_code == 200:
        catPicture = catPicture.url
    embed = discord.Embed(title = "Meow", color = 0x1abc9c)
    embed.set_image(url = catPicture)
    await client.say(embed=embed)

if not os.environ.get('TOKEN'):
    print("no token found!")
client.run(os.environ.get('TOKEN').strip('"'))
