import config

from discord import Member, VoiceState, RawReactionActionEvent
from discord.ext import commands

from cogs.create_vote import CreateVoteCog


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel != after.channel and after.channel is not None:
            if len(after.channel.members) == 1:
                if after.channel.id in config.VOICE_CHANNEL_SUMMON_IDS:
                    for text_channel_id in config.TEXT_CHANNEL_ALERT_IDS:
                        await self.bot.get_channel(text_channel_id).send(f"{member.display_name} is summoning @everyone")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.member.bot:
            return
        for vote_message in CreateVoteCog.votes:
            if payload.message_id == vote_message.id:
                live_message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for reaction in live_message.reactions:
                    if payload.member in await reaction.users().flatten() and reaction.emoji != payload.emoji.name:
                        await live_message.remove_reaction(reaction.emoji, payload.member)
                break




def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
