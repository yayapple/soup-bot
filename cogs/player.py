# gets player information
from discord.ext import commands
import discord
import requests

class player(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def uuid(self, ctx, name: str):
		r = requests.post('https://api.mojang.com/profiles/minecraft', json = name)
		if r.json() == []:
			await ctx.send(f'couldn\'t find the name {name}.')
		else:
			await ctx.send(r.json()[0].get('id'))

	@commands.command()
	async def render(self, ctx, renderType: str, name: str):
		if len(name) > 20:
			uuid = name
		else:
			r = requests.post('https://api.mojang.com/profiles/minecraft', json = name)
			if r.json() == []:
				await ctx.send(f'couldn\'t find the name {name}.')
			else:
				uuid = r.json()[0].get('id')

		
		if renderType == 'head':
			renderURL = 'https://mc-heads.net/head/'
		elif renderType == 'body':
			renderURL = 'https://mc-heads.net/body/'
		elif renderType == 'skin':
			renderURL = 'https://mc-heads.net/skin/'
		elif renderType == 'face':
			renderURL = 'https://visage.surgeplay.com/face/'
		elif renderType == 'front':
			renderURL = 'https://visage.surgeplay.com/frontfull/'
		elif renderType == 'body2':
			renderURL = 'https://visage.surgeplay.com/full/'
		elif renderType == 'head2':
			renderURL = 'https://visage.surgeplay.com/head/'
		else:
			return await ctx.send('invalid render type')
			
		embed = discord.Embed(
			color = discord.Color.gold()
		)
		embed.set_image(
			url = renderURL + uuid + '.png'
		)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['names', 'history'])
	async def _namehistory(self, ctx, name: str):
		if len(name) > 20:
			uuid = name
		else:
			r = requests.post('https://api.mojang.com/profiles/minecraft', json = name)
			if r.json() == []:
				await ctx.send(f'couldn\'t find name history for {name}.')
			else:
				uuid = r.json()[0].get('id')

				
		r = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')

		# this could be better
		namelist = [entry.get('name') for entry in r.json()]
		namestring = '\n'.join(reversed(['**' + str(index+1) + '** ' + namelist[index] for index in range(len(namelist))]))

		embed = discord.Embed(
			title = namelist[-1] + '\'s name history', 
			color = discord.Color.gold(),
			description = namestring
		)
		embed.set_thumbnail(
			url = 'https://visage.surgeplay.com/face/' + uuid
		)
		embed.set_footer(
			text = 'UUID: ' + uuid,
			)
		await ctx.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('missing required argument: ' + error.param.name)
			

def setup(bot):
	bot.add_cog(player(bot))