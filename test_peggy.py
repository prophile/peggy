from peggy import Parser, ParseError, dot, pure, literal, eof, oneof, parser
from nose.tools import raises

def test_parse_dot():
    assert dot.parse('x') == ('x', '')

@raises(ParseError)
def test_fail_dot():
    dot.parse('')

def test_parse_pure():
    key = object()
    assert pure(key).parse('x') == (key, 'x')

def test_parse_pure_empty():
    key = object()
    assert pure(key).parse('') == (key, '')

def test_parse_peek():
    assert dot.peek.parse('x') == ('x', 'x')

@raises(ParseError)
def test_parse_peek_fail():
    dot.peek.parse('')

def test_parse_literal():
    assert literal('bees').parse('bees and cheese') == ('bees', ' and cheese')

@raises(ParseError)
def test_parse_fail_literal():
    literal('beep').parse('bee')

def test_parse_alternative_left():
    assert (literal('bees') / literal('faces')).parse('bees') == ('bees', '')

def test_parse_alternative_right():
    assert (literal('bees') / literal('faces')).parse('faces') == ('faces', '')

@raises(ParseError)
def test_parse_alternative_neither():
    (literal('bees') / literal('faces')).parse('horse')

def test_parse_optional_match():
    assert literal('bees').optional('faces').parse('bees') == ('bees', '')

def test_parse_optional_reject():
    assert literal('bees').optional('faces').parse('death') == ('faces', 'death')

def test_many():
    assert literal('xy').many.parse('xyxyxyz') == (['xy', 'xy', 'xy'], 'z')

def test_many_empty():
    assert literal('bees').many.parse('pony') == ([], 'pony')

def test_many_single():
    assert literal('xy').many.parse('xyz') == (['xy'], 'z')

def test_some():
    assert literal('xy').some.parse('xyxyxyz') == (['xy', 'xy', 'xy'], 'z')

@raises(ParseError)
def test_some_empty():
    literal('bees').some.parse('pony')

def test_some_single():
    assert literal('xy').some.parse('xyz') == (['xy'], 'z')

def test_eof():
    assert eof.parse('') == (None, '')

@raises(ParseError)
def test_not_eof():
    eof.parse('bees')

def test_one_of():
    assert oneof('abc').parse('ab') == ('a', 'b')

@raises(ParseError)
def test_fail_one_of():
    oneof('abc').parse('dc')

def test_parse_decorator():
    @parser
    def example():
        a = yield oneof('ab')
        b = yield oneof('cd')
        return (a, b)
    assert example.parse('ad') == (('a', 'd'), '')

def test_rseq():
    assert (oneof('ab') >> oneof('cd')).parse('ad') == ('d', '')

def test_lseq():
    assert (oneof('ab') << oneof('cd')).parse('ad') == ('a', '')

