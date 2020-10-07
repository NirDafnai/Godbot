from discord.ext import commands

from utils.LoggerFactory import LoggerFactory


class SummonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LoggerFactory.get_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Summon command ready")

    @commands.command(name="summon", aliases=("s",))
    async def summon(self, context: commands.Context):
        await context.send(f"{context.author.display_name} is summoning @everyone")


def setup(bot):
    bot.add_cog(SummonCog(bot))
