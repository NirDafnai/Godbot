import time

from discord import Embed, Colour
from discord.ext import commands
from concurrent.futures._base import TimeoutError as DiscordTimeoutError

AGREE = "✅"
DISAGREE = "❎"


class CreateVoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_vote", aliases=("cv", "createvote"))
    async def create_vote(self, context: commands.Context, poll_time: int, *, question: str):
        poll = Embed(title="Poll", description=question)
        sent_msg = await context.channel.send(embed=poll)
        await sent_msg.add_reaction(AGREE)
        await sent_msg.add_reaction(DISAGREE)
        current_time = time.time()
        agree_count = 0
        disagree_count = 0
        while time.time() - current_time < poll_time:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add',
                                                      check=lambda user_reaction, user:
                                                      user_reaction.message.id == sent_msg.id
                                                      and user_reaction.me
                                                      and (user_reaction.emoji == AGREE
                                                           or user_reaction.emoji == DISAGREE), timeout=0.1)
            except DiscordTimeoutError:
                pass
            else:
                if reaction.emoji == AGREE:
                    agree_count += 1
                    print("Someone agreed")
                elif reaction.emoji == DISAGREE:
                    disagree_count += 1
            try:
                reaction, _ = await self.bot.wait_for('reaction_remove',
                                                      check=lambda user_reaction, user:
                                                      user_reaction.message.id == sent_msg.id
                                                      and user.id != self.bot.user.id
                                                      and (user_reaction.emoji == AGREE
                                                           or user_reaction.emoji == DISAGREE), timeout=0.1)

            except DiscordTimeoutError:
                pass
            else:
                if reaction.emoji == AGREE:
                    agree_count -= 1
                    print("Someone agreed")
                elif reaction.emoji == DISAGREE:
                    disagree_count -= 1
                    print("Someone disagreed")

        results = Embed(title="Poll Results", description=f"Results for the poll: {question}")
        results.add_field(name="Results:", value=f"{AGREE}: {str(agree_count)}  {DISAGREE}: {str(disagree_count)}")
        await context.channel.send(embed=results)
        await sent_msg.delete()


def setup(bot):
    bot.add_cog(CreateVoteCog(bot))
