import random
import discord


greetings = ['hello', 'hi', 'greetings', 'hey', 'yo', 'ahoy', 
'salutations', 'howdy']


def bad_anal_joke(message: discord.Message) -> str:
  return message.channel.send("I'm flattered, " + get_author(message) 
  + ", but I'll have to decline.")


def coinflip() -> str:
  if random.choice([0, 1]) == 0: return "Heads."
  return "Tails."


def get_help() -> str:
  return "Here's a list of commands: \nhttps://docs.google.com/document/d/1MCxDtjRRnO61RX7Chbed5VbXZOBBWARwsXb7EAhrn1U/edit?usp=sharing"


def get_author(message: discord.Message) -> str:
  my_author = str(message.author)
  return my_author[:len(my_author) - 5]


def say(message: discord.Message, my_string: str) -> None:
  return message.channel.send(my_string)


def say_hello(message: discord.Message) -> str:
    greeting = random.choice(greetings).capitalize()
    return greeting + ', ' + get_author(message) + '!'


def shout(message: discord.Message, my_string: str) -> None:
  return message.channel.send(my_string.upper())
  