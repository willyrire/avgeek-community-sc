from discord.ui import Button, View
import discord
from discord import option
from discord.utils import get
import os
from datetime import datetime
import datetime
import time
import mysql.connector
from dotenv import load_dotenv
from random import randint
import string
import random
import base64
load_dotenv()

token = os.getenv('TOKEN')
sqlpswd = os.getenv('SQLPSWD1')
sqlhost = os.getenv('SQLHOST1')
sqlusr = os.getenv('SQLUSER1')
sqldb = os.getenv('SQLDB1')
# secdbpass = os.getenv('SQLPSWD2')
# secdbhost = os.getenv('SQLHOST2')
# secdbusr = os.getenv('SQLUSER2')
# secdb = os.getenv('SQLDB2')


# date_time = datetime.datetime.now()
# ctt = int(time.mktime(date_time.timetuple()))


###################COLOR VARIABLES###################
lightblue = 0x5ca3ff
red = 0xff0000
orange = 0xffa500
yellow = 0xffff00
greensuccess = 0x81fe8f
rederror = 0xfe8181
white = 0xffffff
###################COLOR VARIABLES###################

#bot
bot = discord.Bot(command_prefix=".", intents = discord.Intents.all(), debug_guilds=[1001644433831366716])
# cmds = commands.bot(command_prefix='.', intents=discord.Intents.all())

print()
print("Loading Commands...")
print("Trying to connect to first database...")
mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
bdd = mydb.cursor()
print("Connection Success")
print("Trying to connect to second database...")
# mydb = mysql.connector.connect(host=secdbhost,user=secdbusr,password=secdbpass,database=secdb)
# bdd = mydb.cursor()
print("Connection success")
print("Loading Modules...")

######################EVENTS######################

#####################UTIL VAR#####################

fem = discord.Embed # discord embed

##################################################

@bot.event # When bot is online and ready to use
async def on_ready():
    print()
    print("                _____           _       _____                                      _ _         ")
    print("     /\        / ____|         | |     / ____|                                    (_) |        ")
    print("    /  \__   _| |  __  ___  ___| | __ | |     ___  _ __ ___  _ __ ___  _   _ _ __  _| |_ _   _ ")
    print("   / /\ \ \ / / | |_ |/ _ \/ _ \ |/ / | |    / _ \| '_ ` _ \| '_ ` _ \| | | | '_ \| | __| | | |")
    print("  / ____ \ V /| |__| |  __/  __/   <  | |___| (_) | | | | | | | | | | | |_| | | | | | |_| |_| |")
    print(" /_/    \_\_/  \_____|\___|\___|_|\_\  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|_|\__|\__, |")
    print("                                                                                          __/ |")
    print("                                                                                         |___/ ")
    print("===============================================================================================")
    print()
    print()
@bot.event # Quand quelqu'un rejoind le serveur
async def on_member_join(member):
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    date_time = datetime.datetime.now()
    ctt = int(time.mktime(date_time.timetuple()))
    role = discord.utils.get(member.guild.roles, id=1002578714309165066)
    await member.add_roles(role)
    ausr = member.name
    atag = member.discriminator
    aid = member.id
    sql = f"SELECT * FROM avkick WHERE usrid = '{aid}' AND expiration > {ctt}"
    bdd.execute(sql)
    results = bdd.fetchall()
    row = bdd.rowcount
    if row == 0:
        # 2nd check to see if the user is temp banned
        sql = f"SELECT * FROM avtbans WHERE usrid = {aid} AND expiration > {ctt}"
        bdd.execute(sql)
        result = bdd.fetchall()
        row = bdd.rowcount
        if row == 0:
            channel = bot.get_channel(1026620022514262126)
            print(f"[System] {ausr}#{atag} A Rejoind le Serveur")
            await channel.send(f"<@{aid}>",embed=discord.Embed(title="🛬 CAVC's ATC 🚁", description=f"""🎤 Air {ausr} cleared to land runway general left, take taxyway <#1012877013629018204> to leave the runway.
Welcome {ausr}#{atag} in the Avgeek Community Server ! Here you can talk with other people but, respect <#1012877013629018204> and have fun !""", color=lightblue))
        elif row >=1:
            for data in result:
                usrid = data[0]
                date = data[1]
                mod = data[2]
                banid = data[3]
                reason = data[4]
                expiration = data[6]
                duration = data[7]
            mod = bot.get_user(mod)
            channel = bot.get_channel(1026620022514262126)
            print(f"[System] {ausr}#{atag} Joined the server but he has an active tempban")
            await channel.send(f"<@{aid}>",embed=discord.Embed(title="🛬Uh oh 🛫", description=f"""**{ausr}'s pov :** `Go Around Windshear Ahead`,
`Windshear, windshear, go around, windshear ahead`,
**Also {ausr}'s pov :** Going around windshear""", color=red), delete_after=30)
            await member.send(embed=discord.Embed(title="Banned", description=f"""Hello <@{usrid}>,
You got kicked out of the server cause you have an active ban. That's mean, you have a ban that isnt expired so we cant let you in until its expired. The ban isnt permanently ! Its only temporaly. Sadly, you have no way for the moment to appeal a temporary ban. The only way to get back the access to the server is to wait.

Keep in mind that we like our channels to be calm and chill, so, if you got banned, but temporary, that's probably because you didnt respected our rules. 

**==========Ban Infos==========**

**Ban Type :** Temporary
**User ID :** {usrid}
**Date :** <t:{date}>
**Moderator :** {mod}

**Ban ID :**```{banid}```*Note : the ban id is used to report a abuse from a moderator, you can report a abuse only one time per ban id*

**Reason :**```{reason}```
**Expiration :** <t:{expiration}>
**Duration of this ban :** {duration} day(s)

**===============================**

**You will be allowed to join the server** <t:{expiration}:R>

**Here is a link for you to join the server when your ban is ended :**
[clicking here](https://discord.gg/WGVneaZyPw) or here https://discord.gg/WGVneaZyPw 
Also, make sure to read <#1012877013629018204>
""", color=red))
            await member.guild.kick(member)
    elif row >=1:
        for data in results:
            usrid = data[0]
            date = data[1]
            mod = data[2]
            kickid = data[3]
            reason = data[4]
            expiration = data[6]
        mod = bot.get_user(mod)
        channel = bot.get_channel(1026620022514262126)
        print(f"[System] {ausr}#{atag} Joined the server but his kick cooldown isnt ended so going around")
        await channel.send(f"<@{aid}>",embed=discord.Embed(title="🛬Oh no 🛫", description=f"""{ausr} joined the server but there was an airplane on the runway GO AROUND !""", color=yellow), delete_after=30)
        await member.send(embed=discord.Embed(title="User Kicked", description=f"""Hello <@{usrid}>,
Because you recently got kicked and it's doing 15 minutes since you got kicked, you cant join right now.

In AvGeek Community, we realy like to keep our channel chill, cool and fun, and, to prevent you to continue making trouble, you arent allowed to join the server until 15 minutes after your kick. We doing this to bring back channels to calm. Hope you understand :)

**========Infos About your Recent Kick========**

**User ID :** {usrid}
**Date :** <t:{date}> | <t:{date}:R>
**Moderator :** {mod}

**Kick ID :**```{kickid}```*Note : The kick id can be used to report the abuse of a moderator. The report need to be made as fast as possible when you are allowed to join back*

**Reason :**```{reason}```
**Expiration :** <t:{expiration}>

**======================================**

**You Will be allowed to join the server** <t:{expiration}:R>

**When the 15 minutes is ended you can join back by [clicking here](https://discord.gg/WGVneaZyPw) or here https://discord.gg/WGVneaZyPw ** Also, make sure to read <#1012877013629018204>""", color=red))
        await member.guild.kick(member)

