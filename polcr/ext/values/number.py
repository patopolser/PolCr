from polcr.ext.utils.tokens import ARITHMETIC, COMPARISION
from ..utils.position import Position
from ..utils.errors import RTError

class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()
		self.set_context()

	def set_pos(self, pos: Position = None):
		self.pos = pos

		return self

	def set_context(self, context = None):
		self.context = context
		return self
	
	def arithmetic_op(self, other, op: str):

		if not isinstance(other, Number):
			return None
		
		if op == ARITHMETIC["+"]:
			return Number(self.value + other.value).set_context(self.context), None
		
		elif op == ARITHMETIC["-"]:
			return Number(self.value - other.value).set_context(self.context), None

		elif op == ARITHMETIC["*"]:
			return Number(self.value * other.value).set_context(self.context), None
		
		elif op == ARITHMETIC["/"]:
			if other.value == 0:
				return None, RTError(other.pos, 'Divison por cero', self.context)

			return Number(self.value / other.value).set_context(self.context), None
		
		elif op == ARITHMETIC["%"]:
			if other.value == 0:
				return None, RTError(other.pos, 'Divison por cero', self.context)

			return Number(self.value % other.value).set_context(self.context), None
		
		elif op == ARITHMETIC["^"]:
			return Number(self.value ** other.value).set_context(self.context), None
			

	def comparision_op(self, other, op: str):

		if not isinstance(other, Number):
			return None
		
		if op == COMPARISION["=="]:
			return Number(int(self.value == other.value)).set_context(self.context), None
		
		elif op == COMPARISION["!="]:
			return Number(int(self.value != other.value)).set_context(self.context), None

		elif op == COMPARISION["<"]:
			return Number(int(self.value < other.value)).set_context(self.context), None
		
		elif op == COMPARISION[">"]:
			return Number(int(self.value > other.value)).set_context(self.context), None
		
		elif op == COMPARISION[">="]:
			return Number(int(self.value >= other.value)).set_context(self.context), None
		
		elif op == COMPARISION["<="]:
			return Number(int(self.value <= other.value)).set_context(self.context), None

		
	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos)
		copy.set_context(self.context)
		
		return copy

	def is_true(self):
		return self.value != 0

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)