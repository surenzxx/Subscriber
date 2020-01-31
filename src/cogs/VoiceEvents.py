import datetime
from discord.ext import commands
import discord 
import re 
from discord import utils

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            print(member.name + " just joined a channel!")
            print("{} has joined {} in {}".format(member.name, after.channel.name, member.guild))
            # Get all users subscribed to the channel.
            # For each user subscribed to channel, first check if their whitelist is enabled.
            # If enabled, check if user who joined is in it. If not, don't DM user.
            # If user is whitelisted, send DM.
            # Set a flag called is_notified to indicate user was notified, prevent spam.
            whitelisters = self.bot.db.get_all_subbed_users(str(after.channel.id), str(member.guild.id), str(member.id))
            # Does not work if user doesnt have whitelist. Need to check the user's whitelist first.
            for w in whitelisters:
                for member in after.channel.members:
                    if str(w) == str(member.id):
                        #print(str(w) + " did match " + str(member.id))
                        break
                    else:
                        #print(str(w) + " didn't match " + str(member.id))
                        user = utils.find(lambda u : u.id == int(w), member.guild.members)
                        if user is not None:
                            #await user.send('{} joined {} in {}'.format(member.name, after.channel.name, member.guild))
                            join_message=('{} joined {} in {}'.format(member.name, after.channel.name, member.guild))
                            invitelinknew = await after.channel.create_invite(destination=after.channel.name)
                            embed = discord.Embed()
                            embed.title = join_message
                            embed.description = invitelinknew.url
                            #embed.url = invitelinknew.url
                            #embed.color = 8097750
                            embed.set_footer(text="Click the link above to join")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url) 
                            #invitelinknew.url
                            #embed.description = invitelinknew.url
                            #embed.set_footer(text=invitelinknew.url)
                            await user.send(embed=embed)


        elif before.channel is not None and after.channel is not None:
            print("{} switched from {} to {}".format(member.name, before.channel.name, after.channel.name))
            whitelisters = self.bot.db.get_all_subbed_users(str(after.channel.id), str(member.guild.id), str(member.id))
            
            for id in whitelisters:
                user = utils.find(lambda u : u.id == int(id), member.guild.members)
                if user is not None:
                    print("{} has switched to {} in {}".format(member.name, after.channel.name, before.channel.name))
                    #await user.send('{} has switched to {} from {}'.format(member.name, after.channel.name, before.channel.name))
        elif before.channel is not None and after.channel is None:
            print("{} left {} in {}".format(member.name, before.channel.name, member.guild))
            whitelisters = self.bot.db.get_all_subbed_users(str(before.channel.id), str(member.guild.id), str(member.id))
            for id in whitelisters:
                user = utils.find(lambda u : u.id == int(id), member.guild.members)
                if user is not None:
                    print("{} has left {}".format(member.name, before.channel.name))
                    #await user.send('{} has left {}'.format(member.name, before.channel.name))


        

        
def setup(bot):
    bot.add_cog(VoiceEvents(bot))
