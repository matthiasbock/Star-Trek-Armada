#!/usr/bin/python

class Player:
	def __init__(self, binary, debug=False):
		self.debug = debug

		self.name = binary[175:195]
		if self.debug:
			print self.name

class SAV:
	def __init__(self, filename=None, debug=False):

		self.debug = debug

		self.version		= 'version [1] =\x0d\x0a2053\x0d\x0asaveGameDesc = '
		self.saveGameDesc	= ''
		self.binary		= '\x0d\x0abinarySave [1] =\x0d\x0atrue\x0d\x0a'
		self.untitled		= '\x02\xdd\x60\x00\x10\x00\x00\x00untitled.bzn\x00\x00\x00'

		if filename is not None:
			self.open(filename)

	def open(self, filename):
		self.f = open(filename)

		assert self.f.read(36) == self.version	# 0x000 - 0x023

		d = self.f.read(256)			# 0x024 - 0x123
		self.saveGameDesc = ''.join([chr(int(d[i*2]+d[i*2+1], 16)) for i in range(128)]).strip()

		if self.debug:
			print self.saveGameDesc

		assert self.f.read(26) == self.binary	# 0x124 - 0x13D

		assert self.f.read(23) == self.untitled	# 0x13E - 0x155

		for i in range(5):			# 0x156 - 0x193
			self.f.read(12)

		# 0x194 - 0x7e4: player info
		# 8 players, 202 byte per player

		self.player = []
		for i in range(8):
			self.player.append( Player(self.f.read(202), debug=self.debug) )

		

		# 0x00140b - 0x01d90e
		# nebulae, varying counts, 827 bytes per nebula
		# 

		self.nebulae = []
		for i in range(140): # don't know the exact number
			self.nebulae.append( Nebula(self.f.read(827), debug=self.debug) )

		# moons


	def save(self):
		# write back to file, once it works
		return

	def saveas(self, filename):
		self.filename = filename
		self.save()


if __name__ == '__main__':
	import sys
	sav = SAV(sys.argv[1], debug=True)
	sav.saveas('test.sav')

