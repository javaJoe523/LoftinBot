import discord
import os
import requests
import json
import random
import const
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build

client = discord.Client()

def get_quote(msg):
  if (not allow_cmd(msg, ['!inspire'])):
    return (['']) 
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return ([quote])

def get_fact(msg):
  if (not allow_cmd(msg, ['!fact'])):
    return (['']) 
  response = requests.get("https://uselessfacts.jsph.pl/random.txt?language=en")
  return ([response.text])

def get_space_pic(msg):
  if (not allow_cmd(msg, ['!space'])):
    return ([''])
  startdate=date.today()
  date_str=startdate-timedelta(random.randint(1,365))
  api_key=os.getenv('NASA_API_KEY')
  response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date_str}')
  json_data = json.loads(response.text)
  return ([json_data['url']])

def date_diff(msg):
  if (not allow_cmd(msg, const.CMD_DAYSUNTIL)):
    return ([''])
  msg = get_cmd_input(msg, '!daysuntil')
  today = date.today()
  to_date = datetime.strptime(msg, "%m/%d/%Y").date()
  return ([(to_date - today).days])

def translate_msg(msg, cmd, code):
  # TODO: Use a dictionary for code
  if (not allow_cmd(msg, [cmd])):
    return ([''])
  msg = get_cmd_input(msg, cmd)
  if not msg:
    return ([''])

  service = build('translate', 'v2', developerKey=os.getenv('GOOGLE_API_KEY'))
  json_data = service.translations().list( source='en', target=code, q=[msg] ).execute()
  return ([json_data['translations'][0]['translatedText']])

def get_cur_weather(msg):
  if (not allow_cmd(msg, ['!weather'])):
    return ([''])
  query = get_cmd_input(msg, '!weather')
  
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
  try:
    json_data = json_data['locations'][f'{query}']['currentConditions']
  except:
    print("Could not find currentConditions.")
  cur_temp   = json_data['temp']
  heat_index = json_data['heatindex']
  windchill  = json_data['windchill']
  humidity   = json_data['humidity']

  # Create the message
  result = f'The current temperature in {query} is {cur_temp}'
  if (heat_index is not None):
    result += f' but it feels like {heat_index}'
  if (windchill is not None):
    result += f' but there is a windchill of {windchill}'
  result += f'. The current humidity is {humidity}%.'
  return ([result])

def allow_cmd(msg, options):
  return (msg and any(c in msg for c in options))

def get_help():
  return ([const.HELP_INFO])

def get_message_content(message):
  return message.content.lower().strip() if (message and message.content) else message

def get_cmd_input(msg, cmd):
  pos = msg.lower().find(cmd) + len(cmd) + 1
  return msg[pos::].strip()

async def send_msg(message, keys, options, check_key=True):
  # Remove empty options
  options = [o for o in options if o]
  # Check options and pick a random one
  if options and (not check_key or allow_cmd(get_message_content(message), keys)):
    response = random.choice(options)
    await message.channel.send(response)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = get_message_content(message)

  await send_msg(message, ['!hello'], const.GREETING)
  await send_msg(message, ['!inspire'], get_quote(msg), False)
  await send_msg(message, ['!8ball'], const.YES_NO)
  await send_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)
  await send_msg(message, ['!fact'], get_fact(msg), False)
  await send_msg(message, ['!rps'], const.RPS)
  await send_msg(message, ['!dice'], ([random.randint(2,12)]))
  await send_msg(message, ['!french'], translate_msg(msg, '!french', 'fr'), False)
  await send_msg(message, ['!spanish'], translate_msg(msg, '!spanish', 'es'), False)
  await send_msg(message, ['!italian'], translate_msg(msg, '!italian', 'it'), False)
  await send_msg(message, ['!daysuntil'], date_diff(msg))
  await send_msg(message, ['!weather'], get_cur_weather(msg), False)
  await send_msg(message, ['!space'], get_space_pic(msg), False)
  await send_msg(message, ['!help'], get_help())

  #Custom
  if '!sortinghat' in msg:
    h = random.choice(const.HOUSES)
    if (h == "Muggle"):
      msg = "I'm sorry but you are a muggle."
    else:
      msg = ("You are in house "+h+".")
    await message.channel.send(msg)

client.run(os.getenv('DISCORD_TOKEN'))
