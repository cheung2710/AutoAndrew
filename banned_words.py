import discord
from replit import db
from small_bot_functions import get_author


banned_word_message = ", watch your fucking language!"


async def check_banned_words(message: discord.Message) -> None:
  """Sends a message if anyone says a word in the bad_words[] list."""
  try: 
    banned_words = db["bannedwords_" + str(message.author.guild.id)]

  except KeyError:
    return

  for word in banned_words:
      if word in message.content.lower():
        await message.channel.send(get_author(message) + banned_word_message)
        return


async def dm_banned_words(client: discord.Client, message: discord.Message) -> None:
  """Sends a DM to the message's author 
  with a list of the banned words in the guild.
  """ 
  try:
    words_list = db["bannedwords_" + str(message.author.guild.id)]

  except KeyError:
    await message.channel.send("There are no banned words in this server.")
    return
  
  banned_words = "Banned words: \n"
  for word in words_list:
    banned_words += word + "\n"
  await message.author.send(banned_words)
  await message.channel.send("Check your DMs for the naughty words, " + get_author(message) + " ;)")


async def add_banned_word(message: discord.Message) -> None:
  new_banned_word = message.content[5:].strip()
  if len(new_banned_word) < 1:
    await message.channel.send("Sorry, that can't be banned.")
    return

  key = "bannedwords_" + str(message.author.guild.id)
  try:
    db[key]

  except KeyError:
    db[key] = []

  if len(db[key]) >= 30:
    await message.channel.send("Sorry, you can't ban any more words. \nUse *a!getbannedwords* to see all the banned words, or remove banned words with *a!unban*.")
    return
  
  if new_banned_word in db[key]:
    await message.channel.send(new_banned_word + " is already banned.")
    return
    
  db[key].append(new_banned_word)
  db[key].value.sort()
  await message.channel.send(new_banned_word + " is now banned.")


async def remove_banned_word(message: discord.Message) -> None:
  my_word = message.content[7:].strip()
  if len(my_word) < 1:
    await message.channel.send("That word isn't on the banlist.")
    return

  key = "bannedwords_" + str(message.author.guild.id)
  try:
    banned_words = db[key]
    banned_words.remove(my_word)
    await message.channel.send(my_word + " is now unbanned.")

  except (KeyError, ValueError):
    await message.channel.send("That word isn't on the banlist.")
