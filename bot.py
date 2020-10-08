import os
from pathlib import Path

from discord.ext import commands

import config
from utils.LoggerFactory import LoggerFactory

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, help_command=None)
logger = LoggerFactory.get_logger()


@bot.event
async def on_ready():
    logger.info("Connected")


def load_commands():
    logger.info("Loading commands...")
    with os.scandir(config.COMMANDS_FOLDER) as directory:
        files = [f for f in directory if f.is_file()]
        for file_path in files:
            try:
                bot.load_extension(f"{config.COMMANDS_FOLDER}.{Path(file_path).stem}")
            except commands.errors.ExtensionNotFound:
                logger.warning(f"Could not load file {file_path.name}.")

    logger.info("Loaded commands")


def main():
    logger.info(config.ASCII_ART)
    load_commands()
    logger.info("Connecting to discord servers...")
    bot.run(config.TOKEN)


if __name__ == '__main__':
    main()
