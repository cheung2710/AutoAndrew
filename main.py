# documentation: 
# https://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit


import discord
import os
# from replit import db

from api_requests import get_cat, get_inspirobot, get_quote, get_roast
from banned_words import add_banned_word, check_banned_words, dm_banned_words, remove_banned_word
from keep_alive import keep_alive
from scheduled_message import (try_create_scheduled_message, do_scheduled_messages, clear_guild_scheduled_messages)
from small_bot_functions import (bad_anal_joke, coinflip,
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
  await check_banned_words(message)

  # Check for command prefix.
  if message.content.startswith(COMMAND_PREFIX):

    if message.content.startswith(COMMAND_PREFIX + 'ban'):
      await add_banned_word(message)
  
    elif message.content.startswith(COMMAND_PREFIX + 'cat'):
      await get_cat(message)

    elif message.content.startswith(COMMAND_PREFIX + 
    'clearscheduledmessages'):
      if clear_guild_scheduled_messages(message):
        await message.channel.send("Messages deleted.")
      else: 
        await message.channel.send("No messages found.")

    elif message.content.startswith(COMMAND_PREFIX + 'coinflip'):
      await message.channel.send(coinflip())

    elif message.content.startswith(COMMAND_PREFIX + 'getbannedwords'):
      await dm_banned_words(client, message)

    elif message.content.startswith(COMMAND_PREFIX + 'hello'):
      await message.channel.send(say_hello(message))

    elif message.content.startswith(COMMAND_PREFIX + 'help'):
      await message.channel.send(get_help())

    elif message.content.startswith(COMMAND_PREFIX + 'inspire'):
      await get_inspirobot(message)

    elif message.content.startswith(COMMAND_PREFIX + 'null'):
      await bad_anal_joke(message)

    elif message.content.startswith(COMMAND_PREFIX + 'quote'):
      await message.channel.send(get_quote())

    elif message.content.startswith(COMMAND_PREFIX + 'roast'): 
      await message.channel.send(get_roast(message))

    elif message.content.startswith(COMMAND_PREFIX + 'say'):
      if len(message.content) > 5:
        await say(message, message.content[5:])

    elif message.content.startswith(COMMAND_PREFIX + 'scheduledmessage'):
      my_message = await try_create_scheduled_message(message)
      my_channel = message.channel
      await my_channel.send(my_message)

    elif message.content.startswith(COMMAND_PREFIX + 'shout'):
      if len(message.content) > 7:
        await shout(message, message.content[7:])

    elif message.content.startswith(COMMAND_PREFIX + 'unban'):
      await remove_banned_word(message)


keep_alive()
# print(db.keys())
client.run(os.environ['DISCORD_BOT_KEY'])
