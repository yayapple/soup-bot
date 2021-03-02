# club penguin jokes

import discord
from discord.ext import commands
from random import choice
import json

class jokes(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		with open('jokes.json', 'r') as f:
			self.jokelist = json.load(f)
	
	@commands.command(name='tell', aliases=['joke'])
	async def _joke(self, ctx, *args):
		if not 'joke' in args and not len(args) == 0:
			return

		category = choice(list(self.jokelist.keys()))
		joke = choice(self.jokelist.get(category))
	
		embed = discord.Embed(
			description=joke,
			color=discord.Color.gold()
		)

		embed.set_footer(
			text=category
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(jokes(bot))