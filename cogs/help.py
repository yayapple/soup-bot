import discord
from discord.ext import commands

class bothelp(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def help(self, ctx):
		embed = discord.Embed(
			title="help me please", 
			color=discord.Color.gold(),
			description="""
				`name`: gives a sity name

				`names` or `history`: brings up a player's name history. takes the name or uuid of a player as an argument
				__example__: please names nochef

				`render`: renders a player. accepted arguments are `head, face, body, skin, front, head2, body2`. also takes a name or uuid.
				__example__: please render head 67e258a3521b47a9837a8b7e9b416fa6

				`uuid`: takes a minecraft name and returns a uuid

				`joke`: tells a joke

				`eval`: runs a python script

				thats it i think
			"""
		)
		embed.set_footer(text="https://repl.it/@nochef/soup-bot" )

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(bothelp(bot))