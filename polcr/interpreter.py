from .ext import *

class Interpreter:
	def visit(self, node, context: Context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node) -> None:
		raise Exception(f'No visit_{type(node).__name__} method defined')

	def visit_NumberNode(self, node: NumberNode, context: Context) -> RTResult:
		return RTResult().success(
			Number(node.token.value).set_context(context).set_pos(node.pos)
		)

	def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
		response = RTResult()
		left = response.register(self.visit(node.left_node, context))

		if response.should_return(): 
			return response

		right = response.register(self.visit(node.right_node, context))
		
		if response.should_return(): 
			return response
		

		if node.op_token.type in ARITHMETIC.values():
			result, error = left.arithmetic_op(right, node.op_token.type)

		elif node.op_token.type in COMPARISION.values():
			result, error = left.comparision_op(right, node.op_token.type)

		elif node.op_token.matches(TOKENS["KEYWORD"], "y"):
			result, error = left.anded_by(right)

		elif node.op_token.matches(TOKENS["KEYWORD"], "o"):
			result, error = left.ored_by(right)

		if error:
			return response.failure(error)

		else:
			return response.success(result.set_pos(node.pos))

	def visit_UnaryOpNode(self, node: BinOpNode, context: Context) -> RTResult:
		response = RTResult()
		number = response.register(self.visit(node.node, context))
		
		if response.should_return(): 
			return response

		error = None

		if node.op_token.type == TOKENS["-"]:
			number, error = number.multed_by(Number(-1))

		elif node.op_token.matches(TOKENS["KEYWORD"], "no"):
			number, error = number.notted()

		if error:
			return response.failure(error)
		else:
			return response.success(number.set_pos(node.pos))

	def visit_VarAccessNode(self, node: VarAccessNode, context):
		response = RTResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)

		if not value:
			return response.failure(RTError(node.pos, f"'{var_name}' is not defined", context))

		value = value.copy().set_pos(node.pos).set_context(context)
		
		return response.success(value)

	def visit_VarAssignNode(self, node: VarAssignNode, context):
		response = RTResult()
		var_name = node.var_name_token.value
		value = response.register(self.visit(node.value_node, context))

		if response.should_return(): 
			return response

		context.symbol_table.set(var_name, value)
		return response.success(value)

	def visit_IfNode(self, node, context):
		response = RTResult()

		for condition, expr, should_return_null in node.cases:
			condition_value = response.register(self.visit(condition, context))

			if response.should_return(): 
				return response

			if condition_value.is_true():
				expr_value = response.register(self.visit(expr, context))

				if response.should_return(): 
					return response

				return response.success(Number.null if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			expr_value = response.register(self.visit(expr, context))

			if response.should_return(): 
				return response

			return response.success(Number.null if should_return_null else expr_value)

		return response.success(Number.null)

	def visit_ForNode(self, node, context):
		response = RTResult()
		elements = []

		start_value = response.register(self.visit(node.start_value_node, context))
		
		if response.should_return(): 
			return response

		end_value = response.register(self.visit(node.end_value_node, context))
		
		if response.should_return(): 
			return response

		if node.step_value_node:
			step_value = response.register(self.visit(node.step_value_node, context))
		
		if response.should_return(): 
			return response

		else:
			step_value = Number(1)

		i = start_value.value

		if step_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value
		
		while condition():
			context.symbol_table.set(node.var_name_token.value, Number(i))
			i += step_value.value

			value = response.register(self.visit(node.body_node, context))
			if response.should_return() and response.loop_should_continue == False and response.loop_should_break == False: 
				return response
			
			if response.loop_should_continue:
				continue
			
			if response.loop_should_break:
				break

			elements.append(value)

		return response.success(Number.null if node.should_return_null else List(elements).set_context(context).set_pos(node.pos))

	def visit_WhileNode(self, node, context):
		response = RTResult()
		elements = []

		while True:
			condition = response.register(self.visit(node.condition_node, context))

			if response.should_return(): 
				return response

			if not condition.is_true():
				break

			value = response.register(self.visit(node.body_node, context))

			if response.should_return() and response.loop_should_continue == False and response.loop_should_break == False: 
				return response

			if response.loop_should_continue:
				continue
			
			if response.loop_should_break:
				break

			elements.append(value)

		return response.success(Number.null if node.should_return_null else List(elements).set_context(context).set_pos(node.pos))

	def visit_FuncDefNode(self, node, context):
		response = RTResult()

		func_name = node.var_name_token.value if node.var_name_token else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos)
		
		if node.var_name_token:
			context.symbol_table.set(func_name, func_value)

		return response.success(func_value)

	def visit_CallNode(self, node: CallNode, context: Context) -> RTResult:
		response = RTResult()
		args = []

		value_to_call = response.register(self.visit(node.node_to_call, context))

		if response.should_return(): 
			return response

		value_to_call = value_to_call.copy().set_pos(node.pos)

		for arg_node in node.arg_nodes:
			args.append(response.register(self.visit(arg_node, context)))

			if response.should_return(): 
				return response

		return_value = response.register(value_to_call.execute(args))

		if response.should_return(): 
			return response

		return_value = return_value.copy().set_pos(node.pos).set_context(context)

		return response.success(return_value)

	def visit_StringNode(self, node: StringNode, context: Context):
		return RTResult().success(String(node.token.value).set_context(context).set_pos(node.pos))

	def visit_ListNode(self, node: ListNode, context: Context) -> RTResult:
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
		
		if res.should_return(): 
			return res

		return res.success(List(elements).set_context(context).set_pos(node.pos))

	def visit_ReturnNode(self, node, context):
		response = RTResult()

		if node.node_to_return:
			value = response.register(self.visit(node.node_to_return, context))

			if response.should_return(): 
				return response

		else:
			value = Number.null
		
		return response.success_return(value)

	def visit_ContinueNode(self):
		return RTResult().success_continue()

	def visit_BreakNode(self):
		return RTResult().success_break()


class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def execute(self, args):
		response = RTResult()
		interpreter = Interpreter()
		exec_ctx = self.generate_new_context()

		response.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if response.should_return(): 
			return response

		value = response.register(interpreter.visit(self.body_node, exec_ctx))

		if response.should_return() and response.func_return_value == None: 
			return response

		ret_value = (value if self.should_auto_return else None) or response.func_return_value or Number.null

		return response.success(ret_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos)
		return copy

	def __repr__(self):
		return f"<function {self.name}>"