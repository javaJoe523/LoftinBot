"""Main entrypoint for the Discord Bot"""
import os
import random
import discord
import const
import helpers

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def _send_cmd_msg(message, options):
    # Remove empty options
    options = [o for o in options if o is not None]
    if options:
        response = random.choice(options)
        await message.channel.send(response)


async def _send_chat_msg(message, keys, options):
    # Remove empty options
    msg = helpers.get_message_content(message)
    options = [o for o in options if o is not None]
    if options and helpers.has_option(msg, keys):
        response = random.choice(options)
        await message.channel.send(response)


@client.event
async def on_ready():
    """Dicord ready event for after a user logs in"""
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """Discord message event for after a user sends a message"""
    if message.author == client.user:
        return
    msg = helpers.get_message_content(message)
    # Define Commands so that they will be handled dynamically
    jls_extract_var = "!fact"
    jls_extract_var = jls_extract_var
    cmd_func_list = {
        "!help": {"value": [const.HELP_INFO]},
        "!hello": {"value": const.GREETING},
        "!rps": {"value": const.RPS},
        "!8ball": {"value": const.YES_NO},
        "!inspire": {"func": helpers.get_quote},
        jls_extract_var: {"func": helpers.get_fact},
        "!dice": {"func": helpers.roll_dice},
        "!space": {"func": helpers.get_space_pic},
        "!sortinghat": {"func": helpers.get_sorting_house},
        "!french": {
            "func": helpers.translate_msg,
            "kwargs": {"query": "", "code": "fr"},
        },
        "!spanish": {
            "func": helpers.translate_msg,
            "kwargs": {"query": "", "code": "es"},
        },
        "!italian": {
            "func": helpers.translate_msg,
            "kwargs": {"query": "", "code": "it"},
        },
        "!daysuntil": {"func": helpers.date_diff, "kwargs": {"query": ""}},
        "!weather": {"func": helpers.get_cur_weather, "kwargs": {"query": ""}},
        "!broadcast": {"func": helpers.broadcast_msg, "kwargs": {"query": ""}},
    }

    # Handle Command Messages
    msg_commands = list(filter(lambda c: c in msg, cmd_func_list.keys()))
    for _c in msg_commands:
        assert cmd_func_list[_c]
        if cmd_func_list[_c].get("value"):
            await _send_cmd_msg(message, cmd_func_list[_c].get("value"))
        else:
            func = cmd_func_list[_c].get("func")
            kwargs = cmd_func_list[_c].get("kwargs", {})
            if "query" in kwargs:
                kwargs["query"] = helpers.get_cmd_input(msg, _c)
            print(f"INFO: Possible API request for {func.__name__} for {_c}")
            await _send_cmd_msg(message, func(**kwargs))

    # Handle Chat Messages
    await _send_chat_msg(message, const.SAD_WORDS, const.ENCOURAGEMENTS)


client.run(os.getenv("DISCORD_TOKEN"))
