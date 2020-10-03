@client.event
async def on_voice_state_update(member, before, after):
    """
        This function is called when:
        * A member joins a voice channel.
        * A member leaves a voice channel.
        In this case, whenever a user joins an empty voice channel, it summons everyone in the chat.
        :param member: The member that joined
        :type member: discord.Member
        :param before: The member's VoiceState before he joined.
        :type before: discord.VoiceState
        :param after: The member's VoiceState after he joined.
        :type after: discord.VoiceState
    """
    if before.channel is None and len(after.channel.members) == 1:
        for text_channel in after.channel.guild.text_channels:
            if text_channel.name.lower() == GENERAL_CHANNEL_NAME:
                await text_channel.send("{} is summoning @everyone".format(member.display_name))
                break