@bot.event # Quand quelqu'un quitte le serveur
async def on_member_remove(member):
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    date_time = datetime.datetime.now()
    ctt = int(time.mktime(date_time.timetuple()))
    ausr = member.name
    atag = member.discriminator
    aid = member.id
    sql = f"SELECT * FROM avkick WHERE usrid = '{aid}' AND expiration > {ctt}"
    bdd.execute(sql)
    results = bdd.fetchall()
    row = bdd.rowcount
    if row == 0:
        ausr = member.name
        atag = member.discriminator
        aid = member.id
        channel = bot.get_channel(1026620022514262126)
        print(f"[System] {ausr}#{atag} A Quitter le Serveur")
        await channel.send(f"<@{aid}>",embed=discord.Embed(title="🛬 CAVC's ATC 🚁", description=f"""🎤 Air {ausr} cleared to takeoff runway 06L left, hope you had a nice experience at Avgeek Community airport !""", color=lightblue))


@bot.event
async def on_raw_reaction_add(reaction):
    guild_id = reaction.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
    msgid = 1026698293973098568
    rmsgid = reaction.message_id
    ausr = get(guild.members, id=reaction.user_id)
    if reaction.emoji.name == '📷':
        if msgid == rmsgid:
            member = reaction.member
            if member is not None:
                role = discord.utils.get(guild.roles, name="{📷} PlaneSpotter")
                await member.add_roles(role)
                channel = bot.get_channel(1026930615477604404)
                await channel.send(f"```[System] Role (📷) PlaneSpotter added to {ausr}```")
                print(f"[System] Role Plane Spotter added to {ausr}")
    elif reaction.emoji.name == '⚜':
        if msgid == rmsgid:
            member = reaction.member
            if member is not None:
                role = discord.utils.get(guild.roles, name="{⚜} Quebecois")
                await member.add_roles(role)
                channel = bot.get_channel(1026930615477604404)
                await channel.send(f"```[System] Role (⚜) Quebecois added to {ausr}```")
                print(f"[System] Role Quebecois added to {ausr}")
@bot.event
async def on_raw_reaction_remove(reaction):
    guild_id = reaction.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
    msgid = 1026698293973098568
    rmsgid = reaction.message_id
    ausr = get(guild.members, id=reaction.user_id)
    if reaction.emoji.name == '📷':
        if msgid == rmsgid:
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                role = discord.utils.get(guild.roles, name="{📷} PlaneSpotter")
                await member.remove_roles(role)
                channel = bot.get_channel(1026930615477604404)
                await channel.send(f"```[System] Role (📷) PlaneSpotter removed from {ausr}```")
                print(f"[System] Role Plane Spotter removed from {ausr}")
    elif reaction.emoji.name == '⚜':
        if msgid == rmsgid:
            member = get(guild.members, id=reaction.user_id)
            if member is not None:
                role = discord.utils.get(guild.roles, name="{⚜} Quebecois")
                await member.remove_roles(role)
                channel = bot.get_channel(1026930615477604404)
                await channel.send(f"```[System] Role (⚜) Quebecois removed from {ausr}```")
                print(f"[System] Role Québécois removed from {ausr}")

@bot.event 
async def on_message(ctx):
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    aid = ctx.author.id
    bdd.execute(f"SELECT * FROM avbank WHERE usrid = {aid}")
    result = bdd.fetchall()
    row = bdd.rowcount
    if row == 0:
        bdd.execute(f"INSERT INTO avbank(usrid) VALUES({aid})")
        mydb.commit()
        bdd.execute(f"INSERT INTO avbanksettings(usrid) VALUES({aid})")
        mydb.commit()
######################EVENTS######################
#####################COMMANDS#####################



@bot.command()# Send a embed message
async def sendembed(ctx, title, description):
    role = discord.utils.get(ctx.guild.roles, name="emp")
    # data that are required in all commands
    ar = ctx.author.roles
    aid = ctx.author.id
    ausr = ctx.author.name
    atag = ctx.author.discriminator
    title = str(title)
    desc = str(description)
    if role in ar:

        await ctx.respond("Your embed message got successfully sent. This message will auto delete in 5 seconds", delete_after=5)
        await ctx.send(embed=discord.Embed(title=title, description=desc, color=red))
        print(f"[System] {ausr}#{atag} used the command send embed")
    else:
        await ctx.respond(embed=discord.Embed(title="Error", description="You need the role <@&1026610612505169930> to be able to use this command", color=red))

@bot.command() # send the role reaction message
async def rrm(ctx):
    role = discord.utils.get(ctx.guild.roles, name="emp")
    # data that are required in all commands
    ar = ctx.author.roles
    if role in ar:
        await ctx.respond("e", delete_after=1)
        msg = await ctx.send(embed=discord.Embed(title="Role Reaction",description="""To Receive a Specific Role, you just need to react with the reactions !
📷 For the role <@&1012449581444902954>
⚜ For the role <@&1012491712783978537>""",color=lightblue))
        await msg.add_reaction("📷")
        await msg.add_reaction("⚜")
    else:
        await ctx.respond(embed=discord.Embed(title="Error", description="You need the role <@&1026610612505169930> to be able to use this command", color=red))


#########MODERATION#########

#|------------------------------------------------------------------|
#| Role Name                     |       Role Id                    |
#|------------------------------------------------------------------|
#| {🛡} Modérateur              | 1001649319390228581              |
#|------------------------------------------------------------------|
#| {⚔} Modérateur+              | 1026225756562538517              |
#|------------------------------------------------------------------|

