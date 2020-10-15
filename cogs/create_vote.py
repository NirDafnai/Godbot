from datetime import datetime
import asyncio

from discord import Embed, RawReactionActionEvent, Message
from discord.ext import commands

from utils.LoggerFactory import LoggerFactory

AGREE = "✅"
DISAGREE = "❎"


class CreateVoteCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.context = None
        self.votes = []
        self.logger = LoggerFactory.get_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Create vote command ready")

    async def create_vote_message(self, vote_question, vote_seconds):
        vote_message = Embed(title="Poll",
                             description=vote_question,
                             colour=self.context.author.colour,
                             timestamp=datetime.utcnow())

        fields = [("Options", "\n".join((f"{AGREE} - Yes", f"{DISAGREE} - No")), False),
                  ("Instructions", "React to cast a vote!", False)]
        for name, value, inline in fields:
            vote_message.add_field(name=name, value=value, inline=inline)

        return vote_message

    async def send_vote_message(self, vote_message):
        message_sent = await self.context.send(embed=vote_message)
        await message_sent.add_reaction(AGREE)
        await message_sent.add_reaction(DISAGREE)
        return message_sent

    @commands.command(name="create_vote", aliases=("cv", "createvote"), description="Creates a vote on a chosen topic.")
    async def create_vote(self, context: commands.Context, vote_seconds: int, *, vote_question: str):
        self.context = context

        vote_message = await self.create_vote_message(vote_question, vote_seconds)
        message_sent = await self.send_vote_message(vote_message)

        self.votes.append(message_sent)
        await asyncio.sleep(vote_seconds)
        await self.end_poll(context, message_sent, vote_question)

    async def end_poll(self, context: commands.Context, vote_message: Message, vote_question: str):
        live_message = await vote_message.channel.fetch_message(vote_message.id)
        filtered_reactions = [reaction for reaction in live_message.reactions if reaction.emoji in [AGREE, DISAGREE]]

        most_voted = max(filtered_reactions, key=lambda reactions: reactions.count)
        least_voted = min(filtered_reactions, key=lambda reactions: reactions.count)
        await context.send(f"Question: {vote_question}\n\n{most_voted.emoji} - {most_voted.count - 1}\n\n"
                           f"{least_voted.emoji} - {least_voted.count - 1}")
        self.votes.remove(vote_message)
        await live_message.delete()

    @commands.Cog.listener("on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.member.bot:
            return
        for vote_message in self.votes:
            if payload.message_id == vote_message.id:
                live_message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for reaction in live_message.reactions:
                    if payload.member in await reaction.users().flatten() and reaction.emoji != payload.emoji.name:
                        await live_message.remove_reaction(reaction.emoji, payload.member)
                return



def setup(bot):
    bot.add_cog(CreateVoteCog(bot))
