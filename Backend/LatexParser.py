import re
from collections import deque
import pprint

GREEK = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota',
    'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau',
    'upsilon', 'phi', 'chi', 'psi', 'omega'
]

COMMANDS = [
               'frac', 'sqrt', 'leq', 'geq', 'int', 'sum', 'sin', 'cos', 'tan', 'log', 'ln',
               'lim', 'cdot', 'infty', 'to', 'neq', 'approx'
           ] + GREEK

# 1. Tokeniser
def tokenise_latex(expr):


    token_spec = [
        (r'\\[a-zA-Z]+', 'COMMAND'),
        (r'{', 'LBRACE'),
        (r'}', 'RBRACE'),
        (r'[a-zA-Z]', 'VARIABLE'),
        (r'[0-9]+', 'NUMBER'),
        (r'\^', 'CARET'),
        (r'_', 'UNDERSCORE'),
        (r'[=+\-\*/<>]', 'OPERATOR'),
        (r'\s+', None),  # skip whitespace
    ]

    tok_regex = '|'.join(f'(?P<{name}>{regex})' for regex, name in token_spec if name)
    tokens = []
    for match in re.finditer(tok_regex, expr):
        kind = match.lastgroup
        value = match.group()
        tokens.append((kind, value))
    return tokens


# 2. Parser
def parse(tokens):
    tokens = deque(tokens)

    def parse_expr():
        if not tokens:
            return None

        token = tokens.popleft()
        kind, val = token

        if kind == 'COMMAND':
            name = val[1:]  # remove backslash

            if name == 'frac':
                return {
                    'type': 'fraction',
                    'numerator': parse_braced(),
                    'denominator': parse_braced()
                }

            elif name == 'sqrt':
                return {
                    'type': 'sqrt',
                    'value': parse_braced()
                }

            elif name in ['sum', 'sin', 'cos', 'tan', 'log', 'ln', 'lim']:
                return {
                    'type': 'function',
                    'name': name,
                    'arg': parse_braced()
                }

            elif name in GREEK:
                return {
                    'type': 'greek',
                    'value': name
                }

            else:
                return {
                    'type': 'command',
                    'name': name
                }

        elif kind == 'VARIABLE':
            node = {'type': 'var', 'value': val}
            return maybe_power_or_subscript(node)

        elif kind == 'NUMBER':
            node = {'type': 'number', 'value': int(val)}
            return maybe_power_or_subscript(node)

        elif kind == 'LBRACE':
            # Unbraced group – parse and return directly
            tokens.appendleft((kind, val))
            return parse_braced()

        elif kind == 'OPERATOR':
            return {'type': 'operator', 'value': val}

        return {'type': 'unknown', 'value': val}

    def maybe_power_or_subscript(base):
        if not tokens:
            return base

        if tokens[0][0] == 'CARET':
            tokens.popleft()
            exponent = parse_expr()
            return {'type': 'power', 'base': base, 'exponent': exponent}

        elif tokens[0][0] == 'UNDERSCORE':
            tokens.popleft()
            subscript = parse_expr()
            return {'type': 'subscript', 'base': base, 'subscript': subscript}

        return base

    def parse_braced():
        if not tokens:
            raise ValueError("Unexpected end of input in braced expression")

        kind, val = tokens.popleft()
        if kind != 'LBRACE':
            raise ValueError(f"Expected '{{', got {val}")

        contents = []
        while tokens and tokens[0][0] != 'RBRACE':
            contents.append(parse_expr())

        if not tokens:
            raise ValueError("Missing closing '}'")
        tokens.popleft()  # consume RBRACE
        return contents

    ast = []
    while tokens:
        ast.append(parse_expr())

    return ast


# 3. Example usage
expr = r"\sum{\sin{\sqrt{x^2}}} + \frac{a_1}{b^2} + \alpha"
tokens = tokenise_latex(expr)
ast = parse(tokens)
pprint.pprint(ast)
