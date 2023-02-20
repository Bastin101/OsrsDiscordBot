
import discord
from discord.ext import commands
import asyncio
import logging

import rng
import os.path


# Settings

with open("Token.txt", 'r') as fp:
    gTOKEN = fp.readline()

gFilePath = "S:\\pers\\bastin\\rng\\new\\gamefiles"
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
			message += f"\nYour new task is: {task}"

		title = "Dicing:"
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
		text = f"Your current task is {task}"

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

	"""sort based on positions"""

	title = "Highscore:"
	text = ""
	for pair in gamers.items():
		name = getUserName(int(pair[0]))
		score = rng.score(pair[1])
		text = text + f"{name}: {score} \n"
		
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	await ctx.send(embed=embed)
	

logging.basicConfig(level=logging.DEBUG)
rng.init(gFilePath)
bot.run(gTOKEN)
