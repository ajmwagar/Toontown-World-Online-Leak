from panda3d.core import *
from direct.distributed.ClockDelta import *
import math
import random
from pandac.PandaModules import Point3
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
from toontown.suit import SuitTimings
from toontown.suit import SuitDNA
from toontown.toonbase import TTLocalizer
from toontown.suit.SuitLegList import *
TIME_BUFFER_PER_WPT = 0.25
TIME_DIVISOR = 100
DISTRIBUTE_TASK_CREATION = 0

class cogfunctions:
	notify = DirectNotifyGlobal.directNotify.newCategory('cogfunctions')

	def __init__(self):
		self.dna = None
		self.level = 0
		self.maxHP = 0
		self.currHP = 0
		self.isSkelecog = 0
		self.legList = None
		self.path = None
		self.suitGraph = None
		return
	def delete(self):
		if self.legList is not None:
			del self.legList
		# I have no idea if this will fix anything... but it looks like it isn't
		# deleted, so w/e.
		if self.path is not None:
			del self.path
		if self.suitGraph is not None:
			del self.suitGraph

	def getStyleName(self):
		if hasattr(self, 'dna') and self.dna:

			return self.dna.name
		else:
			self.notify.error('called getStyleName() before dna was set!')
			return 'unknown'

	def getStyleDept(self):
		if hasattr(self, 'dna') and self.dna:
			return SuitDNA.getDeptFullname(self.dna.dept)
		else:
			self.notify.error('called getStyleDept() before dna was set!')
			return 'unknown'

	def getLevel(self):
		return self.level

	def setLevel(self, level):
		self.level = level
		nameWLevel = TTLocalizer.SuitBaseNameWithLevel % {'name': self.name,
		 'dept': self.getStyleDept(),
		 'level': self.getActualLevel()}
		self.setDisplayName(nameWLevel)
		attributes = SuitBattleGlobals.SuitAttributes[self.dna.name]
		if len(attributes['hp'])<=self.level:
			print "maxHP is less then level, Oops!"
			raise Exception("invalid list index: len(attributes['hp') = %d, self.level=%d" % (len(attributes['hp']), self.level))
# if we made it this far, we are good  
		self.maxHP = attributes['hp'][self.level]

		#self.maxHP = attributes['hp'][self.level]
		self.currHP = self.maxHP

	def getSkelecog(self):
		return self.isSkelecog

	def setSkelecog(self, flag):
		self.isSkelecog = flag

	def getActualLevel(self):
		if hasattr(self, 'dna'):
			return SuitBattleGlobals.getActualFromRelativeLevel(self.getStyleName(), self.level) + 1
		else:
			self.notify.warning('called getActualLevel with no DNA, returning 1 for level')
			return 1

	def setPath(self, suitGraph, path):
		self.suitGraph = suitGraph
		self.path = path

	def getPath(self):
		return self.path

	def printPath(self):
		print '%d points in path' % len(self.path)
		for currPathPt in self.path:
			print '\t', currPathPt

	def makeLegList(self):
		self.legList = SuitLegList(self.suitGraph, self.path)
