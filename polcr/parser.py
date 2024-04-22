from .ext import *

class ParserResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.last_registered_advance_count = 0
		self.advance_count = 0
		self.to_reverse_count = 0

	def register_advancement(self):
		self.last_registered_advance_count = 1
		self.advance_count += 1

	def register(self, response):
		self.last_registered_advance_count = response.advance_count
		self.advance_count += response.advance_count

		if isinstance(response, ParserResult):
			if response.error: 
				self.error = response.error

			return response.node

		return response

	def try_register(self, response):
		if response.error:
			self.to_reverse_count = response.advance_count
			return None

		return self.register(response)

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.last_registered_advance_count == 0:
			self.error = error

		return self

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.advance()

	def advance(self):
		self.token_index += 1
		self.update_current_token()
		return self.current_token

	def reverse(self, amount=1):
		self.token_index -= amount
		self.update_current_token()
		return self.current_token

	def update_current_token(self):
		if self.token_index >= 0 and self.token_index < len(self.tokens):
			self.current_token = self.tokens[self.token_index]

	def parse(self) -> ParserResult:
		response = self.statements()

		if not response.error and self.current_token.type != TOKENS["EOF"]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))
		
		return response

	def term(self) -> ParserResult:
		return self.bin_op(self.factor, (TOKENS["*"], TOKENS["/"], TOKENS["%"]))

	def power(self):
		return self.bin_op(self.call, (TOKENS["^"], ), self.factor)

	def statements(self):
		response = ParserResult()
		statements = []

		while self.current_token.type == TOKENS[";\n"]:
			response.register_advancement()
			self.advance()

		statement = response.register(self.statement())

		if response.error: 
			return response
		
		more_statements = True

		if response.error: 
			return response

		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			while self.current_token.type == TOKENS[";\n"]:
				response.register_advancement()
				self.advance()
				newline_count += 1

			if newline_count == 0:
				more_statements = False
		
			if not more_statements: 
				break

			statement = response.try_register(self.statement())

			if not statement:
				self.reverse(response.to_reverse_count)
				more_statements = False
				continue
		
			statements.append(statement)
			
		return response.success(ListNode(statements, self.current_token.pos.copy()))

	def statement(self):
		response = ParserResult()

		if self.current_token.matches(TOKENS["KEYWORD"], "devolver"):
			response.register_advancement()
			self.advance()

			expr = response.try_register(self.expresion())
			if not expr:
				self.reverse(response.to_reverse_count)

			return response.success(ReturnNode(expr, self.current_token.pos.copy()))
		
		if self.current_token.matches(TOKENS["KEYWORD"], "continuar"):
			response.register_advancement()
			self.advance()
			return response.success(ContinueNode(self.current_token.pos.copy()))
		
		if self.current_token.matches(TOKENS["KEYWORD"], "salir"):
			response.register_advancement()
			self.advance()
			return response.success(BreakNode(self.current_token.pos.copy()))

		expr = response.register(self.expresion())

		if response.error:
			return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		return response.success(expr)

	def call(self):
		response = ParserResult()
		atom = response.register(self.atom())

		if response.error: 
			return response

		if self.current_token.type == TOKENS["("]:
			response.register_advancement()
			self.advance()
			arg_nodes = []

			if self.current_token.type == TOKENS[")"]:
				response.register_advancement()
				self.advance()

			else:
				arg_nodes.append(response.register(self.expresion()))

				if response.error:
					return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

				while self.current_token.type == TOKENS[","]:
					response.register_advancement()
					self.advance()

					arg_nodes.append(response.register(self.expresion()))

					if response.error: 
						return response

				if self.current_token.type != TOKENS[")"]:
					return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

				response.register_advancement()
				self.advance()

			return response.success(CallNode(atom, arg_nodes))

		return response.success(atom)

	def arith_expr(self):
		return self.bin_op(self.term, (TOKENS['+'], TOKENS['-']))

	def if_expresion(self):
		response = ParserResult()
		all_cases = response.register(self.if_expresion_cases("si"))

		if response.error: 
			return response

		cases, else_case = all_cases
		return response.success(IfNode(cases, else_case))

	def if_expresion_b(self):
		return self.if_expresion_cases("sino_si")
    
	def if_expresion_c(self):
		response = ParserResult()
		else_case = None

		if self.current_token.matches(TOKENS["KEYWORD"], "sino"):
			response.register_advancement()
			self.advance()

		if self.current_token.type == TOKENS[";\n"]:
			response.register_advancement()
			self.advance()

			statements = response.register(self.statements())

			if response.error: 
				return response

			else_case = (statements, True)

			if self.current_token.matches(TOKENS["KEYWORD"], "fin"):
				response.register_advancement()
				self.advance()
			
			else:
				return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		else:
			expr = response.register(self.statement())

			if response.error: 
				return response

			else_case = (expr, False)

		return response.success(else_case)

	def if_expresion_b_or_c(self):
		response = ParserResult()
		cases, else_case = [], None

		if self.current_token.matches(TOKENS["KEYWORD"], "sino_si"):
			all_cases = response.register(self.if_expresion_b())

			if response.error: 
				return response

			cases, else_case = all_cases

		else:
			else_case = response.register(self.if_expresion_c())

		if response.error: 
			return response
    
		return response.success((cases, else_case))

	def if_expresion_cases(self, case_keyword):
		response = ParserResult()
		cases = []
		else_case = None

		if not self.current_token.matches(TOKENS["KEYWORD"], case_keyword):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		condition = response.register(self.expresion())

		if response.error: 
			return response

		if not self.current_token.matches(TOKENS["KEYWORD"], "entonces"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS[";\n"]:
			response.register_advancement()
			self.advance()

			statements = response.register(self.statements())
			
			if response.error: 
				return response

			cases.append((condition, statements, True))

			if self.current_token.matches(TOKENS["KEYWORD"], "fin"):
				response.register_advancement()
				self.advance()
			
			else:
				all_cases = response.register(self.if_expresion_b_or_c())
				
				if response.error:
					return response

				new_cases, else_case = all_cases
				cases.extend(new_cases)

		else:
			expr = response.register(self.statement())
			
			if response.error: 
				return response

			cases.append((condition, expr, False))

			all_cases = response.register(self.if_expresion_b_or_c())
			
			if response.error: 
				return response
			
			new_cases, else_case = all_cases
			cases.extend(new_cases)

		return response.success((cases, else_case))

	def for_expresion(self):
		response = ParserResult()

		if not self.current_token.matches(TOKENS["KEYWORD"], "desde"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type != TOKENS["IDENTIFIER"]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		var_name = self.current_token
		response.register_advancement()
		self.advance()

		if self.current_token.type != TOKENS["="]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))
		
		response.register_advancement()
		self.advance()

		start_value = response.register(self.expresion())

		if response.error: 
			return response

		if not self.current_token.matches(TOKENS["KEYWORD"], "hasta"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))
		
		response.register_advancement()
		self.advance()

		end_value = response.register(self.expresion())

		if response.error: 
			return response

		if self.current_token.matches(TOKENS["KEYWORD"], "paso"):
			response.register_advancement()
			self.advance()

			step_value = response.register(self.expresion())

			if response.error: 
				return response
		else:
			step_value = None

		if not self.current_token.matches(TOKENS["KEYWORD"], "entonces"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS[";\n"]:
			response.register_advancement()
			self.advance()

			body = response.register(self.statements())

			if response.error: 
				return response

			if not self.current_token.matches(TOKENS["KEYWORD"], "fin"):
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

			response.register_advancement()
			self.advance()

			return response.success(ForNode(var_name, start_value, end_value, step_value, body, True))

		body = response.register(self.statement())

		if response.error: 
			return response

		return response.success(ForNode(var_name, start_value, end_value, step_value, body, False))

	def while_expresion(self):
		response = ParserResult()

		if not self.current_token.matches(TOKENS["KEYWORD"], "mientras"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		condition = response.register(self.expresion())

		if response.error: 
			return response

		if not self.current_token.matches(TOKENS["KEYWORD"], "entonces"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS[";\n"]:
			response.register_advancement()
			self.advance()

			body = response.register(self.statements())

			if response.error: 
				return response

			if not self.current_token.matches(TOKENS["KEYWORD"], "fin"):
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

			response.register_advancement()
			self.advance()

			return response.success(WhileNode(condition, body, True))

		body = response.register(self.statement())

		if response.error: 
			return response

		return response.success(WhileNode(condition, body, False))

	def atom(self) -> ParserResult:
		response = ParserResult()
		token = self.current_token
		
		if token.type in (TOKENS["INT"], TOKENS["FLOAT"]):
			response.register_advancement()
			self.advance()
			
			return response.success(NumberNode(token))

		elif token.type == TOKENS["STRING"]:
			response.register_advancement()
			self.advance()

			return response.success(StringNode(token))

		elif token.type == TOKENS['IDENTIFIER']:
			response.register_advancement()
			self.advance()
			return response.success(VarAccessNode(token))

		elif token.type == TOKENS["("]:
			response.register_advancement()
			self.advance()

			expr = response.register(self.expresion())

			if response.error: 
				return response

			if self.current_token.type == TOKENS[")"]:
				response.register_advancement()
				self.advance()

				return response.success(expr)

			else:
				return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		elif token.type == TOKENS['[']:
			list_expr = response.register(self.list_expresion())

			if response.error: 
				return response

			return response.success(list_expr)


		elif token.matches(TOKENS["KEYWORD"], "si"):
			if_expresion = response.register(self.if_expresion())
			
			if response.error: 
				return response

			return response.success(if_expresion)

		elif token.matches(TOKENS["KEYWORD"], "desde"):
			for_expr = response.register(self.for_expresion())

			if response.error: 
				return response

			return response.success(for_expr)

		elif token.matches(TOKENS["KEYWORD"], "mientras"):
			while_expr = response.register(self.while_expresion())

			if response.error: 
				return response

			return response.success(while_expr)

		elif token.matches(TOKENS["KEYWORD"], "funcion"):
			func_def = response.register(self.func_def())

			if response.error: 
				return response

			return response.success(func_def)

		return response.failure(InvalidSyntaxError(token.pos, "Sintaxis inválida"))

	def factor(self) -> ParserResult:
		response = ParserResult()
		token = self.current_token

		if token.type in (TOKENS["+"], TOKENS["-"]):
			response.register_advancement()
			self.advance()

			factor = response.register(self.factor())

			if response.error: 
				return response
				
			return response.success(UnaryOpNode(token, factor))

		return self.power()

	def comp_expr(self):
		response = ParserResult()

		if self.current_token.matches(TOKENS['KEYWORD'], "no"):
			op_token = self.current_token
			response.register_advancement()
			self.advance()

			node = response.register(self.comp_expr())

			if response.error: 
				return response

			return response.success(UnaryOpNode(op_token, node))
		
		node = response.register(self.bin_op(self.arith_expr, (
			TOKENS['=='], TOKENS['!='], TOKENS['<'], 
			TOKENS['>'], TOKENS['<='], TOKENS['>=']
			)))
		
		if response.error:
			return response.failure(InvalidSyntaxError(
				self.current_token.pos, "Sintaxis inválida"))

		return response.success(node)

	def expresion(self) -> ParserResult:
		response = ParserResult()

		if self.current_token.matches(TOKENS['KEYWORD'], 'polser'):
			response.register_advancement()
			self.advance()

			if self.current_token.type != TOKENS['IDENTIFIER']:
				return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

			var_name = self.current_token
			response.register_advancement()
			self.advance()

			if self.current_token.type != TOKENS['=']:
				return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

			response.register_advancement()
			self.advance()
			expr = response.register(self.expresion())

			if response.error: 
				return response

			return response.success(VarAssignNode(var_name, expr))

		node = response.register(self.bin_op(self.comp_expr, ((TOKENS['KEYWORD'], "y"), (TOKENS['KEYWORD'], "o")) ))

		if response.error:
			return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		return response.success(node)

	def func_def(self):
		response = ParserResult()

		if not self.current_token.matches(TOKENS["KEYWORD"], "funcion"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS["IDENTIFIER"]:
			var_name_token = self.current_token
			response.register_advancement()
			self.advance()

			if self.current_token.type != TOKENS["("]:
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		else:
			var_name_token = None

			if self.current_token.type != TOKENS["("]:
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))
		
		response.register_advancement()
		self.advance()
		arg_name_tokens = []

		if self.current_token.type == TOKENS["IDENTIFIER"]:
			arg_name_tokens.append(self.current_token)
			response.register_advancement()
			self.advance()
			
			while self.current_token.type == TOKENS[","]:
				response.register_advancement()
				self.advance()

				if self.current_token.type != TOKENS["IDENTIFIER"]:
					return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

				arg_name_tokens.append(self.current_token)
				response.register_advancement()
				self.advance()
			
			if self.current_token.type != TOKENS[")"]:
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))
				
		else:
			if self.current_token.type != TOKENS[")"]:
				return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS["~>"]:
			response.register_advancement()
			self.advance()

			body = response.register(self.expresion())

			if response.error: 
				return response

			return response.success(FuncDefNode(var_name_token, arg_name_tokens, body, False))
			
		if self.current_token.type != TOKENS[";\n"]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		body = response.register(self.statements())

		if response.error: 
			return response

		if not self.current_token.matches(TOKENS["KEYWORD"], "fin"):
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()
		
		return response.success(FuncDefNode(var_name_token, arg_name_tokens, body, True))

	def list_expresion(self):
		response = ParserResult()
		element_nodes = []

		if self.current_token.type != TOKENS["["]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		if self.current_token.type == TOKENS["]"]:
			response.register_advancement()
			self.advance()

		else:
			element_nodes.append(response.register(self.expresion()))

			if response.error:
				return response.failure(InvalidSyntaxError(self.current_token.pos, "Sintaxis inválida"))

		while self.current_token.type == TOKENS[","]:
			response.register_advancement()
			self.advance()

			element_nodes.append(response.register(self.expresion()))

			if response.error: 
				return response

		if self.current_token.type != TOKENS["]"]:
			return response.failure(InvalidSyntaxError(self.current_token.pos, f"Sintaxis inválida"))

		response.register_advancement()
		self.advance()

		return response.success(ListNode(element_nodes, self.current_token.pos.copy()))


	def bin_op(self, func_a: ParserResult, operations: tuple[str], func_b: ParserResult = None) -> ParserResult:
	
		func_b = func_a if func_b == None else func_b

		response = ParserResult()
		left = response.register(func_a())

		if response.error: 
			return response

		while self.current_token.type in operations or (self.current_token.type, self.current_token.value) == operations[0]:
			op_token = self.current_token

			response.register_advancement()
			self.advance()

			right = response.register(func_b())

			if response.error: 
				return response

			left = BinOpNode(left, op_token, right)

		return response.success(left)
