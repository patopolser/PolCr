from polcr.ext.utils.tokens import ARITHMETIC
from .number import Number
from .value import Value

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def arithmetic_op(self, other, op: str):
		if isinstance(other, String) and op == ARITHMETIC["+"]:
			return String(self.value + other.value).set_context(self.context), None
		
		elif isinstance(other, Number):

			if op == ARITHMETIC["+"]:
				return String(self.value + str(other.value)).set_context(self.context), None
			
			elif op == ARITHMETIC["*"]:
				return String(self.value * other.value).set_context(self.context), None
	
		else:
			return None, Value.illegal_operation(self, other)


	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return f'"{self.value}"'