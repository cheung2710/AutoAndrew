import random

bad_words = ['fuck', 'shit', 'bitch']
greetings = ['hello', 'hi', 'greetings', 'hey', 'yo']


def bad_anal_joke(message):
  name = get_author(message)
  return message.channel.send("I'm flattered, " + name + ", but I'll have to decline.")


async def check_bad_words(message):
  """Sends a message if anyone says a word in the bad_words[] list."""
  for word in bad_words:
      if word in message.content:
        my_author = get_author(message)
        await message.channel.send(my_author + ", watch your fucking language!")


def coinflip():
  if random.choice([0, 1]) == 0: return "heads"
  return "tails"


def get_help():
  return "Here are the coolest commands: \na!cat \na!inspire \na!null \na!roast \na!say \na!shout \n\nHere's a list of all the commands: \nhttps://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit?usp=sharing"


def get_author(message):
  my_author = str(message.author)
  my_author = my_author[:len(my_author) - 5]
  return my_author


def say(message, s):
  return message.channel.send(s)


def say_hello(message):
    my_author = get_author(message)
    greeting = random.choice(greetings).capitalize()
    return greeting + ', ' + my_author + '!'


def shout(message, s):
  return message.channel.send(s.upper())