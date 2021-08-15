import discord
import os
import random
import const
import helpers

client = discord.Client()

async def send_msg(message, keys, options, check_key=True):
  # Remove empty options
  options = [o for o in options if o]
  # Check options and pick a random one
  # TODO: Possibly use a decorator here
  if options and (not check_key or helpers.allow_cmd(helpers.get_message_content(message), keys)):
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

  await send_msg(message, ['!hello'], const.GREETING)
  await send_msg(message, ['!inspire'], helpers.get_quote(msg), False)
  await send_msg(message, ['!8ball'], const.YES_NO)
  await send_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)
  await send_msg(message, ['!fact'], helpers.get_fact(msg), False)
  await send_msg(message, ['!rps'], const.RPS)
  await send_msg(message, ['!dice'], helpers.roll_dice(msg), False)
  await send_msg(message, ['!french'], helpers.translate_msg(msg, '!french', 'fr'), False)
  await send_msg(message, ['!spanish'], helpers.translate_msg(msg, '!spanish', 'es'), False)
  await send_msg(message, ['!italian'], helpers.translate_msg(msg, '!italian', 'it'), False)
  await send_msg(message, ['!daysuntil'], helpers.date_diff(msg))
  await send_msg(message, ['!weather'], helpers.get_cur_weather(msg), False)
  await send_msg(message, ['!space'], helpers.get_space_pic(msg), False)
  await send_msg(message, ['!help'], helpers.get_help())
  await send_msg(message, ['!sortinghat'], helpers.get_sorting_house(msg), False)

client.run(os.getenv('DISCORD_TOKEN'))
