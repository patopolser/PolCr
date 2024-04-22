from .number import Number
from .string import String
from .list import List
from.value import  Value

from ..utils import *

import os

class BaseFunction(Value):
  def __init__(self, name):
    super().__init__()
    self.name = name or "<anonymous>"

  def generate_new_context(self):
    new_context = Context(self.name, self.context.symbol_table, self.context, self.pos)
    return new_context

  def check_args(self, arg_names, args):
    res = RTResult()

    if len(args) > len(arg_names):
      return res.failure(RTError(self.pos, f"{len(args) - len(arg_names)} too many args passed into {self}", self.context))
    
    if len(args) < len(arg_names):
      return res.failure(RTError(self.pos, f"{len(arg_names) - len(args)} too few args passed into {self}", self.context))

    return res.success(None)

  def populate_args(self, arg_names, args, exec_ctx):
    for i in range(len(args)):
      arg_name = arg_names[i]
      arg_value = args[i]
      arg_value.set_context(exec_ctx)
      exec_ctx.symbol_table.set(arg_name, arg_value)

  def check_and_populate_args(self, arg_names, args, exec_ctx):
    res = RTResult()
    res.register(self.check_args(arg_names, args))
    if res.error: return res
    self.populate_args(arg_names, args, exec_ctx)
    return res.success(None)

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.error: return res

		return_value = res.register(method(exec_ctx))
		if res.error: return res
		return res.success(return_value)
	
	def no_visit_method(self, node, context):
		raise Exception(f'No execute_{self.name} method defined')

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos)
		return copy

	def __repr__(self):
		return f"<built-in function {self.name}>"

	def execute_print(self, exec_ctx):
		if isinstance(exec_ctx.symbol_table.get('value'), String):
			print(str(exec_ctx.symbol_table.get('value'))[1:-1])

		elif isinstance(exec_ctx.symbol_table.get('value'), Number):
			print(str(exec_ctx.symbol_table.get('value')))

		return RTResult().success(Number.null)
	
	execute_print.arg_names = ['value']
	
	def execute_input(self, exec_ctx):
		text = input(str(exec_ctx.symbol_table.get('value'))[1:-1])
		return RTResult().success(String(text))
	
	execute_input.arg_names = ['value']

	def execute_input_int(self, exec_ctx):
		while True:
			text = input(str(exec_ctx.symbol_table.get('value'))[1:-1])
		
			try:
				number = int(text)
				break

			except ValueError:
				print(f"'{text}' must be an integer. Try again!")

		return RTResult().success(Number(number))

	execute_input_int.arg_names = ['value']

	def execute_to_int(self, exec_ctx):
		
		n = exec_ctx.symbol_table.get("value")

		if not isinstance(n,  Number):
			return None

		return RTResult().success(Number(int(n.value)))

	execute_to_int.arg_names = ['value']

	def execute_clear(self, exec_ctx):
		os.system('cls') 
		return RTResult().success(Number.null)
	
	execute_clear.arg_names = []

	def execute_is_number(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
		return RTResult().success(Number.true if is_number else Number.false)
	
	execute_is_number.arg_names = ["value"]

	def execute_is_string(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
		return RTResult().success(Number.true if is_number else Number.false)
	
	execute_is_string.arg_names = ["value"]

	def execute_is_list(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
		return RTResult().success(Number.true if is_number else Number.false)
	
	execute_is_list.arg_names = ["value"]

	def execute_is_function(self, exec_ctx):
		is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
		return RTResult().success(Number.true if is_function else Number.false)
	
	execute_is_function.arg_names = ["value"]

	def execute_int_to_str(self, exec_ctx):
		text = str(exec_ctx.symbol_table.get('value'))
		return RTResult().success(String(text))

	execute_int_to_str.arg_names = ['value']

	def execute_round(self, exec_ctx):
		return RTResult().success(Number(int(exec_ctx.symbol_table.get('value').value)))

	execute_round.arg_names = ['value']

