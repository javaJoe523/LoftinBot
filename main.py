import discord
import os
import requests
import json
import random
import const
from datetime import date, datetime

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return ([quote])

def get_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.txt?language=en")
  return ([response.text])

def date_diff(msg):
  if (not msg or not msg.content or msg.content not in const.CMD_DAYSUNTIL):
    return
  msg = get_cmd_input(msg, const.CMD_DAYSUNTIL)
  today = date.today()
  to_date = datetime.strptime(msg, "%m/%d/%Y").date()
  return ([(to_date - today).days])

def translate_msg(msg, code):
  if (not msg or not msg.content or msg.content not in const.CMD_LANG):
    return
  if (len(msg.content.split(' ', 1)) <= 1):
    return (["Invalid Message"])

  msg = msg.content.lower().split(' ', 1)[1]
  url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
  payload = f"q={msg}&format=text&target={code}&source=en"
  headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept-encoding': "application/gzip",
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
    'x-rapidapi-host': "google-translate1.p.rapidapi.com"
  }
  response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
  json_data = json.loads(response.text)
  return ([json_data["data"]["translations"][0]["translatedText"]])

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
  return ([const.HELP_INFO])

def get_cmd_input(message, cmd):
  msg = message.content.lower()
  pos = msg.find(cmd) + len(cmd)
  return msg[pos::]

async def send_msg(message, keys, options):
  msg = message.content.lower()
  if any(word.lower() in msg for word in keys):
    response = random.choice(options)
    await message.channel.send(response)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  await send_msg(message, ['!hello'], const.GREETING)
  await send_msg(message, ['!inspire'], get_quote())
  await send_msg(message, ['!8ball'], const.YES_NO)
  await send_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)
  await send_msg(message, ['!fact'], get_fact())
  await send_msg(message, ['!rps'], const.RPS)
  await send_msg(message, ['!dice'], ([random.randint(2,12)]))
  await send_msg(message, ['!french'], translate_msg(message, 'fr'))
  await send_msg(message, ['!spanish'], translate_msg(message, 'es'))
  await send_msg(message, ['!italian'], translate_msg(message, 'it'))
  await send_msg(message, ['!daysuntil'], date_diff(message))
  await send_msg(message, ['!help'], get_help())

  #Custom
  msg = message.content
  if '!sortinghat' in msg:
    h = random.choice(const.HOUSES)
    if (h == "Muggle"):
      msg = "I'm sorry but you are a muggle."
    else:
      msg = ("You are in house "+h+".")
    await message.channel.send(msg)

  if msg.startswith('!weather'):
    result = get_cur_weather(msg.replace('!weather', '').strip())
    await message.channel.send(result)

client.run(os.getenv('DISCORD_TOKEN'))
