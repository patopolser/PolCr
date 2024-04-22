from polcr.ext.utils.position import Position
from ..strings import string_with_arrows

class Error:
    def __init__(self, pos: Position, error_name: str, details: str):
        self.pos = pos
        self.error_name = error_name
        self.details = details
    
    def as_string(self) -> str:
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos.file_name}, line {self.pos.line + 1}'
        
        return result

class IllegalCharError(Error):
    def __init__(self, pos, details):
        super().__init__(pos, 'Illegal Character', details)

class ExpectedCharError(Error):
	def __init__(self, pos, details):
		super().__init__(pos, 'Expected Character', details)

class InvalidSyntaxError(Error):
		def __init__(self, pos, details):
				super().__init__(pos, 'Invalid Syntax', details)

class RTError(Error):
	def __init__(self, pos, details, context):
		super().__init__(pos, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos.file_text, self.pos)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos
		ctx = self.context

		while ctx:
			result = f'  File {pos.file_name}, line {str(pos.line + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result