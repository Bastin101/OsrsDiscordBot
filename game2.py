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
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "r") as log:
		return log.readline()

def set_player_position(author: str, new_position: int):
	"""Sets the player's current position"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as f:
		f.write(str(new_position))

def set_player_lvl(author: str, new_lvl: int):
	with open(f"/home/pi/GameMods/GamerScore/{author}", "w") as f:
		f.write(str(new_lvl))
		
def player_score(author: str):
	"""Get current player score"""
	with open(f"/home/pi/GameMods/GamerScore/{author}", "r") as log:
		return log.readline()

def get_task(author: str, level: int, position: int) -> str:
	"""Generates a new task for a player, or tells them to advance to the next level
	Returns a message suitable for the bot to respond with"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write(position)
		text = text + f"\n Your new position is: {number}"
		with open(task_files[level], 'r') as tasklist:
			file = tasklist.readlines()
			if((level_lengths[level]) > int(position)):
				text = text + f'\n Your new task is: {file[int(position)-1]}'
			else:
				text = f"**You finished lvl{level}. type !lvl{current_level + 1} to move on**"
	return text
		
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
async def ping(ctx):
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
async def score(ctx):
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
			with open(f"/home/pi/GameMods/GamerPosition/{int(row[:-1])}", "r") as gamerPos:
				with open(f"/home/pi/GameMods/GamerScore/{int(row[:-1])}", "r") as gamerScore:
					score2 = int(gamerScore.readline())
					pos2 = int(gamerPos.readline())
					finalscore = pos2 + (score2*TaskLines2)
					positions.append(finalscore)
	"""sort based on positions"""
	players_and_positions_sorted = sorted(zip(gamers, positions), key=lambda pair: pair[1], reverse=True)
	
	title = "Highscore:"
	text = ""
	for pair in players_and_positions_sorted:
		text = text + f"{pair[0]}: {pair[1]} \n"
		
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	await ctx.send(embed=embed)

async def move_player_to_next_lvl(author, current_lvl):
	if ((TaskLines) < int(get_player_position(author))):
		set_player_lvl(author, 2)
		set_player_position(author, 0)
		await ctx.send("You are now in lvl 2. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl1")

@bot.command()
async def lvl2(ctx):
	author = ctx.author.id
	author = str(author)


@bot.command()
async def lvl3(ctx):
	author = ctx.author.id
	author = str(author)
	if ((TaskLines2) < int(get_player_position(author))):
		set_player_lvl(author, 3)
		set_player_position(author, 0)
		await ctx.send("You are now in lvl 3. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl2")


@bot.command()
async def lvl4(ctx):
	author = ctx.author.id
	author = str(author)
	if ((TaskLines3) < int(get_player_position(author))):
		set_player_lvl(author, 4)
		set_player_position(author, 0)
		await ctx.send("You are now in lvl 4. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl3")


	

@bot.command()
async def dice(ctx):
	"""Dice for player"""
	roll = randint(1, 6)
	text = f'**you hit**: {str(roll)}'
	author = str(ctx.author.id)
	current_position = get_player_position(author)
	position = str(roll + int(current_position))
	message = get_task(author, level, position)
	title = "Dicing:"
	embed=discord.Embed(title=title, description=message, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)



@bot.command()
async def undice(ctx):
	"""unDice for player"""
	roll = randint(-6, -1)
	text = f'**you hit**: {str(roll)}'
	author = str(ctx.author.id)
	current_position = get_player_position(author)
	position = str(roll + int(current_position))
	message = get_task(author, level, position)
	title = "Undicing:"
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)


@bot.command()
async def resetme(ctx):
	"""put player in position 0"""
	author = ctx.author.id
	author = str(author)
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write("0")
		
@bot.command()
async def setpos(ctx,human:str,pos:str):
	"""owner of game can place player on the field"""
	if ctx.author.id == player_master:
		with open(f"/home/pi/GameMods/GamerPosition/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"possition is now: {pos}")
	else:
		await ctx.send("No :)")
		
@bot.command()
async def setscore(ctx,human:str,pos:str):
	"""owner of game can place player lvl"""
	if ctx.author.id == player_master:
		with open(f"/home/pi/GameMods/GamerScore/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"Lvl is now: {pos}")
	else:
		await ctx.send("No :)")
				
	

@bot.command()
async def resetall(ctx):
	if ctx.author.id == player_master:
		await ctx.send("Everyone is now on field 0")
	else:
		await ctx.send("No :)")


@bot.command()
async def task(ctx):
	author = str(ctx.author.id)
	player_pos = get_player_position(author)
	current_level = int(player_score(author)) + 1
	with open(task_files[current_level], 'r') as tasklist:
		file = tasklist.readlines()
		text = f'**Field {player_pos}:** Your current is: {file[int(player_pos)-1]}'
		author = ctx.message.author
		title = "Current task:"
		embed=discord.Embed(title=title, description=text, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
		await ctx.send(embed=embed)




	

bot.run(TOKEN)
