from polcr.ext.utils.position import Position


def string_with_arrows(text, pos: Position):
    result = ''

    idx_start = max(text.rfind('\n', 0, pos.index), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    line_count = pos.line
    for i in range(line_count):

        line = text[idx_start:idx_end]
        col_start = pos.column if i == 0 else 0
        col_end = pos.column if i == line_count - 1 else len(line) - 1

        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')