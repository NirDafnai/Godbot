from discord.ext import commands


class SummonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[+] Summon command ready.")

    @commands.command(name="summon", aliases=("s",))
    async def summon(self, context: commands.Context):
        await context.send(f"{context.author.display_name} is summoning @everyone")


def setup(bot):
    bot.add_cog(SummonCog(bot))