@bot.command(description="Warn someone that didn't respected rules") # command warn
async def warn(ctx, user : discord.User, reason):
    modo = discord.utils.get(ctx.guild.roles, name="{🛡} Modérateur")
    modop = discord.utils.get(ctx.guild.roles, name="{⚔} Modérateur+")
    aid = ctx.author.id
    ausr = ctx.author.name
    ar = ctx.author.roles
    if modo in ar or modop in ar:
        usrid = user.id # id of the user that got warned
        usrname = str(user) # the username of the warned user
        date_time = datetime.datetime.now()
        ctt = int(time.mktime(date_time.timetuple()))
        reason = str(reason)
        usrroles = user.roles
        if modo in usrroles or modop in usrroles:
            await ctx.respond(embed=discord.Embed(title="Error", description="You can't use this command on a moderator", color=red))
        else:
            wrandint = randint(100000000000,9999999999999)
            warnid = f"AG{wrandint}"
            mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
            bdd = mydb.cursor()
            sql = "INSERT INTO avwarns(`usrid`, `date`, `modid`, `reason`, `warnid`) VALUES(%s, %s, %s, %s, %s)"
            val = (f'{usrid}', f'{ctt}', f'{aid}', f'{reason}', f'{warnid}')
            bdd.execute(sql, val)
            mydb.commit()
            texpi = datetime.datetime.fromtimestamp(ctt)
            date_time = texpi.strftime("%m/%d/%Y, %H:%M:%S")
            await ctx.respond(embed=discord.Embed(title="User Warned", description=f"""**User :** <@{usrid}>
**Moderator :** <@{aid}>
**Reason :**```{reason}```**Warn ID :** {warnid}""",color=yellow))
            channel = bot.get_channel(1026954875625537648)
            await channel.send(embed=discord.Embed(title="User Warned", description=f"""**User ID :** {usrid}
**User :** {usrname}
**Date :** {date_time}
**Moderator :** <@{aid}>
**Reason :**```{reason}```**Warn ID :** {warnid}""",color=yellow))
            await user.send(embed=discord.Embed(title="You've got warned", description=f"""Hello {usrname} this may be the first time you receive a mesage from me, i just want to show you the content of your warn;
**User :** <@{usrid}>
**Moderator :** {ausr}
**Reason :**```{reason}```**Warn ID :** {warnid}
Note : `The WarnID is used to identify your warn and, in the futur delete it in the case of a abuse`

If you feel this warn was unjustified or the moderator abused, please follow those steps :
1- Go here <#1026635543557197854>
2- Do /reportabuse <your warn id> // Your warn id is {warnid}
3- Go in the channel that got created and explain your problem with proof
""", color=yellow))
            # verify if user is already registered in punisher
            mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
            bdd = mydb.cursor()
            userid = user.id
            sql = f"SELECT * FROM punisher WHERE usrid = '{userid}'"
            bdd.execute(sql)
            result = bdd.fetchall()
            row = bdd.rowcount
            if row == 1:
                for data in result:
                    activepunisher = data[1]
                sql = f"UPDATE punisher SET data = '{activepunisher}**[Warn]** By <@{aid}> **Reason :** {reason} <t:{ctt}:R>[See more infos](https://avgeekcommunity.ml/m/i/wi?tbanid={warnid})\n' WHERE usrid = '{usrid}'"
                bdd.execute(sql)
                mydb.commit()
            else:
                sql = "INSERT INTO punisher(usrid, data) VALUES(%s, %s)"
                val = (usrid, f'**[Warn]** By <@{aid}> **Reason :** {reason} <t:{ctt}:R>[See more infos](https://avgeekcommunity.ml/m/i/wi?tbanid={warnid})\n')
                bdd.execute(sql, val)
                mydb.commit()
    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permission", description="Only moderators can use this command", color=red))
@bot.command(description="Kick someone that didn't respected rules but, at a hight level") # Kick command
async def kick(ctx, user:discord.User, reason):
    modop = discord.utils.get(ctx.guild.roles, name="{⚔} Modérateur+")
    ar = ctx.author.roles
    if modop in ar:
        usrroles = user.roles
        modo = discord.utils.get(ctx.guild.roles, name="{🛡} Modérateur")
        if modo in usrroles or modop in usrroles:
            await ctx.respond(embed=discord.Embed(title="Error", description="You can't use this command on a moderator", color=red))
        else:
            mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
            bdd = mydb.cursor()
            date_time = datetime.datetime.now()
            ctt = int(time.mktime(date_time.timetuple()))
            ranint = randint(1000000000,9999999999)
            ranstr = ''.join(random.choice(string.ascii_letters) for i in range(6))
            ranstr = ranstr.upper()
            usrid = user.id
            date = ctt
            modid = ctx.author.id
            kickid = f"AGKD{ranstr}{ranint}{ctt}"
            reason = str(reason)
            expiration = ctt + 900
            sql = "INSERT INTO avkick(usrid, date, modid, kickid, reason, expiration) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (f'{usrid}', date, f'{modid}', f'{kickid}', f'{reason}', expiration)
            bdd.execute(sql, val)
            mydb.commit()
            channel = bot.get_channel(1026954875625537648)
            await channel.send(embed=discord.Embed(title="User Kicked", description=f"""**User ID :** {usrid}
**User :** {user}
**Date :** {date_time}
**Moderator :** <@{modid}>

**Reason :** ```{reason}```
The user will be able to join <t:{expiration}:R>
""", color=orange))
            await ctx.respond(embed=discord.Embed(title="User Kicked", description=f"""**User :** {user}
**Reason :**```{reason}```
""", color=orange))
            await user.send(embed=discord.Embed(title="Kicked", description=f"""Hello {user},
You received this message because you got kicked by a moderator. We want to bring our channel calm and chill and, that why, you arent allowed to join back 15 minutes since you got kicked.

Informations related to your kick :
**==============User Kicked==============**

**User ID :** {usrid}
**User :** {user}
**Date :** {date_time}
**Moderator :** {ctx.author.name}
**Kick ID :**```{kickid}```*Note : The kick id is used to identify data of this kick if in some case you decide to report an abuse*
**Reason :**```{reason}```
**You will be able to join back :** <t:{expiration}:R>

**=======================================**

To join back, [click here](https://discord.gg/WGVneaZyPw) or here https://discord.gg/WGVneaZyPw
After you joined, make sure to read <#1012877013629018204>

If you feel this warn was unjustified or the moderator abused, please follow those steps :
1- Go here <#1026635543557197854>
2- Do /reportabuse <your warn id> // Your kick id is {kickid}
3- Go in the channel that got created and explain your problem with proof
""", color=orange))

            # verify if user is already registered in punisher
            mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
            bdd = mydb.cursor()
            userid = user.id
            sql = f"SELECT * FROM punisher WHERE usrid = '{userid}'"
            bdd.execute(sql)
            result = bdd.fetchall()
            row = bdd.rowcount
            if row == 1:
                for data in result:
                    activepunisher = data[1]
                sql = f"UPDATE punisher SET data = '{activepunisher}**[Kick]** By <@{modid}> **Reason :** {reason} <t:{ctt}:R>[See more infos](https://avgeekcommunity.ml/m/i/ki?tbanid={kickid})\n' WHERE usrid = '{usrid}'"
                bdd.execute(sql)
                mydb.commit()
            else:
                sql = "INSERT INTO punisher(usrid, data) VALUES(%s, %s)"
                val = (usrid, f'**[Kick]** By <@{modid}> **Reason :** {reason} <t:{ctt}:R>[See more infos](https://avgeekcommunity.ml/m/i/ki?tbanid={kickid})\n')
                bdd.execute(sql, val)
                mydb.commit()
            await ctx.guild.kick(user)
    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permissions", description="Only <@&1026225756562538517> can use this command", color=red))
