from discord.ext import commands

from utils.LoggerFactory import LoggerFactory


class SkeletonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LoggerFactory.get_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Skeleton command ready")

    @commands.command(name="skeleton", aliases=("s", "skel"))
    async def skeleton_command(self, context: commands.Context):
        pass


def setup(bot):
    bot.add_cog(SkeletonCog(bot))
