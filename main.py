import discord
import os
import random
import const
import helpers
 
client = discord.Client()
 
async def send_cmd_msg(message, cmd, options):
 # Remove empty options
 options = [o for o in options if o]
 if options:
   response = random.choice(options)
   await message.channel.send(response)
 
async def send_chat_msg(message, keys, options):
 # Remove empty options
 msg = helpers.get_message_content(message)
 options = [o for o in options if o]
 if options and helpers.has_option(msg, keys):
   response = random.choice(options)
   await message.channel.send(response)
 
@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = helpers.get_message_content(message)
  msg_commands = list(filter(lambda c: c in msg, const.COMMANDS))
  # Define Commands so that they will be handled dynamically
  cmd_func_list = {
    '!hello': {'value': const.GREETING},
    '!inspire': {'func': 'get_quote', 'args': {'msg': msg}},
    '!8ball': {'value': const.YES_NO },
    '!fact': {'func': 'get_fact', 'args': {'msg': msg}},
    '!rps': {'value': const.RPS },
    '!dice': {'func': 'roll_dice', 'args': {'msg': msg}},
    '!french': {'func': helpers.translate_msg, 'args':{'msg': msg, 'cmd': '!french', 'code': 'fr'}},
    '!spanish': {'func': helpers.translate_msg, 'args':{'msg': msg, 'cmd': '!spanish', 'code': 'es'}},
    '!italian': {'func': helpers.translate_msg, 'args':{'msg': msg, 'cmd': '!italian', 'code': 'it'}},
    '!daysuntil': {'func': 'date_diff', 'args': {'msg': msg}},
    '!weather': {'func':'get_cur_weather', 'args':{'msg': msg}},
    '!space': {'func':'get_space_pic', 'args':{'msg': msg}},
    '!sortinghat': {'func':'get_sorting_house', 'args':{'msg': msg}},
    '!help': {'value': [const.HELP_INFO] }
  }

  # Handle Command Messages
  for c in msg_commands:
   assert cmd_func_list[c]
   if cmd_func_list[c].get('value'):
     await send_cmd_msg(message, c, cmd_func_list[c]['value'])
   else:
     func = cmd_func_list[c]['func']
     kwargs = cmd_func_list[c]['args']
     print('INFO: Possible API request for {0} for {1}'.format(func.__name__, c))
     await send_cmd_msg(message, c, func(**kwargs))

  # Handle Chat Messages
  await send_chat_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)
 
client.run(os.getenv('DISCORD_TOKEN'))