@bot.command(description="Temporary ban a user")
@option(
    "duration",
    int,
    description="Time (in day) the user will get banned"
)
async def tempban(ctx, user : discord.Member, duration, reason):
    modop = discord.utils.get(ctx.guild.roles, name="{⚔} Modérateur+")
    modo = discord.utils.get(ctx.guild.roles, name="{🛡} Modérateur")
    usrroles = user.roles
    authroles = ctx.author.roles
    date_time = datetime.datetime.now()
    ctt = int(time.mktime(date_time.timetuple()))
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    if modop in authroles:
        if modo in usrroles or modop in usrroles:
            await ctx.respond(embed=discord.Embed(title="Error", description="You can't use this command on a moderator", color=red))
        else:
            day = duration * 86400
            # Generate a banid key
            ranint = randint(1000000000,9999999999)
            # Database insert data
            usrid = user.id
            date = ctt
            modid = ctx.author.id
            tbanid = f"AVTB{ranint}{ctt}"
            reason = str(reason)
            expiration = ctt + day
            duration = str(duration)
            sql = "INSERT INTO avtbans(usrid, date, modid, tbanid, reason, expiration, duration) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            val = (usrid, date, modid, tbanid, reason, expiration, duration)
            bdd.execute(sql, val)
            mydb.commit()
            await ctx.respond(embed=discord.Embed(title="Temporary Ban", description=f"""**User :** <@{usrid}>
**Reason :**```{reason}```**Temporary Ban Id :** {tbanid}
**Duration :** {duration} day(s)
""", color=red))
            channel = bot.get_channel(1026954875625537648)
            await channel.send(embed=discord.Embed(title="Temporary Ban", description=f"""**User ID :** {usrid}
**User :** {user}
**Date :** <t:{ctt}>
**Moderator :** <@{modid}>

**Reason :**```{reason}```
**Ban Duration :** {duration} Day's
**Ban expiration :** <t:{expiration}> (<t:{expiration}:R>)
""", color=red))

            await user.send(embed=discord.Embed(title="You got Temporary Banned", description=f"""Hello <@{usrid}>,
You got temporary banned from our server. Here are informations about your ban.
**================Temp Ban Infos================**

**User ID :** {usrid}
**User :** <@{usrid}>
**Date :** <t:{ctt}>

**Moderator :** {ctx.author.name}
**Reason :**```{reason}```**Ban Duration :**```{duration} Day's```**Ban Expiration Date :** <t:{expiration}> (<t:{expiration}:R>)
**TempBan ID :** {tbanid}

**===========================================**

If you feel this ban was unjustified, or abused, you can still appeal by  [clicking here](https://discord.com) (This will redirect you to discord.com because the appeal system isnt completed)
When your temporary ban is finished, you can [click here](https://discord.gg/WGVneaZyPw) or here https://discord.gg/WGVneaZyPw to join back the server. Make sure to read <#1012877013629018204>
""", color=red))

            # verify if user is already registered in punisher
            mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
            bdd = mydb.cursor()
            sql = f"SELECT * FROM punisher WHERE usrid = '{usrid}'"
            bdd.execute(sql)
            result = bdd.fetchall()
            row = bdd.rowcount
            if row == 1:
                for data in result:
                    activepunisher = data[1]
                sql = f"UPDATE punisher SET data = '{activepunisher}**[TempBan]** By <@{modid}> **Reason :** {reason} <t:{ctt}:R>[See more infos](https://avgeekcommunity.ml/m/i/tb?tbanid={tbanid})\n' WHERE usrid = '{usrid}'"
                bdd.execute(sql)
                mydb.commit()
            else:
                sql = "INSERT INTO punisher(usrid, data) VALUES(%s, %s)"
                val = (usrid, f'**[TempBan]** By <@{modid}> **Reason :** {reason} <t:{ctt}:R> [See more infos](https://avgeekcommunity.ml/m/i/tb?tbanid={tbanid})\n')
                bdd.execute(sql, val)
                mydb.commit()
            await ctx.guild.kick(user)
    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permissions", description="Only <@&1026225756562538517> can use this command", color=red))

@bot.command(description="See warns, kicks and temporary bans of a user")
async def punisher(ctx, user : discord.Member):
    modo = discord.utils.get(ctx.guild.roles, name="{🛡} Modérateur")
    modop = discord.utils.get(ctx.guild.roles, name="{⚔} Modérateur+")
    aid = ctx.author.id
    ausr = ctx.author.name
    ar = ctx.author.roles
    if modo in ar or modop in ar:
        mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
        bdd = mydb.cursor()
        aid = user.id
        usr = user.name
        sql = f"SELECT * FROM punisher WHERE usrid = '{aid}'"
        bdd.execute(sql)
        result = bdd.fetchall()
        row = bdd.rowcount
        if row ==1:
            for data in result:
                punisher = data[1]
            await ctx.respond(embed=discord.Embed(title=f"{usr}'s Punisher", description=f"{punisher}", color=red))
        else:
            await ctx.respond(embed=discord.Embed(title=f"{usr}'s Punisher", description="This user has no warn, no kick and no ban registered to him !", color=greensuccess))

    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permissions", description="Only <@&1026225756562538517> and <@&1001649319390228581> can use this command. If you want to see your punisher, do /mypunisher", color=red))
@bot.command(description="See all kick, warn and temp ban you received")
async def mypunisher(ctx):
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    aid = ctx.author.id
    sql = f"SELECT * FROM punisher WHERE usrid = {aid}"
    bdd.execute(sql)
    result = bdd.fetchall()
    row = bdd.rowcount
    if row == 1:
        for data in result:
            punishercontent = data[1]
        await ctx.respond(embed=discord.Embed(title="Your Punisher", description=f"{punishercontent}", color=red))
    else:
        await ctx.respond(embed=discord.Embed(title="Your Punisher", description="You have no warn, no kick and no bans in your punisher", color=greensuccess))

