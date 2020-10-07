import os

import discord
from discord.ext import commands
from pretty_help import PrettyHelp

import config
from utils.LoggerFactory import LoggerFactory

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())
logger = LoggerFactory.get_logger()


@bot.event
async def on_ready():
    logger.info("Connected")


def load_commands():
    logger.info("Loading commands...")
    for file_name in os.listdir(config.COMMANDS_FOLDER):
        if file_name.endswith(".py"):
            bot.load_extension(f"{config.COMMANDS_FOLDER}.{file_name[:-3]}")

    logger.info("Loaded commands")


def main():
    logger.info(config.ASCII_ART)
    load_commands()
    logger.info("Connecting to discord servers...")
    bot.run(config.TOKEN)


if __name__ == '__main__':
    main()
