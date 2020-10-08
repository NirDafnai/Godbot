from discord.ext import commands
from discord import Embed

from utils.LoggerFactory import LoggerFactory


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LoggerFactory.get_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Help command ready")

    @commands.command(name="help", aliases=("h",), description="Returns all commands available")
    async def help_command(self, context: commands.Context):
        help_message = Embed(title="Commands")
        for command in self.bot.commands:
            command_name = f"{self.bot.command_prefix}{command.name}"
            if command.clean_params is not None:
                command_name = " ".join([command_name, *[f"{{{param}}}" for param in command.clean_params]])
            help_message.add_field(name=command_name, value=command.description, inline=False)
        await context.send(embed=help_message)


def setup(bot):
    bot.add_cog(HelpCog(bot))
