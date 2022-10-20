import discord
import os
from datetime import datetime
import datetime
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
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

#####################UTIL VAR#####################

fem = discord.Embed # discord embed

##################################################

token = os.getenv('TOKEN2')
sqlpswd = os.getenv('SQLPSWD1')
sqlhost = os.getenv('SQLHOST1')
sqlusr = os.getenv('SQLUSER1')
sqldb = os.getenv('SQLDB1')

bot = discord.Bot(command_prefix=".", intents = discord.Intents.all(), debug_guilds=[1001644433831366716])

@bot.event 
async def on_ready():
    print("Bot is online")

@bot.command(description="Enable the bot")
async def enable(ctx):
    await ctx.respond("enabled")
    nbre = 0
    while True:
        channel = bot.get_channel(1031368582036201472)
        mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
        bdd = mydb.cursor()
        date_time = datetime.datetime.now()
        ctt = int(time.mktime(date_time.timetuple()))
        bdd.execute(f"SELECT * FROM qodd WHERE end < {ctt}")
        re = bdd.fetchall()
        row = bdd.rowcount
        if row == 1:
            for h in re:
                qid = h[0]
                ga = h[6]
                question = h[1]
                a = h[2]
                b = h[3]
                c = h[4]
                d = h[5]
            bdd.execute(f"SELECT * FROM qoddr WHERE qid = {qid}")
            result = bdd.fetchall()
            for i in result:
                ar = i[1]
                br = i[2]
                cr = i[3]
                dr = i[4]
                if ga == "a":
                    winners = ar
                elif ga == "b":
                    winners = br
                elif ga == "c":
                    winners = cr
                elif ga == "d":
                    winners = dr
                ttlvote = ar+br+cr+dr    
                em = discord.Embed(color=orange)
                em.title="❓Question of the Day❔"
                em.description=f"""**Question**
                {question}"""
                em.add_field(name="A)", value=a, inline=True)
                em.add_field(name="B)", value=b, inline=True)
                em.add_field(name="Prize", value="+250$ in your bank account", inline=True)
                em.add_field(name="C)", value=c, inline=True)
                em.add_field(name="D)", value=d, inline=True)
                em.add_field(name="Status", value="Expired", inline=True)
                em.add_field(name="Reveal", value=f"The good answer is 🥁🥁🥁🥁 **{ga}**", inline=False)
                em.add_field(name="Stats of this Question",value="Who vote for what, the amount of people who voted and the amount of winners", inline=False)
                em.add_field(name="Vote for A", value=ar, inline=True)
                em.add_field(name="Vote for B", value=br, inline=True)
                em.add_field(name="Total Vote", value=ttlvote, inline=True)
                em.add_field(name="Vote for C", value=cr, inline=True)
                em.add_field(name="Vote for D", value=dr, inline=True)
                em.add_field(name="Winners", value=winners, inline=True)
                await channel.send(embed=em)
                bdd.execute(f"SELECT * FROM qoddp WHERE choice = '{ga}'")
                result = bdd.fetchall()
                for data in result:
                    usrid = data[0]
                    bdd.execute(f"SELECT * FROM avbank WHERE usrid = {usrid}")
                    result = bdd.fetchall()
                    row = bdd.rowcount
                    if row == 1:
                        for x in result:
                            money = x[2]
                            nmoney = money+250
                            bdd.execute(f"UPDATE avbank SET money = {nmoney} WHERE usrid = {usrid}")
                            mydb.commit()
                    else:
                        bdd.execute(f"INSERT INTO avbank(usrid, pts, money,pending) VALUES({usrid},0,250,0)")
                        mydb.commit()
                time.sleep(30)
                mydb = mysql.connector.connect(host=sqlhost,user=sqlusr,password=sqlpswd,database=sqldb)
                bdd = mydb.cursor()
                bdd.execute("DELETE FROM qodd WHERE 1=1")
                mydb.commit()
                bdd.execute("DELETE FROM qoddr WHERE 1=1")
                mydb.commit()
                bdd.execute("DELETE FROM qoddp WHERE 1=1")
                mydb.commit()
        else:
            nbre += 1
            print(f"No expired question | #{nbre} ")

bot.run(token)
