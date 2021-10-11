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
  # The maximum number of messages we'll store is 10.
  if len(db.prefix("message")) > 10:
    await message.channel.send(
      "Sorry, the maximum number of messages has been reached.")

  else:
    try:
      add_scheduled_message_to_db(ScheduledMessage(message))
      return "Message logged."

    except IndexError:
      return "Please type the command like this: \na!scheduledmessage [time in PST] [message] \nFor example: \na!scheduledmessage 23:30 Pee-pee before slee-pee!"


@tasks.loop(seconds = 60)
async def do_scheduled_messages(client: discord.Client) -> None:
  my_time = get_time()
  for key in db:
    scheduled_message = get_scheduled_message_from_db(key)
    # Sends the scheduled message if it's the right time.
    if isinstance(scheduled_message, ScheduledMessage) and scheduled_message.hour == my_time[0] and scheduled_message.minute == my_time[1]:
      my_channel = get_channel(client, scheduled_message.channel_id)
      if my_channel is not None:
        await my_channel.send(scheduled_message.content)


def get_channel(client: discord.Client, channel_id: int) -> Optional[discord.CategoryChannel]:
  for channel in client.get_all_channels():
    if channel.id == channel_id:
      return channel
  return None


def get_time() -> tuple:
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
  value = db[key]
  if isinstance(value, str):
    return jsonpickle.decode(db[key])
  return None


def clear_all_scheduled_messages() -> None:
  messages = db.prefix("message")
  for message in messages:
    del db[message]
  db["current_message_number"] = 1
  