import peggy

from functools import reduce

@peggy.parser
def sum_part():
    operation = yield peggy.oneof('+-')
    rhs = yield product_expr
    return lambda lhs: (operation, lhs, rhs)

@peggy.parser
def sum_expr():
    first = yield product_expr
    elements = yield sum_part.many
    return reduce(lambda l, r: r(l), elements, first)

@peggy.parser
def product_part():
    operation = yield peggy.oneof('*/')
    rhs = yield base_expr
    return lambda lhs: (operation, lhs, rhs)

@peggy.parser
def product_expr():
    first = yield base_expr
    elements = yield product_part.many
    return reduce(lambda l, r: r(l), elements, first)

@peggy.parser
def base_integer():
    elements = yield peggy.oneof('0123456789').some
    return ('literal', int(''.join(elements)))

@peggy.parser
def base_parens():
    lparen = yield peggy.literal('(')
    result = yield sum_expr
    rparen = yield peggy.literal(')')
    return result

base_expr = base_integer / base_parens

print(sum_expr.run('3-2-1'))

