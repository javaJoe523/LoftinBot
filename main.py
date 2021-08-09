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

def get_cur_weather(query):
  # Call the API
  url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
  querystring = {"location":query,"aggregateHours":"24","shortColumnNames":"0","unitGroup":"us","contentType":"json"}
  headers = {
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
    'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  # Get specific data
  cur_temp = json_data['locations'][f'{query}']['currentConditions']['temp']
  heat_index = json_data['locations'][f'{query}']['currentConditions']['heatindex']
  windchill = json_data['locations'][f'{query}']['currentConditions']['windchill']
  humidity = json_data['locations'][f'{query}']['currentConditions']['humidity']
  # Create the message
  result = f'The current temperature in {query} is {cur_temp}'
  if (heat_index is not None):
    result += f' but it feels like {heat_index}'
  if (windchill is not None):
    result += f' but there is a windchill of {windchill}'
  result += f'. The current humidity is {humidity}%.'
  return (result)

def get_help():
  help_info = "!help: This message | !hello: Greet the bot | !inspire: Motivational Quotes | !8ball: Ask the 8 ball a question | !dice: Roll the dice | !fact: Random Fact | !sortinghat: Sorts you into a Harry Potter House | !weather {location}: Check the current temperature"
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
  await send_msg(message, ['!dice'], ([random.randint(2,12)]))
  await send_msg(message, ['!help'], get_help())

  #Custom
  msg = message.content
  if '!sortinghat' in msg:
    h = random.choice(houses)
    if (h == "Muggle"):
      msg = "I'm sorry but you are a muggle."
    else:
      msg = ("You are in house "+h+".")
    await message.channel.send(msg)

  if msg.startswith('!weather'):
    result = get_cur_weather(msg.replace('!weather', '').strip())
    await message.channel.send(result)

client.run(os.getenv('DISCORD_TOKEN'))
