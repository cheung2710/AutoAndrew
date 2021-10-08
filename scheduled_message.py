from discord.ext import tasks
from replit import db
import time


class ScheduledMessage:
  def __init__(self, message):
    message_list = message.content.split()
    my_time = message_list[1].split(':')
    hour = my_time[0]
    if int(hour) < 10:
      hour = '0' + hour
    minute = my_time[1]

    my_message = ''
    for word in message_list[2:]:
      my_message += word + ' '
    my_message = my_message.strip()

    self.hour = hour
    self.minute = minute
    self.content = my_message
    self.channel = message.channel
    self.guild_snowflake = message.author.guild.id


async def try_create_scheduled_message(message):
  # The maximum number of messages we'll store is 10.
  if len(db.prefix("message")) > 10:
    await message.channel.send(
      "Sorry, the maximum number of messages has been reached.")

  else:
    try:
      sm = ScheduledMessage(message)
      add_scheduled_message_to_db(sm)
      await message.channel.send("Message logged.")

    except IndexError:
      await message.channel.send("Please type the command like this: \na!scheduledmessage [time in UTC] [message] \nFor example: \na!scheduledmessage 23:30 Pee-pee before slee-pee!")


@tasks.loop(seconds = 60)
async def do_scheduled_messages(client):
  my_time = get_time()
  for key in db:

    try: 
      is_iterable = db[key][0]
      is_iterable = True
    except TypeError:
      is_iterable = False

    # checks if the hours and minutes match
    if is_iterable and db[key][0] == my_time[0] and db[key][1] == my_time[1]:
      my_channel = get_channel(client, db[key][3])
      if my_channel is not None:
        await my_channel.send(db[key][2])


def get_channel(client, channel_id):
  for channel in client.get_all_channels():
    if channel.id == channel_id:
      return channel
  return None


def get_time() -> str:
  my_time = time.gmtime()
  # using Pacific Standard Time for inputs
  hour = str((my_time.tm_hour + 17) % 24)
  if int(hour) < 10:
    hour = "0" + hour
  minute = str(my_time.tm_min)
  if int(minute) < 10:
    minute = "0" + minute

  return hour, minute


def add_scheduled_message_to_db(sm: ScheduledMessage):
  db["current_message_number"] += 1
  key = db["current_message_number"]
  key = "message" + str(key)
  db[key] = (sm.hour, sm.minute, sm.content, int(sm.channel.id), sm.guild_snowflake)


def clear_all_scheduled_messages():
  messages = db.prefix("message")
  for message in messages:
    del db[message]
  db["current_message_number"] = 1