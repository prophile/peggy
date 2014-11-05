class Parser(object):
    """A parser."""
    def __init__(self, parse):
        """Standard, direct constructor. The parse handler takes a string and
        returns either a (result, unparsed-rest) pair or raises a ParseError."""
        self.parse = parse

    """Run, requiring no residue."""
    def run(self, input):
        result, residue = self.parse(input)
        if residue:
            raise ParseError()
        return result

    @property
    def peek(self):
        """A variation on parser which returns results but does not consume
        input."""
        def _new_parser(input):
            data, _ = self.parse(input)
            return data, input
        return Parser(_new_parser)

    def __truediv__(self, other):
        """Ordered choice. If the left hand side matches it is used, otherwise
        the right hand side is used."""
        def _internal_parser(string):
            try:
                return self.parse(string)
            except ParseError:
                return other.parse(string)
        return Parser(_internal_parser)

    def optional(self, default):
        """Optionality, equivalent to the ? operator. Returns the default
        argument if there is no match."""
        def _internal_parser(string):
            try:
                return self.parse(string)
            except ParseError:
                return default, string
        return Parser(_internal_parser)

    @property
    def many(self):
        """Kleene star: match zero or more. Returns results as a list."""
        def _internal_parser(string):
            results = []
            try:
                while True:
                    step, string = self.parse(string)
                    results.append(step)
            except ParseError:
                return results, string
        return Parser(_internal_parser)

    @property
    def some(self):
        """Plus operator: match one or more. Returns results as a list."""
        many = self.many
        def _internal_parser(string):
            result, leftover = many.parse(string)
            if not result:
                raise ParseError()
            return result, leftover
        return Parser(_internal_parser)

    def filter(self, pred):
        """Filter combinator: accept only under some predicate on results."""
        def _internal_parser(string):
            result, rest = self.parse(string)
            if not pred(result):
                raise ParseError()
            return result, rest
        return Parser(_internal_parser)

    def __rshift__(self, other):
        """Right-biased sequencing: take the right result."""
        def _internal_parser(string):
            result_left, interm = self.parse(string)
            result_right, rest = other.parse(interm)
            return result_right, rest
        return Parser(_internal_parser)

    def __lshift__(self, other):
        """Left-biased sequencing: take the left result."""
        def _internal_parser(string):
            result_left, interm = self.parse(string)
            result_right, rest = other.parse(interm)
            return result_left, rest
        return Parser(_internal_parser)

class ParseError(Exception):
    """Exception indicating a failure to parse."""
    pass

def _dot_match(string):
    if string == '':
        raise ParseError()
    else:
        return string[0], string[1:]

dot = Parser(_dot_match)

def pure(x):
    def _handler(string):
        return x, string
    return Parser(_handler)

def literal(k):
    length = len(k)
    def _handle(data):
        if data.startswith(k):
            return k, data[length:]
        else:
            raise ParseError()
    return Parser(_handle)

def _eof_match(string):
    if string == '':
        return (None, '')
    else:
        raise ParseError()

eof = Parser(_eof_match)

def oneof(collection):
    return dot.filter(collection.__contains__)

def parser(f):
    def wrapped(string):
        result = None
        generator = f()
        try:
            while True:
                parser = generator.send(result)
                result, string = parser.parse(string)
        except StopIteration as e:
            return e.value, string
    return Parser(wrapped)

