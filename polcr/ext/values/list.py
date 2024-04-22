from .value import Value
from .number import Number
from ..utils import RTError

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):

		if isinstance(other, Number):
			new_list = self.copy()
			
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			
			except:
				return None, RTError(other.pos, 'El elemento no se encuentra en la lista', self.context)

		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):

		if isinstance(other, List):
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None

		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):

		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			
			except:
				return None, RTError(other.pos, 'El elemento no se encuentra en la lista', self.context)

		else:
			return None, Value.illegal_operation(self, other)

	def copy(self):
		copy = List(self.elements[:])
		copy.set_pos(self.pos)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return ", ".join([str(x) for x in self.elements])

	def __repr__(self):
		return f'[{", ".join([str(x) for x in self.elements])}]'