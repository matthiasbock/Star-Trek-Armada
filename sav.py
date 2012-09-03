#!/usr/bin/python

from utils import *

LENGTH_PLAYER		= 202
LENGTH_GAMESETUP	= 584
LENGTH_NEBULA		= 827
LENGTH_TURRET		= 843
LENGTH_FERENGIMARAUDER	= 1683
LENGTH_DIRECTIONALLIGHT	= 863
LENGTH_BLACKHOLE	= 827
LENGTH_PLANET		= 827
LENGTH_MOON		= 827

class Player:
	def __init__(self, binary, debug=False):
		self.debug = debug

		assert binary[0:4] == '\x00\x00\x00\x01'

		self.name = binary[175:175+16].replace('\x00', '')	# 16 bytes
		if self.debug:
			print self.name

class Nebula:
	def __init__(self, binary, debug=False):
		self.debug = debug

		self.type = binary[54:70]
		self.name = binary[114:130]
		self.title = binary[334:370]

		if self.debug:
			print 'nebula type = '+self.type
			print 'nebula name = '+self.name
			print 'nebula title = '+self.title

class SAV:
	def __init__(self, filename=None, debug=False):

		self.debug = debug

		self.version		= 'version [1] =\x0d\x0a2053\x0d\x0asaveGameDesc = '
		self.saveGameDesc	= ''
		self.binary		= '\x0d\x0abinarySave [1] =\x0d\x0atrue\x0d\x0a'
		self.untitled_bzn	= '\x02\xdd\x60\x00\x10\x00\x00\x00untitled.bzn'

		if filename is not None:
			self.open(filename)

	def open(self, filename):
		self.f = open(filename)

		# 0x0000 - 0x0023: version[1] = 2053

		assert self.f.read(len(self.version)) == self.version

		# 0x0024 - 0x0123: saveGameDesc

		d = self.f.read(256)
		self.saveGameDesc = ''.join([chr(int(d[i*2]+d[i*2+1], 16)) for i in range(128)]).strip()

		if self.debug:
			print self.saveGameDesc

		# 0x0124 - 0x013D: binarySave[1] = true

		assert self.f.read(len(self.binary)) == self.binary

		# 0x013E - 0x0151: untitled.bzn

		assert self.f.read(len(self.untitled_bzn)) == self.untitled_bzn

		# 0x0152: ??

		for i in range(2):
			self.f.read(5)
			self.f.read(4)

		for i in range(3):
			self.f.read(8)
			self.f.read(4)

		self.f.read(5)
		self.f.read(4)

		# 0x0191: player setup
		# 8 players, 202 byte per player

		self.player = []
		for i in range(8):
			self.player.append( Player(self.f.read(LENGTH_PLAYER), debug=self.debug) )

		# 0x07e1 - 0x0a29: game setup

		self.f.read(LENGTH_GAMESETUP)

		# 0x0a2a - 0x140a
		# 3x klingon turrent ??
		# 843 bytes per turret

		for i in range(3):
			self.f.read(LENGTH_TURRET)

		# 0x00140b - 0x01d90e: nebulae
		# varying counts, 827 bytes per nebula

		self.nebulae = []
		for i in range(18): # don't know the exact number
			self.nebulae.append( Nebula(self.f.read(LENGTH_NEBULA), debug=self.debug) )

		# 3x Ferengi Marauder

		for i in range(4):
			self.f.read(LENGTH_FERENGIMARAUDER)

		# Directional Light

		self.f.read(LENGTH_DIRECTIONALLIGHT)

		# Black Hole

		self.f.read(LENGTH_BLACKHOLE)

		# Beta Lankal

		self.f.read(LENGTH_PLANET)

		# Dilithium Moon

		self.f.read(LENGTH_MOON)

		# more nebulas

		for i in range(5):
			self.nebulae.append( Nebula(self.f.read(LENGTH_NEBULA), debug=self.debug) )

		print str2hex(self.f.read(8))

		# several (infinite) moons

		# 0x020e26: Borg Dilithium Mining Station

		# 0x02150e: Borg Sphere

		# Klingon Sensor Array

		# 3x Klingon construction something ...

		# Romulan Shrike Class

		# 8x information on the player's resources (?)

		# Mission description

		# information on ongoing "processes"
		# e.g. CraftProcess, StarbaseProcess, SalvageProcess

		# 8x Camera setup

		# many, many instances of unknown information

		# 8x (?): AI setup

		# summary of nebulas and moons (?)

		# EOF

	def save(self):
		# write back to file, once it works
		return

	def saveas(self, filename):
		self.filename = filename
		self.save()


if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		sav = SAV(argv[1], debug=True)
	else:
		sav = SAV('games/s11.sav', debug=True)
#	sav.saveas('test.sav')

