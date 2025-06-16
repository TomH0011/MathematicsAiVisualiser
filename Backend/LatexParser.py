import re # import regex
from collections import deque
import pprint


# 1. Tokeniser
def tokenise_latex(expr):
    GREEK = [
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota',
        'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau',
        'upsilon', 'phi', 'chi', 'psi', 'omega'
    ]

    COMMANDS = [
                   'frac', 'sqrt', 'leq', 'geq', 'int', 'sum', 'sin', 'cos', 'tan', 'log', 'ln',
                   'lim', 'cdot', 'infty', 'to', 'neq', 'approx'
               ] + GREEK

    # Token spec with grouping
    token_spec = [
        (r'\\[a-zA-Z]+', 'COMMAND'),
        (r'{', 'LBRACE'),
        (r'}', 'RBRACE'),
        (r'[a-zA-Z]', 'VARIABLE'),
        (r'[0-9]+', 'NUMBER'),
        (r'\^', 'CARET'),
        (r'[_]', 'UNDERSCORE'),
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


# 2. Parser helpers
def parse(tokens):
    tokens = deque(tokens)

    def parse_expr():
        if not tokens:
            return None
        kind, val = tokens.popleft()

        if kind == 'COMMAND':
            if val == r'\frac':
                return {
                    'type': 'fraction',
                    'numerator': parse_braced(),
                    'denominator': parse_braced()
                }
            elif val == r'\sqrt':
                return {
                    'type': 'sqrt',
                    'value': parse_braced()
                }

        elif kind == 'VARIABLE':
            return {'type': 'var', 'value': val}

        elif kind == 'NUMBER':
            return {'type': 'number', 'value': int(val)}


        elif kind == 'CARET':
            exponent = parse_expr()
            return {'type': 'power', 'base': {'type': 'unknown', 'value': '?'}, 'exponent': exponent}

        elif kind == 'OPERATOR':
            return {'type': 'operator', 'value': val}

        return {'type': 'unknown', 'value': val}

    def parse_braced():
        kind, val = tokens.popleft()
        assert kind == 'LBRACE', f"Expected '{{', got {val}"

        contents = []
        while tokens and tokens[0][0] != 'RBRACE':
            contents.append(parse_expr())

        tokens.popleft()
        return contents

    ast = []
    while tokens:
        ast.append(parse_expr())
    return ast


# 3. Example usage
expr = r"\frac{a}{b} + \sqrt{x^2}"
tokens = tokenise_latex(expr)
ast = parse(tokens)
pprint.pprint(ast)
