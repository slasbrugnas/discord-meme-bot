# Python 3+
# Fill the lines 16, 44 & 45 with your own values
# Example : !meme ramp . studying . coding discord bots

import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import json
import requests

load_dotenv(find_dotenv())

# The token of the discord bot (https://discordapp.com/developers/applications/)
TOKEN = os.environ.get("TOKEN")
# ImgFlip Ids
USERNAME = os.environ.get("IMGFLIP_USERNAME")
PASSWORD = os.environ.get("IMGFLIP_PASSWORD")

bot = commands.Bot(command_prefix="!")
# Removing the default help command
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Ready')

# The meme command
@bot.command(pass_context=True)
async def meme(ctx, *, arg):
    # Get some help by typing !meme help
    if arg == 'help':
        await ctx.send("""```!meme [meme name] ; [text 1 (optional)] ; [text 2 (optional)] ; ... ; [text n (optional)]```You can see the full list of available memes here : https://imgflip.com/memetemplates""")
    else:
        args = arg.split(';')

        meme = args[0].rstrip().lstrip()
        boxes = []

        for text in args[1:]:
            boxes.append(text.rstrip().lstrip())

        response = requests.get("https://api.imgflip.com/get_memes")
        data = json.loads(response.text)

        payload = {
            'template_id': 'undefined',
            'username': USERNAME,
            'password': PASSWORD,
        }

        for idx, box in enumerate(boxes):
            payload['boxes[{}][text]'.format(idx)] = box

        for d in data['data']['memes']:
            if meme.lower() in d['name'].lower():
                payload['template_id'] = d['id']
                break
            else:
                continue

        url = 'undefined'
        if payload['template_id'] != 'undefined':
            response = requests.post('https://api.imgflip.com/caption_image', params=payload)
            data = json.loads(response.text)
            url = json.dumps(data['data']['url'])
            await ctx.send(url.strip('"'))
        else:
            await ctx.send('Meme not found')

bot.run(TOKEN)
