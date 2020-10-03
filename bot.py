import os

import discord
from discord.ext import commands
from pretty_help import PrettyHelp

import config

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())


@bot.event
async def on_ready():
    print("[+] Connected.")


def load_commands():
    for file_name in os.listdir(config.COMMANDS_FOLDER):
        if file_name.endswith(".py"):
            bot.load_extension(f"{config.COMMANDS_FOLDER}.{file_name[:-3]}")

    print("[+] Loaded commands.")


def main():
    print(config.ASCII_ART)
    print("[*] Loading commands...")
    load_commands()
    print("[*] Connecting to discord servers...")
    bot.run(config.TOKEN)


if __name__ == '__main__':
    main()
