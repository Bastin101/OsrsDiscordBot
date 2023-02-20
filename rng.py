

from random import randint
import os, os.path
import logging
from datetime import datetime


gFILEBASE = ""


class NotInGameError(Exception):
	pass

class AlreadyInGameError(Exception):
	pass

class ShouldLevelUpError(Exception):
	pass

class CantLevelUpError(Exception):
	pass

class ShouldDiceError(Exception):
	pass

class NoUndiceError(Exception):
	pass

class CompletedGameError(Exception):
	pass


class BadPositionError(Exception):
	def __init__(self, position):
		self.position = position




class Tasks:
	tasks = []
	levels = []

	@staticmethod
	def loadFiles(path):
		logging.debug("Loading Task Files")
		levelStart = 0
		files = os.listdir(path)
		files.sort()

		for file_name in files:
			with open(os.path.join(path, file_name), 'r') as fp:
				d = fp.readlines()
				Tasks.tasks.append(d)
				Tasks.levels.append(len(d))
				logging.debug(f"Loaded '{file_name}' with {len(d)} tasks")

	@staticmethod
	def isValid(position):
		return (len(position) == 2) \
				and (position[0] >= 0) \
				and (position[0] < len(Tasks.levels)) \
				and (position[1] >= 0) \
				and (position[1] <= Tasks.levels[position[0]])

	@staticmethod
	def get(position):
		return Tasks.tasks[position[0]][position[1]-1]

	@staticmethod
	def add(position, n):
		lvl,step = position
		step = step + n
		if step > Tasks.levels[lvl]:
			# level up
			step = -1

		return (lvl, step)

	@staticmethod
	def subtract(position, n):
		lvl,step = position 
		step = step - n
		if step < 1: 
			step = 1

		return (lvl,step)

	@staticmethod
	def score(position):
		lvl,step = position
		if lvl == -1:
			return 0
		if lvl == -2:
			return sum(Tasks.levels)

		if step < 0:
			step = 0
			lvl += 1

		ret = step
		for i in range(0,lvl):
			ret += Tasks.levels[i]

		return ret


class History:
	@staticmethod
	def record(player, position):
		dt = datetime.now().strftime("%Y%m%dT%H%M")
		score = Tasks.score(position)
		with open(os.path.join(gFILEBASE, "history", player), "a") as f:
			f.write(f"{dt},{score}\n")

class Files:
	@staticmethod
	def loadPlayer(player):
		retPos = (-1, 0)
		try:
			with open(os.path.join(gFILEBASE, "gamers", player), "r") as f:
				posString = f.read().strip().split(",")
				retPos = (int(posString[0]), int(posString[1]))
		except:
			pass

		logging.debug(f"loadPlayer({player}) = {retPos}")

		return retPos

	@staticmethod
	def updatePlayer(player, position):
		logging.debug(f"updatePlayer({player}, {position})")
		with open(os.path.join(gFILEBASE, "gamers", player), "w") as f:
			f.write(f"{position[0]},{position[1]}")

class Game:
	@staticmethod
	def roll():
		return randint(1, 6)

	@staticmethod
	def movePlayer(player, newPos):
		Files.updatePlayer(str(player), newPos)
		History.record(str(player), newPos)





def join(player):
	pos = Files.loadPlayer(player)
	if pos[0] >= 0:
		raise AlreadyInGameError(player)

	Files.updatePlayer(player, (0,0))
	History.record(player, (0,0))

	return True

def dice(player):
	pos = Files.loadPlayer(str(player))

	if pos[0] < 0:
		raise NotInGameError()

	if pos[1] < 0:
		raise ShouldLevelUpError()

	r = Game.roll()
	newPos = Tasks.add(pos, r)

	Game.movePlayer(player, newPos)
	return (r, newPos)

def undice(player):
	lvl,step = Files.loadPlayer(player)

	if lvl < 0:
		raise NotInGameError()

	if step < 0:
		raise ShouldLevelUpError()

	if step == 0:
		raise ShouldDiceError()

	if step == 1:
		raise NoUndiceError()

	r = Game.roll()
	newPos = Tasks.subtract((lvl,step), r)

	Game.movePlayer(player, newPos)
	return (r, newPos)

def levelUp(player):
	lvl,step = getPos(player)

	if step != -1:
		raise CantLevelUpError()

	lvl = lvl+1
	step = 0

	if lvl >= len(Tasks.levels):
		lvl = -2

	Game.movePlayer(player, (lvl,step))

	return (lvl,step)

def setPos(player, pos):
	if not Tasks.isValid(pos):
		raise BadPositionError(pos)

	current = Files.loadPlayer(str(player))

	if current[0] < 0:
		raise NotInGameError()

	Game.movePlayer(player, pos)
	return pos


def getPos(player):
	pos = Files.loadPlayer(str(player))

	if pos[0] == -1:
		raise NotInGameError()

	return pos


def inGame(player):
	pos = Files.loadPlayer(player)
	return pos[0] >= 0

def reset(player):
	return setPos(player, (0,0))

def task(pos):
	if pos[0] == -1:
		raise NotInGameError()

	if pos[0] == -2:
		raise CompletedGameError()

	if pos[1] == -1:
		raise ShouldLevelUpError()

	if pos[1] == 0:
		raise ShouldDiceError()

	if not Tasks.isValid(pos):
		raise BadPositionError(pos)

	return Tasks.get(pos)

def getAllPositions():
	files = os.listdir(os.path.join(gFILEBASE, "gamers"))

	gamers = {}
	for g in files:
		gamers[g] = getPos(g)

	return gamers

def score(position):
	return Tasks.score(position)



def init(path):
	logging.info(f"Initialising RNG in '{path}'")

	global gFILEBASE
	gFILEBASE = path 

	Tasks.loadFiles(os.path.join(path, "tasks"))
