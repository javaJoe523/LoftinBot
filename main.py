import discord
import os
import requests
import json
import random

greeting = ['Hello!', 'Yo!', 'Greetings Human.', 'Pleasant to meet you.']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
yes_no = ['Yes', 'No', 'Maybe', 'Not likely']
houses = ['Ravenclaw', 'Hufflepuff', 'Gryffindor', 'Slytherin', 'Muggle']
encouragements = [
  'Cheer up!',
  'Hang in there.',
  'You are a great person / bot!'
]

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return ([quote])

def get_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.txt?language=en")
  return ([response.text])

def get_help():
  help_info = "!help: This message | !hello: Greet the bot | !inspire: Motivational Quotes | !8ball | !dice: Roll the dice | !fact | !sortinghat"
  return ([help_info])

async def send_msg(message, keys, options):
  msg = message.content
  if any(word in msg for word in keys):
    response = random.choice(options)
    await message.channel.send(response)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  await send_msg(message, ['!hello'], greeting)
  await send_msg(message, ['!inspire'], get_quote())
  await send_msg(message, ['!8ball'], yes_no)
  await send_msg(message, sad_words, encouragements)
  await send_msg(message, ['!fact'], get_fact())
  await send_msg(message, ['dice'], ([random.randint(2,12)]))
  await send_msg(message, ['!help'], get_help())

  #Custom
  if '!sortinghat' in message.content:
    h = random.choice(houses)
    if (h == "Muggle"):
      msg = "I'm sorry but you are a muggle."
    else:
      msg = ("You are in house "+h+".")
    await message.channel.send(msg)

client.run(os.getenv('discord_token'))
