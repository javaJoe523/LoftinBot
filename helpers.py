import os
import requests
import json
import random
import const
import assistant
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build
 
def get_quote():
 response = requests.get(const.INSPIRE_API_URL)
 json_data = json.loads(response.text)
 quote = json_data[0]['q'] + " -" + json_data[0]['a']
 return ([quote])
 
def get_fact():
 response = requests.get(const.FACT_API_URL)
 return ([response.text])
 
def get_space_pic():
 startdate=date.today()
 date_str=startdate-timedelta(random.randint(1,365))
 api_key=os.getenv('NASA_API_KEY')
 response = requests.get(f'{const.NASA_API_URL}?api_key={api_key}&date={date_str}')
 json_data = json.loads(response.text)
 return ([json_data['url']])
 
def date_diff(query):
 if not query:
   return ([''])
 today = date.today()
 to_date = datetime.strptime(query, "%m/%d/%Y").date()
 return ([(to_date - today).days])
 
def translate_msg(query, code):
 if not query:
   return ([''])
 service = build('translate', 'v2', developerKey=os.getenv('GOOGLE_API_KEY'))
 json_data = service.translations().list( source='en', target=code, q=[query] ).execute()
 return ([json_data['translations'][0]['translatedText']])
 
def get_cur_weather(query):
  # Call the API
 querystring = {"location":query,"aggregateHours":"24","shortColumnNames":"0","unitGroup":"us","contentType":"json"}
 headers = {
   'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
   'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
 }
 response = requests.get(
   const.WEATHER_API_URL,
   headers=headers,
   params=querystring
 )
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
 
def roll_dice():
 return ([random.randint(2,12)])
 
def get_sorting_house():
 h = random.choice(const.HOUSES)
 if (h == "Muggle"):
   return (["I'm sorry but you are a muggle."])
 else:
   return([f'You are in house {h}.'])

def broadcast_msg(query):
  # TODO: See if we can verify that a broadcast sent
  if query is not None:
    response = assistant.send_request("broadcast "+query)
    if response is not None and response.startswith('ERROR'):
      return (['Something went wrong :('])
  return (['Message Sent'])

#################
# General Helpers
#################

def has_option(msg, options):
 return (msg and any(c in msg for c in options))
 
def get_message_content(message):
 return message.content.lower().strip() if (message and message.content) else message
 
def get_cmd_input(msg, cmd):
 pos = msg.lower().find(cmd) + len(cmd) + 1
 return msg[pos::].strip()