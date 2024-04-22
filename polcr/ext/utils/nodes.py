from .tokens import Token

class NumberNode:
	def __init__(self, token: Token):
		self.token = token
		self.pos = self.token.pos

	def __repr__(self):
		return f'{self.token}'
	
class BinOpNode:
	def __init__(self, left_node, op_token: Token, right_node):
		self.left_node = left_node
		self.op_token = op_token
		self.right_node = right_node
		self.pos = self.op_token.pos

	def __repr__(self):
		return f'({self.left_node}, {self.op_token}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_token: Token, node):
		self.op_token = op_token
		self.node = node

		self.pos = op_token.pos

	def __repr__(self):
		return f'({self.op_token}, {self.node})'

class VarAccessNode:
	def __init__(self, var_name_token: Token):
		self.var_name_token = var_name_token

		self.pos = var_name_token.pos

class VarAssignNode:
	def __init__(self, var_name_token: Token, value_node):
		self.var_name_token = var_name_token
		self.value_node = value_node

		self.pos = var_name_token.pos

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.pos = self.cases[0][0].pos

class ForNode:
	def __init__(self, var_name_token, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
		self.var_name_token = var_name_token
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos = self.var_name_token.pos

class WhileNode:
	def __init__(self, condition_node, body_node, should_return_null):
		self.condition_node = condition_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos = self.condition_node.pos

class FuncDefNode:
	def __init__(self, var_name_token, arg_name_tokens, body_node, should_auto_return):
		self.var_name_token = var_name_token
		self.arg_name_tokens = arg_name_tokens
		self.body_node = body_node
		self.should_auto_return = should_auto_return
		
		if self.var_name_token:
			self.pos = self.var_name_token.pos

		elif len(self.arg_name_tokens) > 0:
			self.pos = self.arg_name_tokens[0].pos
			
		else:
			self.pos = self.body_node.pos


class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

		self.pos = self.node_to_call.pos

class StringNode:
	def __init__(self, token):
		self.token = token
		self.pos = self.token.pos

	def __repr__(self):
		return f'{self.token}'
		
class ListNode:
  def __init__(self, element_nodes, pos):
    self.element_nodes = element_nodes

    self.pos = pos

  def __repr__(self):
    return self.element_nodes

class ReturnNode:
  def __init__(self, node_to_return, pos):
    self.node_to_return = node_to_return

    self.pos = pos

class ContinueNode:
  def __init__(self, pos_start, pos_end):
    self.pos_start = pos_start
    self.pos_end = pos_end

class BreakNode:
  def __init__(self, pos):
    self.pos = pos