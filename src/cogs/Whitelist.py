from discord.ext import commands
import discord
import re

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['wl'], invoke_without_command=True)
    async def whitelist(self, ctx):
        whitelist = self.bot.db.get_user_whitelist(ctx)
        print(whitelist)
        if bool(whitelist):
            print(whitelist)
        else:
            print('empty')
        
    @whitelist.command(name='add', aliases=['a'])
    async def whitelist_add(self, ctx, channel, *args):
        # self.db.add_wl(ctx)
        try:
            voice_channel = discord.utils.find(lambda c: c.id == int(channel), ctx.guild.voice_channels)
            if voice_channel is not None:
                self.parse_users(ctx, voice_channel, args)
            else:
                print('no voice channel found')
        except Exception as error:
            voice_channel = discord.utils.find(lambda c : c.name == channel, ctx.guild.voice_channels)
            if voice_channel is not None:
                self.parse_users(ctx, voice_channel, args)
            else:
                print('no voice channel foundd')
        

    @whitelist.command(name='remove', aliases=['r', 'rm'])
    async def whitelist_remove(self, ctx):
        print('remove')
    
    @commands.command(name='clearwl')
    async def clear_wl(self, ctx):
        pass

    @whitelist.command(name='enable')
    async def whitelist_enable(self, ctx):
        print("Enabling whitelist.")
    
    @whitelist.command(name='disable')
    async def whitelist_disable(self, ctx):
        print("Disabling whitelist.")

    def parse_users(self, ctx, channel, args):
        print(channel)
        mentioned_users = ctx.message.mentions
        user_whitelist = {
            
        }
        for arg in args:
            try:
                print(re.search("\d+", arg).group(0))
            except Exception as error:
                print(error)
                

def setup(bot):
    bot.add_cog(Whitelist(bot))