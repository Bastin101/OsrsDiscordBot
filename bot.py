

import discord
from discord.ext import commands
import asyncio
import logging
from datetime import datetime

import rng
import os.path

import matplotlib.pyplot as plt


# Settings

with open("token.txt", 'r') as fp:
    gTOKEN = fp.readline().strip()

gFilePath = "/home/liet/bastin/bot/OsrsDiscordBot/gamefiles"
gPrefix = "¬"


# Bot

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''Discord osrs bot'''
bot = commands.Bot(intents=intents, command_prefix=gPrefix , description='The Best Bot For the Best User!',  case_insensitive=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping(ctx: discord.ext.commands.Context):
	""" testing """
	author = str(ctx.author.id)
	logging.info(f"ping() from '{author}'")

	await ctx.send("pong") 
    
      
@bot.command()
async def join(ctx):
	"""Join the game!"""
	author = str(ctx.author.id)

	try:
		rng.join(author)
	except rng.AlreadyInGameError:
		await ctx.send("You are already in the game")
	else:
		await ctx.send("You are now in the game")


@bot.command()
async def levelup(ctx: discord.ext.commands.Context):
	"""Attempt to level up"""
	author = str(ctx.author.id)

	try:
		pos = rng.levelUp(author)
	except rng.CantLevelUpError:
		await ctx.send("You haven't finished your current level yet!")
	except rng.NotInGameError:
		await ctx.send("You're not in the game")
	else:
		if pos[0] == -2:
			await ctx.send(f"YOU'VE COMPLETED THE GAME YOU FUCKING NERD")
		else:
			await ctx.send(f"You are now in level {pos[0]+1}. Good luck nerd")
	

@bot.command()
async def dice(ctx: discord.ext.commands.Context):
	"""Dice for player"""
	author = str(ctx.author.id)

	try:
		roll,pos = rng.dice(author)
	except rng.NotInGameError:
		await ctx.send("You're not in the game")
	except rng.ShouldLevelUpError:
		await ctx.send(f"You've already completed the level! Try {gPrefix}levelup")
	else:
		message = f'**you hit**: {str(roll)}'
		if pos[1] < 0:
			message += f"\nType `{gPrefix}levelup` to advance to the next level"
		else:
			task = rng.task(pos)
			message += f"\nYou are now at: {pos[1]} (level {pos[0]+1})"
			message += f"\nYour new task is: {task}"

		title = "Dicing:"
		embed=discord.Embed(title=title, description=message, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
		await ctx.send(embed=embed)


@bot.command()
async def undice(ctx: discord.ext.commands.Context):
	"""unDice for player"""
	author = str(ctx.author.id)

	try:
		roll,pos = rng.undice(author)
	except rng.NotInGameError:
		await ctx.send("You're not in the game")
	except rng.ShouldLevelUpError:
		await ctx.send(f"You've already completed the level! Try {gPrefix}levelup")
	except rng.NoUndiceError:
		await ctx.send("No undicing on step 1! Do your task.")
	except rng.ShouldDiceError:
		await ctx.send(f"You've not started the level yet! Roll {gPrefix}dice.")
	else:
		message = f'**you hit**: {str(roll)}'
		if pos[1] < 0:
			message += f"\nType `{gPrefix}levelup` to advance to the next level"
		else:
			task = rng.task(pos)
			message += f"\nYou are now at: {pos[1]} (level {pos[0]+1})"
			message += f"\nYour new task is: {task}"

		title = "Undicing:"
		embed=discord.Embed(title=title, description=message, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
		await ctx.send(embed=embed)


@bot.command()
async def task(ctx: discord.ext.commands.Context):
	author = str(ctx.author.id)
	logging.info(f"task('{author}')")

	try:
		pos = rng.getPos(author)
		task = rng.task(pos)
	except rng.NotInGameError:
		await ctx.send("You're not in the game")
	except rng.ShouldLevelUpError:
		await ctx.send(f"You've completed the level! Try {gPrefix}levelup")
	except rng.ShouldDiceError:
		await ctx.send(f"You've not started the level yet! Roll {gPrefix}dice.")
	except rng.CompletedGameError:
		await ctx.send("You've completed the game!.")
	else:
		text = f"You are at: {pos[1]} (level {pos[0]+1})"
		text += f"\nYour current task is {task}"

		title = "Current task:"
		embed=discord.Embed(title=title, description=text, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
		await ctx.send(embed=embed)


def getUserId(ctx: discord.ext.commands.Context, human:str):
	if human.startswith("<@"):
		return int(human.removeprefix("<@").removesuffix(">"))
	else:
		user = discord.utils.get(ctx.guild.members, name=human)
		if user is not None:
			return user.id

	return None

def getUserName(human:int):
	gamer_id = bot.get_user(human)
	return str(gamer_id)[:-5]


@bot.command()
async def reset(ctx: discord.ext.commands.Context, human:str):
	"""owner of game can reset a player on the field"""
	user = getUserId(ctx, human)

	if discord.utils.get(ctx.author.roles, name="Game Owner") is not None:
		if user is not None:
			try:
				rng.reset(user)
			except rng.NotInGameError:
				await ctx.send("They're not in the game")
			else:
				name = getUserName(user)
				await ctx.send(f"{name} is now at position {p[1]} (level {p[0]+1})")
		else:
			await ctx.send("Who?")
	else:
		await ctx.send("No :)")

@bot.command()
async def set(ctx: discord.ext.commands.Context, human:str, lvl:str, pos:str):
	"""owner of game can reset a player on the field"""

	user = getUserId(ctx, human)

	if discord.utils.get(ctx.author.roles, name="Game Owner") is not None:
		if user is not None:
			try:
				p = rng.setPos(user, (int(lvl)-1, int(pos)))
			except rng.NotInGameError:
				await ctx.send("They're not in the game")
			except rng.BadPositionError:
				await ctx.send("That's not a valid position soz")
			else:
				name = getUserName(user)
				await ctx.send(f"{name} is now at position {p[1]} (level {p[0]+1})")
		else:
			await ctx.send("Who?")
	else:
		await ctx.send("No :)")


@bot.command()
async def score(ctx: discord.ext.commands.Context):
	"""print all player names and score"""
	gamers = rng.getAllPositions()

	results = []
	for g in gamers.items():
		name = getUserName(int(g[0]))
		score = rng.score(g[1])
		results.append((name,score))

	"""sort based on positions"""
	results = sorted(results, key=lambda pair: pair[1], reverse=True)

	title = "Highscore:"
	text = ""
	for pair in results:
		text = text + f"{pair[0]}: {pair[1]} \n"
		
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	await ctx.send(embed=embed)


@bot.command()
async def graph(ctx: discord.ext.commands.Context):
	gamers = rng.listGamers()

	data = []
	order = []

	startdate = datetime.now()

	for gamer in gamers:
		hst = rng.getHistory(gamer)
		score = hst[-1]

		if hst[0][0] < startdate:
			startdate = hst[0][0]

		last = True
		for i in range(0,len(data)):
			if score[1] > data[order[i]][-1][1]:
				order.insert(i, len(data))
				last = False
				break
		if last:
			order.append(len(data))

		data.append(hst)

	plt.style.use('dark_background')
	fig, ax = plt.subplots()

	n = 1
	for o in order:
		gamer = getUserName(int(gamers[o]))
		sco = data[o][-1][1]

		ax.plot([((d[0] - startdate).total_seconds() / 60 / 60) for d in data[o]], [d[1] for d in data[o]], label = f"{n}. {gamer} ({sco})")

		n = n+1

	plt.legend()
	plt.tight_layout()
	plt.gcf().set_size_inches(12, 8)
	plt.savefig('history.png', dpi=200)

	await ctx.send(file=discord.File("history.png"))



logging.basicConfig(level=logging.INFO)
rng.init(gFilePath)
bot.run(gTOKEN)
