import discord
from discord.ext import commands
import asyncio
from random import *
import csv
from itertools import islice
import os


with open("Token.txt", 'r') as fp:
    TOKEN = fp.readline()



description = '''Discord osrs bot'''
bot = commands.Bot(intents=discord.Intents.all() , command_prefix= "!" , description='The Best Bot For the Best User!',  case_insensitive=True)

player_master = 631886189493747723

level_lengths = {}
task_files = ["taskList1.txt", "taskList2.txt", "taskList3.txt", "taskList4.txt"]

for i, file_name in enumerate(task_files, start=1):
	with open(file_name, 'r') as fp:
		level_lengths[i] = len(fp.readlines())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def is_player_master(human):
	return human == player_master
	
def get_player_position(author: str) -> str:  
	"""Get current player position"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "r") as f:
		return f.readline()

def set_player_position(author: str, new_position: int):
	"""Sets the player's current position"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as f:
		f.write(str(new_position))

def get_player_level(author: str) -> str:
	"""Gets the current level a player is at"""
	with open(f"/home/pi/GameMods/GamerScore/{author}", "r") as f:
		return f.readline()

def set_player_level(author: str, new_lvl: int):
	with open(f"/home/pi/GameMods/GamerScore/{author}", "w") as f:
		f.write(str(new_lvl))
		
def get_task(author: str, level: int, position: int) -> str:
	"""Generates a new task for a player, or tells them to advance to the next level
	Returns a message suitable for the bot to respond with"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write(position)
		with open(task_files[level], 'r') as tasklist:
			file = tasklist.readlines()
			if((level_lengths[level]) > int(position)):
				return file[int(position)-1]
	return "invalid player position"
		
"""		
@bot.command()
async def embed(ctx):
	author = ctx.message.author
	text = "this is text test \n line 2?"
	title = "this is title test"
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)
"""
	




@bot.command()
async def ping(ctx: discord.ext.commands.Context):
    """ testing """
    await ctx.send("pong") 
    
    
"""    
@bot.command()
async def Join(ctx):
	with open("gamers.csv", "r") as log:
		author = ctx.author.id
		author = str(author)
		ingameCheck = 0
		read_obj = csv.reader(log)
		for row in log:
			if ((author +"\n") == row):
				ingameCheck = ingameCheck + 1
		if(ingameCheck>0):
			await ctx.send("You are already in the game")
		else:
			with open("gamers.csv", "a") as log:
				log.write(author + "\n")
				with open(f"/home/pi/GameMods/GamerPosition/{author}", "x") as gamerPos:
					gamerPos.write("0")
				with open(f"/home/pi/GameMods/GamerScore/{author}", "x") as gamerScore:
					gamerScore.write("0")
	
				await ctx.send("You are now in the game")

"""

@bot.command()
async def score(ctx: discord.ext.commands.Context):
	"""print all player names and score"""
	gamers = []
	positions = []
	"""read usernames"""
	with open("gamers.csv", "r") as file_obj:
		reader_obj = file_obj.readlines()
		for row in reader_obj:
			gamer_id = bot.get_user(int(row))
			gamers.append(str(gamer_id)[:-5])
			"""read positions"""
			with open(f"/home/pi/GameMods/GamerPosition/{int(row[:-1])}", "r") as gamer_positions:
				with open(f"/home/pi/GameMods/GamerScore/{int(row[:-1])}", "r") as gamer_levels:
					level = int(gamer_levels.readline())
					position = int(gamer_positions.readline())
					for i in range(level):
						final_score += level_lengths[i]
					final_score += position
					positions.append(final_score)
	"""sort based on positions"""
	players_and_positions_sorted = sorted(zip(gamers, positions), key=lambda pair: pair[1], reverse=True)
	
	title = "Highscore:"
	text = ""
	for pair in players_and_positions_sorted:
		text = text + f"{pair[0]}: {pair[1]} \n"
		
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	await ctx.send(embed=embed)

async def move_player_to_next_lvl(author: str, current_lvl: int):
	if ((TaskLines) < int(get_player_position(author))):
		set_player_level(author, current_lvl + 1)
		set_player_position(author, 0)
		await ctx.send(f"You are now in lvl {current_lvl + 1}. Good luck nerd")
	else:
		await ctx.send(f"you have not finished lvl {current_lvl}.")

@bot.command()
async def lvl2(ctx: discord.ext.commands.Context):
	author = str(ctx.author.id)
	move_player_to_next_lvl(author, 2)

@bot.command()
async def lvl3(ctx: discord.ext.commands.Context):
	author = str(ctx.author.id)
	move_player_to_next_lvl(author, 3)

@bot.command()
async def lvl4(ctx: discord.ext.commands.Context):
	author = str(ctx.author.id)
	move_player_to_next_lvl(author, 4)

	

@bot.command()
async def dice(ctx: discord.ext.commands.Context):
	"""Dice for player"""
	roll = randint(1, 6)
	message = f'**you hit**: {str(roll)}'
	author = str(ctx.author.id)
	current_position = get_player_position(author)
	position = str(roll + int(current_position))
	level = get_player_level(author)
	if position > level_lengths[level]:
		message += f"\nType `!lvl{int(level) + 1}` to advance to the next level"
	else:
		task = get_task(author, level, position)
		message += f"Your new task is: {task}"
	title = "Dicing:"
	embed=discord.Embed(title=title, description=message, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)



@bot.command()
async def undice(ctx: discord.ext.commands.Context):
	"""unDice for player"""
	roll = randint(-6, -1)
	text = f'**you hit**: {str(roll)}'
	author = str(ctx.author.id)
	current_position = get_player_position(author)
	if current_position == 0:
		await ctx.send(f"You can't undice at position 1. Do your task instead :)")
		return
	position = str(roll + int(current_position))
	if position < 0:
		position = 0
	task = get_task(author, level, position)
	message = f"Your new task is {task}"
	title = "Undicing:"
	embed=discord.Embed(title=title, description=message, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)


@bot.command()
async def resetme(ctx: discord.ext.commands.Context):
	"""put player in position 0"""
	author = ctx.author.id
	author = str(author)
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write("0")
		
@bot.command()
async def setpos(ctx: discord.ext.commands.Context, human: str, pos: str):
	"""owner of game can place player on the field"""
	if ctx.author.id == player_master:
		with open(f"/home/pi/GameMods/GamerPosition/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"Position is now: {pos}")
	else:
		await ctx.send("No :)")
		
@bot.command()
async def setscore(ctx: discord.ext.commands.Context, human: str, pos: str):
	"""owner of game can place player lvl"""
	if ctx.author.id == player_master:
		with open(f"/home/pi/GameMods/GamerScore/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"Lvl is now: {pos}")
	else:
		await ctx.send("No :)")
				
	

@bot.command()
async def resetall(ctx: discord.ext.commands.Context):
	if ctx.author.id == player_master:
		await ctx.send("Everyone is now on field 0")
	else:
		await ctx.send("No :)")


@bot.command()
async def task(ctx: discord.ext.commands.Context):
	author = str(ctx.author.id)
	level = int(get_player_level(author))
	position = get_player_position(author)
	task = get_task(author, level, position)
	text = f"Your current task is {task}"
	title = "Current task:"
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)




	

bot.run(TOKEN)
