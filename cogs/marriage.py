from discord.ext import commands, tasks
import discord
import json
import time

# TODO:
# add consent thru having parties involved react to message
# have it return true or false, then execute the marriage/divorce in the command
# steal it from skipBot


class _marriage(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.messid = {}
		try:
			self.clearActive.start()
		except:
			pass


	async def marry_message(self, ctx, proposer, mentioned, mtype):
		mname = str(await self.bot.fetch_user(mentioned))
		pname = str(await self.bot.fetch_user(proposer))


		if mtype == 'proposer in marriage':
			embed = discord.Embed(
 			  title = f'{mname}, will you join {pname}\'s marriage?',
  			description = 'react ✅ to accept or ❌ to deny.'
			)			
			
		elif mtype == 'mentioned in marriage':
			embed = discord.Embed(
				title = f'{mname}, will you let {pname} into your marriage?',
				description = 'react ✅ to accept or ❌ to deny.'
			)
			
		elif mtype == 'new marriage':
			embed = discord.Embed(
				title = f'{mname}, will you take {pname}\'s hand in marriage?',
				description = 'react ✅ to accept or ❌ to deny.'
			)

		else: return
		
		embed.set_footer(text='exipres in 2m')
		m = await ctx.send(embed=embed)

		for emoji in ['✅', '❌']:
			await m.add_reaction(emoji)
		
		self.messid.update({m.id: {"timestamp": time.time(), "type": mtype, "proposer": proposer, "mentioned": mentioned}})
		print(self.messid)

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		emoji = reaction.emoji

		if user.bot or not message.id in self.messid:
			return

		with open('relationships.json', 'r') as f:
			marriages = json.load(f)
		
		marriageList = marriages['Marriages']
		proposer = self.messid.get(message.id).get('proposer')
		mentioned = self.messid.get(message.id).get('mentioned')
		mtype = self.messid.get(message.id).get('type')
		timestamp = self.messid.get(message.id).get('timestamp')


		if emoji == '✅':

			if mtype == 'new marriage' and user.id == mentioned:
				marriageList.append(
				{
					"Members": [
						proposer, 
						mentioned
					],
					"Timestamp": timestamp
				})
				await message.channel.send(f'<@!{proposer}> and <@!{mentioned}> are now married!')
				
			elif mtype == 'proposer in marriage' and user.id == mentioned:
				x = next((index for (index, d) in enumerate(marriageList) if proposer in d['Members']), None) # look for marriage with proposer

				marriageList[x]['Members'].append(mentioned) # add mentioned to marriage
				memberList = [str(await self.bot.fetch_user(id)) for id in marriageList[x]['Members'] if id not in [proposer, mentioned]]

				await message.channel.send(f'<@!{proposer}> and <@!{mentioned}> are now married, along with {", ".join(memberList)}.')
			
			elif mtype == 'mentioned in marriage' and user.id == mentioned:
				x = next((index for (index, d) in enumerate(marriageList) if mentioned in d['Members']), None) # look for marriage with mentioned

				marriageList[x]['Members'].append(proposer)
				memberList = [str(await self.bot.fetch_user(id)) for id in marriageList[x]['Members'] if id not in [proposer, mentioned]]

				await message.channel.send(f'<@!{proposer}> and <@!{mentioned}> are now married, along with {", ".join(memberList)}.')
			
			elif mtype == 'divorce':
				pass

			else: return

			with open('relationships.json', 'w') as f:
				json.dump(marriages, f, indent=2)
			del self.messid[message.id]
		
		elif emoji == '❌':
			await message.channel.send('lol rejected')
			del self.messid[message.id]



	@commands.command(name='marry')
	async def _marriage(self, ctx):
		

		if len(ctx.message.mentions) != 1:
			return await ctx.send('Who are you marrying?')

		elif ctx.message.mentions[0].id == ctx.message.author.id:
			return await ctx.send('You cant marry yourself.')

		with open('relationships.json', 'r') as f:
			marriages = json.load(f)

		proposer = ctx.message.author.id
		mentioned = ctx.message.mentions[0].id
		marriageList = marriages['Marriages']


		pmarriage = next((item for item in marriageList if proposer in item['Members']), None)
		mmarriage = next((item for item in marriageList if mentioned in item['Members']), None)

		if pmarriage and pmarriage == mmarriage:
			return await ctx.send('You\'re already married.')
		elif pmarriage and mmarriage:
			return await ctx.send('You\'re both in different marriages.')
		elif pmarriage:
			await self.marry_message(ctx, proposer, mentioned, 'proposer in marriage')
		elif mmarriage:
			await self.marry_message(ctx, proposer, mentioned, 'mentioned in marriage')
		else:
			await self.marry_message(ctx, proposer, mentioned, 'new marriage')




	@commands.command(name='divorce')
	async def _divorce(self, ctx):


		if len(ctx.message.mentions) != 1:
			return await ctx.send('Who are you divorcing?')

		elif ctx.message.mentions[0].id == ctx.message.author.id:
			return await ctx.send('You cant divorce Yourself.')


		with open('relationships.json', 'r') as f:
			marriages = json.load(f)

		proposer = ctx.message.author.id
		mentioned = ctx.message.mentions[0].id		
		marriageList = marriages['Marriages']

		pmarriage = next((item for item in marriageList if proposer in item['Members']), None)

		if pmarriage and mentioned in pmarriage.get('Members'):
			if len(pmarriage.get('Members')) == 2:
				marriageList.remove(pmarriage)
				await ctx.send(f'<@!{proposer}> and <@!{mentioned}> are now divorced.')
			else:
				x = next((index for (index, d) in enumerate(marriageList) if proposer in d['Members']), None)
				marriageList[x]['Members'].remove(proposer) # removes proposer from marriage entry
				print(pmarriage.get('Memebers'))
				memberList = [str(await self.bot.fetch_user(id)) for id in pmarriage.get('Members') if id != mentioned]
				print(memberList)
				await ctx.send(f'<@!{proposer}> has left <@!{mentioned}>\'s marriage, leaving them with {", ".join(memberList)}.')


		with open('relationships.json', 'w') as f:
			json.dump(marriages, f, indent=2)

	
	@commands.command(name='marriage')
	async def _checkMarriage(self, ctx):

		if len(ctx.message.mentions) == 0:
			checkid = ctx.message.author.id
		
		elif len(ctx.message.mentions) == 1:
			checkid = ctx.message.mentions[0].id

		elif len(ctx.message.mentions) > 1:
			return await ctx.send('whose marriage am i checking')

		with open('relationships.json', 'r') as f:
			marriages = json.load(f)

		marriageList = marriages['Marriages']

		marriage = next((item for item in marriageList if checkid in item['Members']), None)
		print(marriage)

		if marriage:
			memberList = [str(await self.bot.fetch_user(id)) for id in marriage['Members']]
			embed = discord.Embed(
				title = "Current marriage",
				color = discord.Color.gold()
			)
			embed.add_field(
				name = "Members:",
				value = "\n".join(memberList)
			)
			return await ctx.send(embed=embed)
		else:
			await ctx.send(str(await self.bot.fetch_user(checkid)) + ' is currently unmarried.')


	@tasks.loop(seconds=30)
	async def clearActive(self):
		for x in list(self.messid):
			if time.time() - self.messid[x] > 120:
				self.messid.pop(x)


def setup(bot):
	bot.add_cog(_marriage(bot))