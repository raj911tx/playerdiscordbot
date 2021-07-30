import discord
import logging
import requests
#hidden.py contains the TOKENS as DISCORD_TOKEN and TRN_TOKEN.Create a file and put the tokens of that value
import hidden

DISCORD_TOKEN=hidden.DISCORD_TOKEN
TRN_TOKEN=hidden.TRN_TOKEN

#Use tracker.gg api endpoint to fetch the player data
url='https://public-api.tracker.gg/v2/csgo/standard/profile/steam'
client = discord.Client()

#Use logging to put the log data in a file for DEBUGGING
logger=logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler=logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#create a decorator of client function
@client.event
async def on_ready():
    print(f'{client.user}')

@client.event
async def on_message(message):
    #If the message author is same as bot it will not do anything
    if message.author == client.user:
        return
    
    #to define it as command when something starts with $ it will take the rest as command parameters
    if message.content.startswith('$'):
        id=message.content[1:]
        #the url request consists of enpoint address and player id
        request_url='/'.join((url,id))
        print(request_url)
        
        response=requests.get(request_url,headers={'TRN-Api-Key':TRN_TOKEN})
        #get the response from HTTP GET request as json format
        data=response.json()
        
        try:
            stats=data['data']['segments'][0]['stats']
            #use embedding to show the output in nice table format
            embedVar = discord.Embed(title=f"__**{data['data']['platformInfo']['platformUserHandle']}**__", description="", color=0x00ff00)

            to_send="**timeplayed:**{}\n**kills:**{},  **deaths:**{}\n**kd:**{},  **headshots:**{}\n**mvp:**{},  **wins:**{}".format(stats['timePlayed']['displayValue'],stats['kills']['displayValue'],stats['deaths']['displayValue'],stats['kd']['displayValue'],stats['headshots']['displayValue'],stats['mvp']['displayValue'],stats['wins']['displayValue'])
            embedVar.add_field(name=f'**Stats:**',value=to_send)
            #send the data to the discord channel
            await message.channel.send(embed=embedVar)
        except:
            #if the steam id is private it will show the following message
            await message.channel.send("User Profile __**Private**__ or __**Doesn't Exist**__")

client.run(DISCORD_TOKEN)
