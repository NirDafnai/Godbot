from discord.ext import commands


class SkeletonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skeleton", aliases=("s", "skel"))
    async def skeleton_command(self, context: commands.Context):
        pass


def setup(bot):
    bot.add_cog(SkeletonCog(bot))
