from discord.ext import commands
from random import choice

class names(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open('names.txt', 'r') as s:
			self.names = s.readlines()

	@commands.command()
	async def name(self, ctx):
		name = choice(self.names).rstrip('\n')
		if name[-1] in tuple('aiou'):
			sityName = name + choice(tuple('bcfgjklmnprsvz')) + 'ity'
		elif name[-1] == 'e':
			sityName = name[:-1] + 'ity'
		else:
			sityName = name + 'ity'
		await ctx.send(sityName)

def setup(bot):
	bot.add_cog(names(bot))
