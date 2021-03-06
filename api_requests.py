import discord
import requests
import json
import io
import aiohttp
from small_bot_functions import get_author


async def get_cat(message: discord.Message) -> None:
  """Sends an image from TheCatApi."""
  response = requests.get('https://api.thecatapi.com/v1/images/search')
  json_data = json.loads(response.text)
  my_url = json_data[0]['url']
  async with aiohttp.ClientSession() as session:
    async with session.get(my_url) as resp:
      if resp.status != 200:
          return await message.channel.send('Sorry, I couldn\'t download the file...')
      data = io.BytesIO(await resp.read())
      await message.channel.send(file = discord.File(data, 'cat_image.png'))


async def get_inspirobot(message: discord.Message) -> None:
  """Sends an image generated by Inspirobot.
  Refer to Discord API docs: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-upload-an-image"""
  try:
    num_images = int(message.content.split()[1])
    if num_images > 10:
      num_images = 10
  except (ValueError, IndexError): 
    num_images = 1

  while num_images > 0:
    my_url = requests.get('https://inspirobot.me/api?generate=true').text
    async with aiohttp.ClientSession() as session:
      async with session.get(my_url) as resp:
        if resp.status != 200:
            return await message.channel.send('Sorry, I couldn\'t download the file...')
        data = io.BytesIO(await resp.read())
        await message.channel.send(file = discord.File(data, 'inspirobot_image.png'))
    num_images -= 1
  

def get_quote() -> str:
  """Returns an inspirational quote from zenquotes.io."""
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  return json_data[0]['q'] + "\n--" + json_data[0]['a']


def get_roast(message: discord.Message) -> str:
  """Returns an insult with a name attached from insult.mattbas.org."""
  insult = requests.get('https://insult.mattbas.org/api/insult').text
  if len(message.content) <= 7:
    return insult + "."

  name = message.content[7:]
  # "a!roast me" will roast the author instead of "Me"
  if name.strip() == 'me':
    name = get_author(message)

  name = name.strip().split()
  # capitalizes all words if there's more than one word
  if len(name) > 1:
    for i in range(len(name)):
      name[i] = name[i].capitalize()
  return ' '.join(name) + ", you " + insult[4:] + "."
