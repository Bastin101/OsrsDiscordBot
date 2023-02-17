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
global TaskLines
playerMaster = 631886189493747723


with open("taskList1.txt", 'r') as fp:
    TaskLines = len(fp.readlines())

with open("taskList2.txt", 'r') as fp:
    TaskLines2 = len(fp.readlines())
    
with open("taskList3.txt", 'r') as fp:
    TaskLines3 = len(fp.readlines())

with open("taskList4.txt", 'r') as fp:
    TaskLines4 = len(fp.readlines())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def isPlayerMaster(human):
	return human == playerMaster
	
def playerPosition(author):
	"""Get current player position"""
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "r") as log:
		return log.readline()
		
def playerScore(author):
	"""Get current player score"""
	with open(f"/home/pi/GameMods/GamerScore/{author}", "r") as log:
		return log.readline()
		
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



@bot.command()
async def lvl2(ctx):
	author = ctx.author.id
	author = str(author)
	if ((TaskLines) < int(playerPosition(author))):
		with open(f"/home/pi/GameMods/GamerScore/{author}", "w") as gamerScore:
					gamerScore.write("1")
					with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
						log.write("0")
					await ctx.send("You are now in lvl 2. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl1")
@bot.command()
async def lvl3(ctx):
	author = ctx.author.id
	author = str(author)
	if ((TaskLines2) < int(playerPosition(author))):
		with open(f"/home/pi/GameMods/GamerScore/{author}", "w") as gamerScore:
					gamerScore.write("2")
					with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
						log.write("0")
					await ctx.send("You are now in lvl 3. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl2")


@bot.command()
async def lvl4(ctx):
	author = ctx.author.id
	author = str(author)
	if ((TaskLines3) < int(playerPosition(author))):
		with open(f"/home/pi/GameMods/GamerScore/{author}", "w") as gamerScore:
					gamerScore.write("3")
					with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
						log.write("0")
					await ctx.send("You are now in lvl 4. Good luck nerd")
	else:
		await ctx.send("you have not finished lvl3")


	

@bot.command()
async def dice(ctx):
	"""Dice for player"""
	number = randint(1, 6)
	text = f'**you hit**: {str(number)}'
	author = ctx.author.id
	author = str(author)
	playerPos = playerPosition(author)
	number = str(number + int(playerPos))
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write(number)
		text = text + f"\n Your new position is: {number}"
		if (int(playerScore(author)) == 0):
			with open(r"taskList1.txt", 'r') as tasklist:
				file = tasklist.readlines()
				if((TaskLines+1) > int(number)):
					text = text + f'\n Your new task is: {file[int(number)-1]}'
				else:
					text = "**You finished lvl 1. type !lvl2 to move on**"
		elif (int(playerScore(author)) == 1):
			with open(r"taskList2.txt", 'r') as tasklist:
				file = tasklist.readlines()
				if((TaskLines2+1) > int(number)):
					text = text + f'\n Your new task is: {file[int(number)-1]}'
				else:
					text = text + "**You finished lvl 2. type !lvl3 to move on**"
		else:
			with open(r"taskList3.txt", 'r') as tasklist:
				file = tasklist.readlines()
				if((TaskLines3+1) > int(number)):
					text = text + f'\n Your new task is: {file[int(number)-1]}'
				else:
					text = text + "**You finished lvl 3. type !lvl4 to move on**"
		author = ctx.message.author
		title = "Dicing:"
		embed=discord.Embed(title=title, description=text, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
		await ctx.send(embed=embed)



@bot.command()
async def undice(ctx):
	"""unDice for player"""
	number = randint(-6, -1)
	text = f'**you hit** {str(number)}'
	author = ctx.author.id
	author = str(author)
	playerPos = playerPosition(author)
	number = str(number + int(playerPos))
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write(number)
		text = text + f"\n Your new position is: {number}"
		PlayerScore = int(playerScore(author)) + 1
		with open(f"taskList{PlayerScore}.txt", 'r') as tasklist:
			file = tasklist.readlines()
			text = text + f'\nYour new task is: {file[int(number)-1]}'
	author = ctx.message.author
	title = "Undicing:"
	embed=discord.Embed(title=title, description=text, color=0xFF5733)
	embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
	await ctx.send(embed=embed)


@bot.command()
async def resetme(ctx):
	"""pu player in position 0"""
	author = ctx.author.id
	author = str(author)
	with open(f"/home/pi/GameMods/GamerPosition/{author}", "w") as log:
		log.write("0")
		
@bot.command()
async def setpos(ctx,human:str,pos:str):
	"""owner of game can place player on the field"""
	if ctx.author.id == playerMaster:
		with open(f"/home/pi/GameMods/GamerPosition/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"possition is now: {pos}")
	else:
		await ctx.send("No :)")
		
@bot.command()
async def setscore(ctx,human:str,pos:str):
	"""owner of game can place player lvl"""
	if ctx.author.id == playerMaster:
		with open(f"/home/pi/GameMods/GamerScore/{human}", "w") as log:
			log.write(pos)
			await ctx.send(f"Lvl is now: {pos}")
	else:
		await ctx.send("No :)")
				
	

@bot.command()
async def resetall(ctx):
	if ctx.author.id == playerMaster:
		await ctx.send("Everyone is now on field 0")
	else:
		await ctx.send("No :)")


@bot.command()
async def task(ctx):
	author = ctx.author.id
	author = str(author)
	playerPos = playerPosition(author)
	PlayerScore = int(playerScore(author)) + 1
	with open(f"taskList{PlayerScore}.txt", 'r') as tasklist:
		file = tasklist.readlines()
		text = f'**Field {playerPos}:** Your current is: {file[int(playerPos)-1]}'
		author = ctx.message.author
		title = "Current task:"
		embed=discord.Embed(title=title, description=text, color=0xFF5733)
		embed.set_author(name=ctx.author.display_name, icon_url=author.avatar.url)
		await ctx.send(embed=embed)




	

bot.run(TOKEN)
