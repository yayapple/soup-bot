from discord.ext import commands

class say(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def say(self, ctx, id: int, *words: str):
		try:
			channel = self.bot.get_channel(id)
			await channel.send(' '.join(words))
		except Exception as e:
			await ctx.send(e)
	

def setup(bot):
	bot.add_cog(say(bot))