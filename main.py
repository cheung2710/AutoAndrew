# documentation: https://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit


import discord
import os

from api_requests import get_cat, get_inspirobot, get_quote, get_roast
from keep_alive import keep_alive
from scheduled_message import (try_create_scheduled_message, do_scheduled_messages, clear_guild_scheduled_messages)
from small_bot_functions import (bad_anal_joke, check_bad_words, coinflip,
get_help, say, say_hello, shout)


client = discord.Client()


COMMAND_PREFIX = 'a!'


@client.event
async def on_ready() -> None:
  """Contains the things the bot will do when it's launched."""
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status = discord.Status.online, 
  activity = discord.Game("a!help"))
  do_scheduled_messages.start(client)


@client.event
async def on_message(message: discord.Message) -> None:
  """Contains all of the bot's responses to message events."""
  # Ignores all bots' messages, including its own.
  if message.author.bot:
    return

  # Checks each message for bad words.
  await check_bad_words(message)

  # Check for command prefix.
  if message.content.startswith(COMMAND_PREFIX):
  
    if message.content.startswith(COMMAND_PREFIX + 'cat'):
      if check_image_permissions(message):
        await get_cat(message)

    elif message.content.startswith(COMMAND_PREFIX + 
    'clearscheduledmessages'):
      if check_message_permissions(message):
        if clear_guild_scheduled_messages(message):
          await message.channel.send("Messages deleted.")
        else: 
          await message.channel.send("No messages found.")

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
        my_message = await try_create_scheduled_message(message)
        my_channel = message.channel
        await my_channel.send(my_message)

    elif message.content.startswith(COMMAND_PREFIX + 'shout'):
      if check_message_permissions(message):
        if len(message.content) > 7:
          await shout(message, message.content[7:])


def check_message_permissions(message: discord.Message) -> bool:
  """Returns whether the bot has permission to send messages."""
  return message.author.guild_permissions.send_messages

def check_image_permissions(message: discord.Message) ->bool:
  """Returns whether the bot has permission to send images."""
  return message.author.guild_permissions.attach_files


keep_alive()
client.run(os.environ['DISCORD_BOT_KEY'])
