import discord
import logging
import requests
import hidden
from discord.ext import commands
import localeregion
import pandas as pd

DISCORD_TOKEN=hidden.DISCORD_TOKEN
TRN_TOKEN=hidden.TRN_TOKEN
X_Riot_Token=hidden.X_Riot_Token
Locales=localeregion.Locales
'''
################################################################################################################################################
                                                                        CSGO
################################################################################################################################################



url='https://public-api.tracker.gg/v2/csgo/standard/profile/steam'
client = discord.Client()

logger=logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler=logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print(f'{client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$'):
        id=message.content[1:]
        request_url='/'.join((url,id))
        print(request_url)
        
        response=requests.get(request_url,headers={'TRN-Api-Key':TRN_TOKEN})
        data=response.json()
        try:
            stats=data['data']['segments'][0]['stats']
            embedVar = discord.Embed(title=f"__**{data['data']['platformInfo']['platformUserHandle']}**__", description="", color=0x00ff00)

            to_send="**timeplayed:**{}\n**kills:**{},  **deaths:**{}\n**kd:**{},  **headshots:**{}\n**mvp:**{},  **wins:**{}".format(stats['timePlayed']['displayValue'],stats['kills']['displayValue'],stats['deaths']['displayValue'],stats['kd']['displayValue'],stats['headshots']['displayValue'],stats['mvp']['displayValue'],stats['wins']['displayValue'])
            embedVar.add_field(name=f'**Stats:**',value=to_send)
            await message.channel.send(embed=embedVar)
        except:
            await message.channel.send("User Profile __**Private**__ or __**Doesn't Exist**__")

client.run(DISCORD_TOKEN)
#################################################################################################################################################
'''
bot=commands.Bot(command_prefix='$')
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to server')

@bot.command(name='status'.lower())
async def server_stats(ctx):
    url='https://ap.api.riotgames.com/val/status/v1/platform-data'
    response=requests.get(url,headers={'X-Riot-Token':X_Riot_Token})
    data=response.json()
    # print(data['maintenances'],data['incidents'])
    try:
        embedVar = discord.Embed(title=f"__**Valorant Server Status**__", description="", color=0x00ff61)
        if data['maintenances']==[] and data['incidents']==[]:
            embedVar.add_field(name="**Service**",value="All Valorant Services are __**`Available`**__")
            await ctx.send(embed=embedVar)
        else:
            print(data['maintenances'],data['incidents'])
            maintenances=[Locales[i] for i in data['maintenances']]
            incidents=[Locales[i] for i in data['incidents']]
            embedVar.add_field(name="**`Outage_Regions:`**",value=str(maintenances))
            embedVar.add_field(name="**`Critical_Regions:`**",value=str(incidents))
            await ctx.send(embed=embedVar)
    except:
        await ctx.send("Wrong Command Try '$help' for more details")


@bot.command(name='top'.lower())
async def leaderboard(ctx,region,count):
    url="https://"+region+".api.riotgames.com/val/ranked/v1/leaderboards/by-act/2a27e5d2-4d30-c9e2-b15a-93b8909a442c?size="+count+"&startIndex=0"
    response=requests.get(url,headers={'X-Riot-Token':X_Riot_Token})
    data=response.json()
    
    df=pd.DataFrame({"Name":[],"Ratings":[]})
    for player in data['players']:
        try:
            name="#".join((player["gameName"],player["tagLine"]))
        except:
            continue
        ratings=player["rankedRating"]        
        # embedVar.add_field(name="Pos:\t\t\t\t\t Name:\t\t\t\t\t\t Ratings:",value=f"{str(leaderboard).ljust(5)} {name.ljust(5)} {str(ratings).ljust(10)}\n",inline=False)
        df=df.append({"Name":name,"Ratings":ratings},ignore_index=True)
    
    embedVar=discord.Embed(title=f"__**Valorant Leaderboards({region})**__", description=df.to_markdown(), color=0xff0061)
    await ctx.send(embed=embedVar)

bot.command(name="helpme".lower())
async def help_command(ctx):
    await ctx.send("status----To get valorant server status\n top {ap,na,br,eu,kr,latam} {0-100} ---- Use this command to get leaderboard stats for top valorant players in these regions")


bot.run(DISCORD_TOKEN)



logger=logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler(filename='discord.log',encoding='utf-8',mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)