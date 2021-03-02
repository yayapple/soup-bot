#this code sux i put it together in like an hour dont @ me

from discord.ext import commands
import os
from keep_alive import keep_alive


def get_prefixes(bot, message):
  prefixes = ['please ', 'when you ', '>']
  return commands.when_mentioned_or(*prefixes)(bot,message)

bot = commands.Bot(command_prefix=get_prefixes)
bot.remove_command('help')


@bot.command(aliases=['l'])
async def load(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		try:
			bot.load_extension(f'cogs.{extension}')
			await ctx.send(f'loaded {extension}')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

@bot.command(aliases=['ul', 'u'])
async def unload(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f'unloaded {extension}')

@bot.command(aliases=['rl', 'r'])
async def reload(ctx, extension):
	if not ctx.author.id == 290983149507182592:
		return
	else:
		try:
			bot.unload_extension(f'cogs.{extension}')
			bot.load_extension(f'cogs.{extension}')
			await ctx.send(f'reloaded {extension}')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in ['import.py']:
		bot.load_extension(f'cogs.{filename[:-3]}')

# in case i fuck up

@bot.command()
async def purge(ctx, amount):
	if ctx.author.id != 290983149507182592:
		return await ctx.send('no')
	if not amount.isdigit():
		return await ctx.send('thats not a number')
	amount = int(amount)
	await ctx.channel.purge(limit=amount+1)
	await ctx.send(f'purged {amount} messages')

@bot.event
async def on_ready():
	print('\n' + bot.user.name + ' online')
	print(bot.user.id)
	print('---------------')


keep_alive()
bot.run(os.environ.get('TOKEN')) 