@bot.command() # report abuse
async def reportabuse(ctx, warnid):
    await ctx.respond(embed=discord.Embed(title="Processing...", description="We are processing your request, please wait.", color=lightblue))
    aid = ctx.author.id
    aname = ctx.author.name
    warnid = str(warnid)
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    sql = f"SELECT * FROM avwarns WHERE `usrid` = '{aid}' AND `warnid` = '{warnid}'"
    await ctx.edit(embed=discord.Embed(title="Preparing the request...", description="We are preparing your request, please wait.", color=lightblue))
    bdd.execute(sql)
    results = bdd.fetchall()
    await ctx.edit(embed=discord.Embed(title="Getting results of the request...", description="We are getting result of your request, please wait.", color=lightblue))
    row = bdd.rowcount
    if row == 1:
        await ctx.edit(embed=discord.Embed(title="Data Processing...", description="We are processing the results of your query.", color=lightblue))
        for data in results:
            usrid = data[0]
            date = data[1]
            mod = data[2]
            reason = data[3]
            warnid = data[4]
            appealable = data[5]
        sql = f"UPDATE avwarns SET appealable = 0 WHERE usrid = '{aid}' AND warnid = '{warnid}'"
        bdd.execute(sql)
        mydb.commit()
        sql = "SELECT * FROM avrati WHERE 1=1"
        bdd.execute(sql)
        result = bdd.fetchall()
        for tinum in result:
            value = tinum[0]
            value = value+1
        if value <=9:
            tinumber = f"000{value}"
        elif value <=99:
            tinumber = f"00{value}"
        elif value <=999:
            tinumber = f"0{value}"
        else:
            tinumber = value
        categ = discord.utils.get(ctx.guild.categories, id=1026979138428477451)
        for ch in categ.channels:
            if ch.topic==str(ctx.author.id):
                return await ctx.edit(embed=discord.Embed(title="Error", description="Its looking like you already have a ticket open.", color=red))
        overwrite={
            ctx.guild.default_role:discord.PermissionOverwrite(read_messages=False),
            ctx.me:discord.PermissionOverwrite(read_messages=True),
            ctx.author:discord.PermissionOverwrite(read_messages=True),
        }
        new_channel = await categ.create_text_channel(name=f"{aname}-{tinumber}",overwrites=overwrite,topic=f"{ctx.author.id}")
        sql = f"UPDATE avrati SET ticketid = {value} WHERE 1=1"
        bdd.execute(sql)
        mydb.commit()
        time.sleep(1)
        texpi = datetime.datetime.fromtimestamp(date)
        datet = texpi.strftime("%m/%d/%Y, %H:%M:%S") # %B %-d, %Y %-I:%-M %p
        await new_channel.send(f"<@{aid}>", embed=discord.Embed(title="Report Abuse", description=f"""Describe in details **with proof (pictures, video)** that you got abused by the moderator for this warn. Also, explain what you want for us, what \"actions\" you would like us to take.

**================Warn Datas================**

**User ID :** {aid}
**Username :** {aname}
**Date :** <t:{date}> <t:{date}:R>
**Moderator :** <@{mod}>
**Warn ID :** {warnid}
**Reason :**```{reason}```
**===================Rule===================**

**You need the respect those rules or, your ticket may get ignored or closed**```1- Do not ping staff
2- Do not insult, stay respectfull
3- The person who will take care of your ticket will remain neutral, even if it is he who warned you
4- Dont spam
5- Explain in details and with proof what happened
6- You understand that your ticket may get ignored/closed if you dont respect those```
**==========================================**""", color=rederror))
        await ctx.edit(embed=discord.Embed(title="Report Abuse Channel Created", description="Your Report channel got successfully created !", color=greensuccess))

    else: # change this else to check if its a ban id or a kick id
        await ctx.edit(embed=discord.Embed(title="404 not found", description=f"Woops, found nobody with your id and with this key in our system...verify if the key is good or contact support by doing `/support`", color=red))

#####################COMMANDS#####################

@bot.command(description="this command is for test, everyone can use it to see the content of this command")
async def test(ctx):
    membercount = ctx.guild.member_count
    print(membercount)
    msg = await ctx.send("Hi \nThis is a test")
    await msg.add_reaction("🇦")
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    bdd.execute("SELECT * FROM avwarns WHERE 1")
    result = bdd.fetchall()
    for x in result:
        usrid = x[0]
        print(usrid)

