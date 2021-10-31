from typing import Optional

import discord
from discord.ext import tasks
from replit import db

import json
import jsonpickle

import time


class ScheduledMessage:
  def __init__(self, my_message: discord.Message):
    message_list = my_message.content.split()
    my_time = message_list[1].split(':')
    hour = int(my_time[0])
    minute = int(my_time[1])

    my_content = ''
    for word in message_list[2:]:
      my_content += word + ' '
    my_content = my_content.strip()

    self.hour: int = hour
    self.minute: int = minute
    self.content: str = my_content
    self.channel_id: int = my_message.channel.id
    self.guild_id: int = my_message.author.guild.id

  # ScheduledMessage objects will be stored in the replit db as json strings. This function makes the jsonpickle conversion work.
  def to_json(self):
    return json.dumps(self, indent = 4, default = lambda o: o.__dict__)


async def try_create_scheduled_message(message: discord.Message) -> str:
  """Attempts to create a ScheduledMessage object 
  and add it to the replit db.
  """
  # The maximum number of messages we'll store is 20.
  if len(db.prefix("message")) > 20:
    await message.channel.send(
      "Sorry, the maximum number of messages has been reached.")

  else:
    try:
      add_scheduled_message_to_db(ScheduledMessage(message))
      return "Message logged."

    except IndexError:
      return "Please see the documentation for how to create scheduled messages: \nhttps://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit"


@tasks.loop(seconds = 60)
async def do_scheduled_messages(client: discord.Client) -> None:
  my_time = get_time()
  for key in db.prefix("message"):
    scheduled_message = get_scheduled_message_from_db(key)
    # Sends the scheduled message if it's the right time.
    if isinstance(scheduled_message, ScheduledMessage) and scheduled_message.hour == my_time[0] and scheduled_message.minute == my_time[1]:
      my_channel = get_channel(client, scheduled_message.channel_id)
      if my_channel is not None:
        await my_channel.send(scheduled_message.content)


def get_channel(client: discord.Client,
channel_id: int) -> Optional[discord.CategoryChannel]:
  """Returns a CategoryChannel object from a channel id. 
  Returns None if the channel is not found."""
  for channel in client.get_all_channels():
    if channel.id == channel_id:
      return channel
  return None


def get_time() -> tuple:
  """Returns the current hour and minute in PST."""
  my_time = time.gmtime()
  # We'll use Pacific Standard Time for time inputs.
  hour = (my_time.tm_hour + 17) % 24
  minute = my_time.tm_min

  return hour, minute


def add_scheduled_message_to_db(sm: ScheduledMessage) -> None:
  db["current_message_number"] += 1
  key = str(db["current_message_number"])
  key = "message" + key

  sm_encoded = jsonpickle.encode(sm, unpicklable = True)
  db[key] = sm_encoded


def get_scheduled_message_from_db(key: str) -> Optional[ScheduledMessage]:
  """Gets a json string at db[key], then returns the ScheduledMessage 
  object that it represents.
  """
  value = db[key]
  if isinstance(value, str):
    return jsonpickle.decode(db[key])
  return None


def clear_guild_scheduled_messages(message: discord.Message) -> bool:
  """Deletes all messages created in the guild. 
  Returns True if something was deleted, False otherwise.
  """
  for key in db.prefix("message"):
    if (get_scheduled_message_from_db(key).guild_id == 
    message.author.guild.id):
      del db[key]
      return True
  return False


def clear_all_scheduled_messages() -> None:
  """Removes scheduled messages in all guilds.
  Use with caution.
  """
  for message in db.prefix("message"):
    del db[message]
  db["current_message_number"] = 1
  