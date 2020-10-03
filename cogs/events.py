import config

from discord import Member
from discord import VoiceState
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel != after.channel and after.channel is not None:
            if after.channel.id in config.VOICE_CHANNEL_SUMMON:
                for text_channel_id in config.TEXT_CHANNEL_ALERT:
                    await self.bot.get_channel(text_channel_id).send(f"{member.display_name} is summoning @everyone")


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