@bot.command(description="Send Rules Mesage")
async def rules(ctx):
    ar = ctx.author.roles
    role = discord.utils.get(ctx.guild.roles, name="*")
    if role in ar:
        button = Button(label="Accept Rules", style=discord.ButtonStyle.success, emoji="<a:tick:1010913651231825930>")
        
        async def button_callback(interaction):
            role = discord.utils.get(ctx.guild.roles, name="✔ Verified")
            ar = interaction.user.roles
            if role in ar:
                await interaction.response.send_message(embed=discord.Embed(title="Already Verified", description="Your account is already verified", color=rederror), ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(embed=discord.Embed(title="Verification Success", description="You successfully verified your account and can now access to the whole server", color=greensuccess), ephemeral=True)
        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)
        em1 = discord.Embed(color=white)
        em1.title="General Informations"
        em1.description ="Our server is a community, that said, respect is required and for all, moderators towards members and members towards moderators. The moderators reserve the right to act accordingly in the event of non-compliance with the rules.These rules may be subject to change. For any change, you will be notified."
        await ctx.send(embed=em1)
        em = discord.Embed(color=orange)
        em.title = "Discord Rules"
        em.description = "These rules are meant to be seen as a very brief and surface-level guidelines in how our moderation decisions take place. We may deem any person of not being able to access this server at any time, or set restriction in which you cannot utilize it for a certain time."
        em.add_field(name="Harassment and/or Threats", value="Direct harassment to an user is tiring to deal with - and we don't accept it in our public channels. Keep it out of our server otherwise face consequences of only using this server to view it, and not speak in it.", inline=False)
        em.add_field(name="Sexual / Violent Content", value="No content that can be seen as sexual or NSFW will be removed instantly for the safety of our server. Users involved indirectly and directly will face punishment. Content that can be seen as potentially disgusting in nature or terrorizing will be removed instantly for the safety of our server. Users involved indirectly and directly will face punishment.", inline=True)
        em.add_field(name="Illegal Activities", value="Due to the safety concerns of our server and to maintain a healthy relation with Discord standards, we prohibit the act of discussing and glorifying illegal activities. [ i.e. Speaking of real-currency gambling ]", inline=True)
        em.add_field(name="Discussing Peripheral Topics", value="We prohibit the act of discussing, glorifying and/or talking highly of any topic that may carry pettiness and may inflict drama in chatrooms.", inline=True)
        em.add_field(name="Spamming and flooding", value="Spamming or sending repeated messages for the purpose of invading a channel is strictly prohibited. Spam is considered as the sending of several messages being the same one after the other with the aim of invading a channel of this message. Flooding is also forbidden. Flood is identified as sending a message with a lot of same character following the previous one ex : ffffffffffffff", inline=True)
        em.add_field(name="Respect", value="Respect from members towards moderators and from moderators towards members is VERY important. The same goes for moderators towards you. They respect you, respect them", inline=True)
        em.add_field(name="Self Advertising", value="Highlighting your server, your website, or anything else that is in the advertising category is prohibited. Failure to respect this rule will result in a warn, followed by a mute if repeated", inline=True)
        em.add_field(name="Toxicity", value="Toxic, hateful behavior on any character of a person, physical or psychological, is prohibited. Body shaming, adding a \"fuck you\" type reaction or wanting to demonstrate hateful or negative behavior is prohibited.", inline=True)
        em.add_field(name="Arguing / Moderation", value="If a moderation action is made and you are not concerned, we ask you not to argue the content of the sanction made. Same thing if you are the person who is notified / kick / tempban, if you feel that there has been an abuse, the command / reportabuse is at your disposal. The general, commands, plane-spotting or any other textual channels are not places to argue a moderation action", inline=True)
        em.add_field(name="Moderation", value="Moderators have the right to determine whether an action, respects the rules or not, or is likely to cause trouble despite the rule not being written. In what, the moderation is free to act accordingly even if the action carried out is not in the rules.", inline=True)
        em.add_field(name="Official Discord Guidelines", value="Our server recommends each and every user utilizing our chatrooms to follow Discord's guidelines, while this rule list may include/exclude some of its rules, the entirety of our rules apparatus surrounds itself of Discord's guidelines. View them [here](https://discord.com/guidelines)", inline=False)
        em.set_footer(text="Now to comfirm you accept rules, click on the button below")
        await ctx.respond("wip", delete_after=1)
        await ctx.send(embed=em, view=view)

# Request access to the tiktok account
# @bot.command(description="A small form for you to request access to the Avgeek Community's tiktok account")
# async def reqttaccess(ctx):
#    aid = ctx.author.id
#    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
#    bdd = mydb.cursor()

@bot.command(description="Make an annoucement")
@option(
    "title",
    str,
    description="The title in the top of your annoucement"
)
@option(
    "content",
    str,
    description="The content of your annoucement"
)
async def makeann(ctx, title, content):
    sr = discord.utils.get(ctx.guild.roles, name="*")
    aid = ctx.author.id
    air = ctx.author.roles
    if sr in air:
        title=str(title)
        content=str(content)
        membercount = ctx.guild.member_count
        em = discord.Embed(color=orange)
        date_time = datetime.datetime.now()
        ctt = int(time.mktime(date_time.timetuple()))
        timeleft = ctt+30
        em.title="Hold up ! 🛑"
        em.description=f"""You are about to mention {membercount} in this server. Are you sure you want to ping them?
        
You have <t:{timeleft}:R> to make a choice"""
        yes = Button(label="Yes", style=discord.ButtonStyle.success, emoji="<a:tick:1010913651231825930>")
        no = Button(label="No", style=discord.ButtonStyle.danger, emoji="<a:tickred:637641999507390467>")
        async def yes_callback(btn):
            btnaid = btn.user.id
            if aid == btnaid:
                channel = channel = bot.get_channel(1026619181522755634)
                await ctx.respond(ephemeral=True,embed=discord.Embed(title="Success", description="Succesfully sent the annoucement in <#1026619181522755634>", color=greensuccess))
                em = discord.Embed(color=yellow)
                em.title=title
                em.description=content
                allowed_mentions = discord.AllowedMentions(everyone = True)
                await channel.send(content = "@everyone", allowed_mentions = allowed_mentions, embed=em)
        yes.callback = yes_callback
        async def no_callback(btn):
            btnaid = btn.user.id
            if aid == btnaid:
                await ctx.respond(ephemeral=True,embed=discord.Embed(title="Canceled", description="Successfully canceled the annoucement message", color=greensuccess))
        no.callback = no_callback
        view = View(timeout=None)
        view.add_item(yes)
        view.add_item(no)
        await ctx.respond(embed=em, view=view, delete_after=30, ephemeral=True)
        

    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permission", description="Only hight rank member can use this command", color=red), ephemeral=True)


