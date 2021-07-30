import discord
import logging
import requests

import hidden

DISCORD_TOKEN=hidden.DISCORD_TOKEN
TRN_TOKEN=hidden.TRN_TOKEN

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

logger=logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler(filename='discord.log',encoding='utf-8',mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)