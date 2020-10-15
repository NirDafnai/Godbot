"""
Use pip install -e . on when in the parent directory to install the CLI tool
Or just run with python generate_command.py


"""
import click
from typing import Tuple

TEMPLATE = """from discord.ext import commands

from utils.LoggerFactory import LoggerFactory


class <CAP_NAME>Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LoggerFactory.get_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("<CAP_NAME> command ready")

    @commands.command(name="<NAME>", aliases=(<ALIASES>))
    async def <NAME>_command(self, context: commands.Context):
        pass
"""


@click.command()
@click.argument("command")
@click.option("--alias", "-a", multiple=True, help="Alias for the command")
def create_command(command: str, alias: Tuple[str]):
    """A CLI tool used to generate command from a template."""
    replaces = {
        "<NAME>": command,
        "<CAP_NAME>": command.capitalize(),
        "<ALIASES>": ", ".join([f'"{a}"' for a in alias])
    }
    result = TEMPLATE
    with open(f"{command}.py", "w") as f:
        for flag, replacement in replaces.items():
            result = result.replace(flag, replacement)
        f.write(result)


if __name__ == "__main__":
    create_command()
