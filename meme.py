# Python 3+
# Fill the lines 16, 43 & 44 with your own values
# Example : !meme ramp . studying . coding discord bots

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import json
import requests

bot = commands.Bot(command_prefix="!")
# Removing the default help command
bot.remove_command('help')

# The token of the discord bot (https://discordapp.com/developers/applications/)
TOKEN = 'your token here'

@bot.event
async def on_ready():
    print('Ready')

# The meme command
@bot.command(pass_context=True)
async def meme(ctx, *, arg):
    # Get some help by typing !meme help
    if arg == 'help':
        await bot.say("""```!meme [meme name] . [text 1] . [text 2]```You can see the full list of available memes here : https://api.imgflip.com/get_memes""")
    else:
        args = arg.split('.')

        meme = args[0].rstrip().lstrip()
        text0 = ' '
        text1 = ' '
        if len(args) > 1:
            text0 = args[1].rstrip().lstrip()
        if len(args) > 2:
            text1 = args[2].rstrip().lstrip()

        response = requests.get("https://api.imgflip.com/get_memes")
        data = json.loads(response.text)

        # You need to create an account on imgflip to use the API
        payload = { 'template_id': 'undefined',
                    'username': 'user', # imgflip username
                    'password': 'pass', # imgflip password
                    'text0': text0,
                    'text1': text1
                    }
        url = 'undefined'

        for d in data['data']['memes']:
            if meme.lower() in d['name'].lower(): 
                payload['template_id'] = d['id']
                break
            else:
                continue

        if payload['template_id'] is not 'undefined':
            response = requests.post('https://api.imgflip.com/caption_image', params=payload)
            data = json.loads(response.text)
            url = json.dumps(data['data']['url'])
            await bot.say(url.strip('"'))
        else:
            await bot.say('Meme not found')

bot.run(TOKEN)