#####################################################################
@bot.command(description="Make the Question of the day || WORKING IN PROGRESS")
@option(
    "question",
    str,
    description="The question"
)
@option(
    "a",
    str,
    description="The option a"
)
@option(
    "b",
    str,
    description="The option b"
)
@option(
    "c",
    str,
    description="The option c"
)
@option(
    "d",
    str,
    description="The option d"
)
@option(
    "goodanswer",
    str,
    description="The good answer | a, b, b, d one of those 4"
)
async def questionoftheday(ctx, question, a, b, c, d, goodanswer):
    rer = get(ctx.guild.roles, name="{❓❔} Question of the day")
    ar = ctx.author.roles
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    date_time = datetime.datetime.now()
    ctt = int(time.mktime(date_time.timetuple()))
    if rer in ar:
        sql = f"SELECT * FROM qodd WHERE end > {ctt}"
        bdd.execute(sql)
        result = bdd.fetchall()
        row = bdd.rowcount
        if row == 0:
            qid=ctt
            question=str(question)
            a=str(a)
            b=str(b)
            c=str(c)
            d=str(d)
            ga=str(goodanswer)
            end = ctt+86400
            if ga == "a" or ga == "b" or ga == "c" or ga == "d":
                bdd.execute(f"INSERT INTO qodd(qid, question, a, b, c, d, ga, end) VALUES({qid},'{question}','{a}','{b}','{c}','{d}','{ga}',{end})")
                mydb.commit()
                bdd.execute(f"INSERT INTO qoddr(qid, end)VALUES({qid},{end})")
                mydb.commit()
                channel = bot.get_channel(1031368582036201472)
                em = discord.Embed(color=white)

                ######### BUTTONS #########

                A = Button(style=discord.ButtonStyle.primary, emoji="🇦")
                async def a_callback(btn):
                    aid = btn.user.id
                    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
                    bdd = mydb.cursor()
                    bdd.execute(f"SELECT * FROM qoddr WHERE qid = {qid} AND end > {ctt}")
                    result = bdd.fetchall()
                    row = bdd.rowcount
                    if row == 1:
                        for dat in result:
                            anb = dat[1]
                            bnb = dat[2]
                            cnb = dat[3]
                            dnb = dat[4]
                            end = dat[5]
                        aid = btn.user.id
                        bdd.execute(f"SELECT * FROM qoddp WHERE qid = {qid} AND usrid = {aid}")
                        result = bdd.fetchall()
                        row = bdd.rowcount
                        if row == 0:
                            bdd.execute(f"INSERT INTO qoddp(usrid, qid, choice) VALUES({aid},{qid},'a')")
                            mydb.commit()
                            anb = anb+1
                            bdd.execute(f"UPDATE qoddr SET a = {anb} WHERE qid = {qid}")
                            mydb.commit()
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Success !", description="You Successfully made your choice. Result will be gived at the end of the question. If you selected the good one, you will receive 250$ in your bank account(/bank)", color=greensuccess))
                        else:
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Choice already made", description="You already made your choice and cant change it.", color=rederror))
                    else:
                        await btn.response.send_message(ephemeral=True,embed=fem(title="Woops...a bit late?", description="This question of the day is expired, you cant answer it anymore, wait for another question of the day ! :D", color=yellow))
                A.callback = a_callback
                
                B = Button(style=discord.ButtonStyle.primary, emoji="🇧")
                async def b_callback(btn):
                    aid = btn.user.id
                    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
                    bdd = mydb.cursor()
                    bdd.execute(f"SELECT * FROM qoddr WHERE qid = {qid} AND end > {ctt}")
                    result = bdd.fetchall()
                    row = bdd.rowcount
                    if row == 1:
                        for dat in result:
                            anb = dat[1]
                            bnb = dat[2]
                            cnb = dat[3]
                            dnb = dat[4]
                            end = dat[5]
                        aid = btn.user.id
                        bdd.execute(f"SELECT * FROM qoddp WHERE qid = {qid} AND usrid = {aid}")
                        result = bdd.fetchall()
                        row = bdd.rowcount
                        if row == 0:
                            bdd.execute(f"INSERT INTO qoddp(usrid, qid, choice) VALUES({aid},{qid},'b')")
                            mydb.commit()
                            bnb = bnb+1
                            bdd.execute(f"UPDATE qoddr SET b = {bnb} WHERE qid = {qid}")
                            mydb.commit()
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Success !", description="You Successfully made your choice. Result will be gived at the end of the question. If you selected the good one, you will receive 250$ in your bank account(/bank)", color=greensuccess))
                        else:
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Choice already made", description="You already made your choice and cant change it.", color=rederror))
                    else:
                        await btn.response.send_message(ephemeral=True,embed=fem(title="Woops...a bit late?", description="This question of the day is expired, you cant answer it anymore, wait for another question of the day ! :D", color=yellow))
                B.callback = b_callback
                
                C = Button(style=discord.ButtonStyle.primary, emoji="🇨")
                async def c_callback(btn):
                    aid = btn.user.id
                    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
                    bdd = mydb.cursor()
                    bdd.execute(f"SELECT * FROM qoddr WHERE qid = {qid} AND end > {ctt}")
                    result = bdd.fetchall()
                    row = bdd.rowcount
                    if row == 1:
                        for dat in result:
                            anb = dat[1]
                            bnb = dat[2]
                            cnb = dat[3]
                            dnb = dat[4]
                            end = dat[5]
                        aid = btn.user.id
                        bdd.execute(f"SELECT * FROM qoddp WHERE qid = {qid} AND usrid = {aid}")
                        result = bdd.fetchall()
                        row = bdd.rowcount
                        if row == 0:
                            bdd.execute(f"INSERT INTO qoddp(usrid, qid, choice) VALUES({aid},{qid},'c')")
                            mydb.commit()
                            cnb = cnb+1
                            bdd.execute(f"UPDATE qoddr SET c = {cnb} WHERE qid = {qid}")
                            mydb.commit()
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Success !", description="You Successfully made your choice. Result will be gived at the end of the question. If you selected the good one, you will receive 250$ in your bank account(/bank)", color=greensuccess))
                        else:
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Choice already made", description="You already made your choice and cant change it.", color=rederror))
                    else:
                        await btn.response.send_message(ephemeral=True,embed=fem(title="Woops...a bit late?", description="This question of the day is expired, you cant answer it anymore, wait for another question of the day ! :D", color=yellow))
                C.callback = c_callback
                
                D = Button(style=discord.ButtonStyle.primary, emoji="🇩")
                async def d_callback(btn):
                    aid = btn.user.id
                    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
                    bdd = mydb.cursor()
                    bdd.execute(f"SELECT * FROM qoddr WHERE qid = {qid} AND end > {ctt}")
                    result = bdd.fetchall()
                    row = bdd.rowcount
                    if row == 1:
                        for dat in result:
                            anb = dat[1]
                            bnb = dat[2]
                            cnb = dat[3]
                            dnb = dat[4]
                            end = dat[5]
                        aid = btn.user.id
                        bdd.execute(f"SELECT * FROM qoddp WHERE qid = {qid} AND usrid = {aid}")
                        result = bdd.fetchall()
                        row = bdd.rowcount
                        if row == 0:
                            bdd.execute(f"INSERT INTO qoddp(usrid, qid, choice) VALUES({aid},{qid},'d')")
                            mydb.commit()
                            dnb = dnb+1
                            bdd.execute(f"UPDATE qoddr SET d = {dnb} WHERE qid = {qid}")
                            mydb.commit()
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Success !", description="You Successfully made your choice. Result will be gived at the end of the question. If you selected the good one, you will receive 250$ in your bank account(/bank)", color=greensuccess))
                        else:
                            await btn.response.send_message(ephemeral=True,embed=fem(title="Choice already made", description="You already made your choice and cant change it.", color=rederror))
                    else:
                        await btn.response.send_message(ephemeral=True,embed=fem(title="Woops...a bit late?", description="This question of the day is expired, you cant answer it anymore, wait for another question of the day ! :D", color=yellow))
                D.callback = d_callback

                ###########################

                view = View(timeout=None)
                view.add_item(A)
                view.add_item(B)
                view.add_item(C)
                view.add_item(D)
                em.title="❔Question of the Day❓"
                em.description=question
                em.add_field(name="A)", value=a, inline=True)
                em.add_field(name="B)", value=f"{b}\n", inline=True)
                em.add_field(name="Prize", value="+250$ in your bank account", inline=True)
                em.add_field(name="C)", value=c, inline=True)
                em.add_field(name="D)", value=d, inline=True)
                em.add_field(name="End", value=f"<t:{end}:R>")
                em.add_field(name="Infos", value=f"""If you take the good answer, you will receive 250$ in your bank account (/bank) \n The good answer will be revealed <t:{end}:R>""", inline=False)

                await channel.send("<@&1002578714309165066>",embed=em, view=view, delete_after=86400)
                await ctx.respond(embed=fem(title="Question Sent", description="Question successfully sent, end in 12 hours. Auto delete in 15 seconds", color=greensuccess), delete_after=15)
            else:
                await ctx.respond(embed=discord.Embed(title="500 wrong request", description=f"Couldnt found `{ga}` isnt a valid good answer. Only `a`,`b`,`c`,`d` are valid content for \"goodanswer\"", color=rederror))
        else:
            await ctx.respond(embed=discord.Embed(title="Error", description="There is already an active question. Please wait for this question to end before starting another question of the day", color=rederror))
    else:
        await ctx.respond(embed=discord.Embed(title="Insufficient Permissions", description="Only special ranked member can use this command", color=red))
