from discord.ext import commands
import discord


def isCreator(ctx: commands.Context):
    return ctx.message.author.id == "114796980739244032"

async def isCreatorAsync(ctx: commands.Context):
    return ctx.message.author.id == "114796980739244032"
    


class Aksu(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.check(isCreator)
    async def reload(self):
        """Reload all the cogs"""
        reloadMessage = "Reloading cogs:```css\n"
        failedOne = False

        for cog in self.client.allCogs:
            try:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                reloadMessage += f"{cog[4:]} - success\n"
            except Exception as err:
                failedOne = True
                reloadMessage += f"{cog[4:]} - failed\n"
                print(f"[reload] Failed to reload cog \"{cog}\" [{type(err).__name__}: {err}]")
        
        reloadMessage += "```"
        reloadMessage += "**Something's wrong!**" if failedOne == True else ""
        await self.client.say(reloadMessage)

    @commands.command()
    @commands.check(isCreator)
    async def die(self):
        """Kill the bot"""
        await self.client.say("Time for me to die :<")
        exit()

    @commands.command(pass_context=True, brief="[\"playing\"/\"streaming\"/\"listening\"/\"watching\"] [what]")
    @commands.check(isCreator)
    async def status(self, ctx: commands.Context, mode: str, *, what: str):
        """Change my status"""
        mode = ["playing", "streaming", "listening", "watching"].index(mode)
        game = discord.Game(name=what, url="https://www.twitch.tv/Helmerz", type=mode)
        await self.client.change_presence(game=game)
        await self.client.add_reaction(ctx.message, '\U00002714') # React with a black checkmark

    @status.error
    async def status_eh(self, err: Exception, ctx: commands.Context):
        if isinstance(err, commands.MissingRequiredArgument):
            await self.client.say(f"{ctx.message.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await self.client.say(f"{ctx.message.author.mention} what the fuck is that mode?")

    @commands.command(brief="[channel/user ID] [message]")
    @commands.check(isCreator)
    async def messageTo(self, target: str, *, msg: str):
        """Send a custom message to any channel or user"""
        channel = self.client.get_channel(target)
        if channel == None:
            channel = await self.client.get_user_info(target)
        await self.client.send_message(channel, msg)

    @messageTo.error
    async def messageTo_eh(self, err: Exception, ctx: commands.Context):
        if isinstance(err, commands.MissingRequiredArgument):
            await self.client.say(f"{ctx.message.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await self.client.say(f"{ctx.message.author.mention} invalid channel/user ID... Baka...")


def setup(client: commands.Bot):
    client.add_cog(Aksu(client))