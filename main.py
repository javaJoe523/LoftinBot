import discord
import os
import random
import const
import helpers
 
client = discord.Client()
 
async def send_cmd_msg(message, options):
 # Remove empty options
 options = [o for o in options if o is not None]
 if options:
   response = random.choice(options)
   await message.channel.send(response)
 
async def send_chat_msg(message, keys, options):
 # Remove empty options
 msg = helpers.get_message_content(message)
 options = [o for o in options if o is not None]
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
  # Define Commands so that they will be handled dynamically
  cmd_func_list = {
    '!help':       {'value': [const.HELP_INFO]},
    '!hello':      {'value': const.GREETING},
    '!rps':        {'value': const.RPS},
    '!8ball':      {'value': const.YES_NO},
    '!inspire':    {'func': helpers.get_quote},
    '!fact':       {'func': helpers.get_fact},
    '!dice':       {'func': helpers.roll_dice},
    '!space':      {'func': helpers.get_space_pic},
    '!sortinghat': {'func': helpers.get_sorting_house},
    '!french':     {'func': helpers.translate_msg, 'kwargs':{'query': '', 'code': 'fr'}},
    '!spanish':    {'func': helpers.translate_msg, 'kwargs':{'query': '', 'code': 'es'}},
    '!italian':    {'func': helpers.translate_msg, 'kwargs':{'query': '', 'code': 'it'}},
    '!daysuntil':  {'func': helpers.date_diff, 'kwargs': {'query': ''}},
    '!weather':    {'func': helpers.get_cur_weather, 'kwargs':{'query': ''}},
    '!broadcast':  {'func': helpers.broadcast_msg, 'kwargs': {'query': ''}}
  }

  # Handle Command Messages
  msg_commands = list(filter(lambda c: c in msg, cmd_func_list.keys()))
  for c in msg_commands:
   assert cmd_func_list[c]
   if cmd_func_list[c].get('value'):
     await send_cmd_msg(message, cmd_func_list[c].get('value'))
   else:
     func = cmd_func_list[c].get('func')
     kwargs = cmd_func_list[c].get('kwargs', {})
     if 'query' in kwargs:
       kwargs['query'] = helpers.get_cmd_input(msg, c)
     print('INFO: Possible API request for {0} for {1}'.format(func.__name__, c))
     await send_cmd_msg(message, func(**kwargs))

  # Handle Chat Messages
  await send_chat_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)
 
client.run(os.getenv('DISCORD_TOKEN'))