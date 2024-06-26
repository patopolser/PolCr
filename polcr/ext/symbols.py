
from .values import *

class SymbolTable:
	def __init__(self, parent= None):
		self.symbols = {
			"NULL": Number(0),
			"True": Number(1),
			"False": Number(0),
			}

		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)

		if value == None and self.parent:
			return self.parent.get(name)

		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]