#########################ECONOMY#########################

@bot.command(description="See informations of your account")
async def bank(ctx):
    aid = ctx.author.id
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    bdd.execute(f"SELECT * FROM avbank WHERE usrid = {aid}")
    result = bdd.fetchall()
    row = bdd.rowcount
    if row == 0:
        accid = randint(1000000000,999999999999)
        sql = "INSERT INTO avbank(usrid, money, accid) VALUES(%s,%s,%s)"
        val = (aid, 50, accid)
        bdd.execute(sql, val)
        mydb.commit()
        await ctx.respond(embed=fem(title="Account Created", description="You didnt had an account, i created one for you, you just need to do the command /bank to see informations about your account", color=greensuccess))
    else:
        for x in result:
            accid = x[4]
            money = x[2]
            pending = x[3]
        em = fem(color=white)
        em.title="AvBank YOUR bank forever"
        em.description=f"Hello <@{aid}> here are all infos about your bank account"
        em.add_field(name="Account ID", value=f"#{accid}", inline=True)
        em.add_field(name="Money", value=f"{money}$", inline=True)
        em.add_field(name="Pending Money", value=f"{pending}$")
        await ctx.respond(embed=em)

@bot.command(description="Change, add, remove and reset money from someone")
@option(
    "action",
    int,
    description="1- change value, 2- add monney, 3 - remove money, 4 - reset"
)
@option(
    "value",
    int,
    description="The amount to set/add/remove for reset set to 0"
)
async def economy(ctx, user : discord.Member,action, value):
    await ctx.respond(embed=fem(title="Processing...", description="Processing your request", color=lightblue))
    rer = get(ctx.guild.roles, name="*")
    ar = ctx.author.roles
    mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
    bdd = mydb.cursor()
    if rer in ar:
        usrid = user.id
        action = int(action)
        value = int(value)
        if action == 1 or action == 2 or action == 3 or action == 4:
            if action == 1:
                bdd.execute(f"SELECT * FROM avbank WHERE usrid = {usrid}")
                result = bdd.fetchall()
                row = bdd.rowcount
                if row == 1:
                    for x in result:
                        money = x[2]
                    bdd.execute(f"UPDATE avbank SET money = {value} WHERE usrid = {usrid}")
                    mydb.commit()
                    value = str(value)
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully set the balance of <@{usrid}> to `{value}$`", color=greensuccess))
                else:
                    code = randint(100000000,99999999999)
                    sql = "INSERT INTO avbank(usrid, money, accid) VALUES(%s, %s, %s)"
                    val = (usrid, value, code)
                    bdd.execute(sql, val)
                    value = str(value)
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully set the balance of <@{usrid}> to `{value}$`", color=greensuccess))
            if action == 2:
                bdd.execute(f"SELECT * FROM avbank WHERE usrid = {usrid}")
                result = bdd.fetchall()
                row = bdd.rowcount
                if row == 1:
                    for x in result:
                        money = x[2]
                    nvalue = money+value
                    bdd.execute(f"UPDATE avbank SET money = {nvalue} WHERE usrid = {usrid}")
                    mydb.commit()
                    value = str(value)
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully added `{value}$` to <@{usrid}>'s bank account ", color=greensuccess))
                else:
                    code = randint(100000000,99999999999)
                    sql = "INSERT INTO avbank(usrid, money, accid) VALUES(%s, %s, %s)"
                    val = (usrid, value, code)
                    bdd.execute(sql, val)
                    value = str(value)
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully added `{value}$` to <@{usrid}>'s bank account ", color=greensuccess))
            if action == 3:
                bdd.execute(f"SELECT * FROM avbank WHERE usrid = {usrid}")
                result = bdd.fetchall()
                row = bdd.rowcount
                if row == 1:
                    for x in result:
                        money = x[2]
                    nvalue = money-value
                    bdd.execute(f"UPDATE avbank SET money = {nvalue} WHERE usrid = {usrid}")
                    mydb.commit()
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully removed `{value}$` from <@{usrid}>'s bank account ", color=greensuccess))
                else:
                    await ctx.edit(embed=fem(title="404 not found..", description="This user dosnt even have an account so you cant remove money from his non existant account...lol", color=rederror))
            if action == 4:
                bdd.execute(f"SELECT * FROM avbank WHERE usrid = {usrid}")
                result = bdd.fetchall()
                row = bdd.rowcount
                if row == 1:
                    bdd.execute(f"UPDATE avbank SET money = 0 WHERE usrid = {usrid}")
                    mydb.commit()
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully reset the balance of <@{usrid}> to `0$`", color=greensuccess))
                else:
                    code = randint(100000000,99999999999)
                    sql = "INSERT INTO avbank(usrid, money, accid) VALUES(%s, %s, %s)"
                    val = (usrid, 0, code)
                    bdd.execute(sql, val)
                    value = str(value)
                    await ctx.edit(embed=fem(title="Success", description=f"Successfully set the balance of <@{usrid}> to `0$`", color=greensuccess))
    else:
        await ctx.edit(embed=fem(title="Insufficient Permissions",description="Only hight ranked members are allowed to use this command", color=red))

#########################################################

@bot.command(description="Infos About the bot")
async def version(ctx):
    em = fem(color=lightblue)
    em.title="Bot Infos"
    em.add_field(name="Version", value="1.2.0", inline=True)
    em.add_field(name="Creator", value="willyrire#0001", inline=True)
    em.add_field(name="Creation date", value="I forgot lmao", inline=True)
    await ctx.respond(embed=em)
bot.run(token)
# date_time = datetime.datetime.now()
# ctt = int(time.mktime(date_time.timetuple()))
