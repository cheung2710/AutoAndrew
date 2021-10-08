# documentation: https://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit


import discord
import os
from replit import db

from api_requests import get_cat, get_inspirobot, get_quote, get_roast
from keep_alive import keep_alive
from scheduled_message import (try_create_scheduled_message, do_scheduled_messages, clear_all_scheduled_messages)
from small_bot_functions import (bad_anal_joke, check_bad_words, coinflip,
get_help, say, say_hello, shout)


client = discord.Client()


COMMAND_PREFIX = 'a!'


@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status = discord.Status.online, 
    activity = discord.Game("a!help"))
    do_scheduled_messages.start(client)


@client.event
async def on_message(message: discord.Message) -> None:
  """Contains all of the bot's responses to message events."""
  # ignore all other bots' messages
  if message.author.bot:
    return

  # check each message for bad words
  await check_bad_words(message)

  # check for command prefix
  if message.content.startswith(COMMAND_PREFIX):
  
    if message.content.startswith(COMMAND_PREFIX + 'cat'):
      if check_image_permissions(message):
        await get_cat(message)

    elif message.content.startswith(COMMAND_PREFIX + 'coinflip'):
      if check_message_permissions(message):
        await message.channel.send(coinflip())

    elif message.content.startswith(COMMAND_PREFIX + 'hello'):
      if check_message_permissions(message):
        await message.channel.send(say_hello(message))

    elif message.content.startswith(COMMAND_PREFIX + 'help'):
      if check_message_permissions(message):
        await message.channel.send(get_help())

    elif message.content.startswith(COMMAND_PREFIX + 'inspire'):
      if check_image_permissions(message):
        await get_inspirobot(message)

    elif message.content.startswith(COMMAND_PREFIX + 'null'):
      if check_message_permissions(message):
        await bad_anal_joke(message)

    elif message.content.startswith(COMMAND_PREFIX + 'quote'):
      if check_message_permissions(message):
        await message.channel.send(get_quote())

    elif message.content.startswith(COMMAND_PREFIX + 'roast'): 
      if check_message_permissions(message):
        await message.channel.send(get_roast(message))

    elif message.content.startswith(COMMAND_PREFIX + 'say'):
      if check_message_permissions(message):
        if len(message.content) > 5:
          await say(message, message.content[5:])

    elif message.content.startswith(COMMAND_PREFIX + 'scheduledmessage'):
      if check_message_permissions(message):
        await try_create_scheduled_message(message)

    elif message.content.startswith(COMMAND_PREFIX + 'shout'):
      if check_message_permissions(message):
        if len(message.content) > 7:
          await shout(message, message.content[7:])


def check_message_permissions(message: discord.Message) -> bool:
  return message.member.guild.me.hasPermission(['SEND_MESSAGES'])

def check_image_permissions(message: discord.Message) ->bool:
  return message.member.guild.me.hasPermission(['ATTACH_FILES'])


keep_alive()
# clear_all_scheduled_messages()
# print(db.keys())
client.run(os.environ['DISCORD_BOT_KEY'])
