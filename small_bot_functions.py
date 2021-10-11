import random
import discord

bad_words = ['fuck', 'shit', 'bitch']
greetings = ['hello', 'hi', 'greetings', 'hey', 'yo']


def bad_anal_joke(message: discord.Message) -> str:
  name = get_author(message)
  return message.channel.send("I'm flattered, " + name + ", but I'll have to decline.")


async def check_bad_words(message: discord.Message) -> None:
  """Sends a message if anyone says a word in the bad_words[] list."""
  for word in bad_words:
      if word in message.content:
        my_author = get_author(message)
        await message.channel.send(my_author + ", watch your fucking language!")


def coinflip() -> str:
  if random.choice([0, 1]) == 0: return "heads"
  return "tails"


def get_help() -> str:
  return "Here are the coolest commands: \na!cat \na!inspire \na!null \na!roast \na!say \na!shout \n\nHere's a list of all the commands: \nhttps://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit?usp=sharing"


def get_author(message: discord.Message) -> str:
  my_author = str(message.author)
  my_author = my_author[:len(my_author) - 5]
  return my_author


def say(message: discord.Message, my_string: str) -> None:
  return message.channel.send(my_string)


def say_hello(message: discord.Message) -> str:
    my_author = get_author(message)
    greeting = random.choice(greetings).capitalize()
    return greeting + ', ' + my_author + '!'


def shout(message: discord.Message, my_string: str) -> None:
  return message.channel.send(my_string.upper())
  