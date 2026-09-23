"""Target-1.1.3 byte-consumption model, not a runtime acceptance oracle.

Authority: main SHA b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b.
Addresses are NSO memory offsets. This parser separates literal bytes from VM
operands and records explicit C/J edges. It does not infer caller closure,
grammar equivalence, output capacity, or permission to replace a message.
"""
from dataclasses import dataclass


class Unresolved(ValueError):
    pass


@dataclass
class Field:
    kind: str
    start: int
    end: int


class Parser:
    def __init__(self, data, mapping):
        self.data, self.mapping = data, mapping
        self.i, self.fields, self.edges = 0, [], []
        self.atoms = []

    def peek(self):
        if self.i >= len(self.data):
            raise Unresolved('INPUT_EXHAUSTED')
        return self.data[self.i]

    def byte(self):
        value = self.peek()
        self.i += 1
        return value

    def atom(self, depth=0):
        start = self.i
        self._atom(depth)
        self.atoms.append((start, self.i))

    def _atom(self, depth=0):
        if depth > 40:
            raise Unresolved('EXPRESSION_DEPTH')
        b = self.byte()
        if b == 0x25 or 0x30 <= b <= 0x39:
            # 43decc: first digit (if any), then at most ten further digits.
            for _ in range(10):
                if not 0x30 <= self.peek() <= 0x39:
                    break
                self.byte()
            return
        if b != 2:
            raise Unresolved('NON_ATOM_' + hex(b))
        selector = self.byte()
        # 263848 dispatch. All known property handlers restore a <=31 lookahead.
        if not (1 <= selector <= 0x84 or selector == 0xc8):
            raise Unresolved('UNRECOGNIZED_SELECTOR_' + hex(selector))
        if self.peek() <= 31:
            return
        prop = self.byte()
        if selector == 0xc8:
            # 261770 table 75cb6e; all CFG return paths agree on expression arity.
            if prop in (0x64, 0x65, 0x8b, 0x96):
                n = 1
            elif 0x6e <= prop <= 0x91:
                n = 2
            else:
                raise Unresolved('UNRECOGNIZED_FUNCTION_PROPERTY_' + hex(prop))
            for _ in range(n):
                self.expr(depth + 1)

    def expr(self, depth=0):
        # 43e1e8: strictly left-to-right atom (03 op atom)*.
        self.atom(depth)
        while self.peek() == 3:
            self.byte()
            if self.byte() not in b'*+-/%':
                raise Unresolved('ARITHMETIC_OPERATOR')
            self.atom(depth)

    def comparison(self):
        self.expr()
        if self.peek() == 4:
            self.byte()
            if self.byte() not in b'!=<>{}':
                raise Unresolved('COMPARISON_OPERATOR')
            self.expr()

    def condition(self):
        self.comparison()
        while self.peek() == 6:
            self.byte()
            if self.byte() not in b'|&':
                raise Unresolved('BOOLEAN_OPERATOR')
            self.comparison()

    def parse(self):
        # Lexical coverage follows stored order, including non-executed branches.
        # Branch topology is retained as bytes; this is not a branch evaluator.
        while self.i < len(self.data):
            start = self.i
            b = self.byte()
            kind = 'STRUCTURE'
            if b == 1:
                sub = self.byte()
                if sub in (0x43, 0x4a):
                    target = self.byte() | self.byte() << 8
                    self.edges.append(dict(offset=start, operation='CALL' if sub == 0x43 else 'JUMP',
                                           target=f'B{target // 1000}:{target % 1000}'))
                elif sub == 0x46:
                    if self.byte() != 0x64:
                        raise Unresolved('UNRECOGNIZED_01F_PROPERTY')
                    self.expr()
                elif sub == 0x4d:
                    if self.byte() != 2:
                        raise Unresolved('ASSIGNMENT_SELECTOR_PREFIX')
                    if not 1 <= self.byte() <= 0x82:
                        raise Unresolved('ASSIGNMENT_SELECTOR')
                    self.expr()
                elif sub in (0x52, 0x53):
                    self.expr()
                else:
                    raise Unresolved('UNRECOGNIZED_01_' + hex(sub))
            elif b == 2:
                self.i = start
                self.expr()
            elif b == 5:
                if self.byte() != 5:
                    raise Unresolved('BRANCH_PREFIX')
                marker = self.byte()
                if marker not in (4, 5, 6, 7, 8, 9):
                    raise Unresolved('BRANCH_MARKER')
                if marker in (4, 9):
                    self.condition()
            elif b in (0x1a, 0x1b):
                sub = self.byte()
                if sub in (0x43, 0x56, 0x57):
                    # VM copies prefix/sub; following byte is a downstream
                    # renderer operand. Preserve it rather than call it prose.
                    if self.byte() < 0x20:
                        raise Unresolved('RENDER_OPERAND')
                elif sub not in (0x48, 0x4b, 0x6b):
                    raise Unresolved('UNREVIEWED_FONT_SUBFORM')
            elif b == 0 and not any(self.data[start:]):
                self.i = len(self.data)
            elif b in (8, 9, 10, 13):
                # Preserve line controls in exact control signature for now.
                kind = 'LAYOUT'
            elif b < 32:
                raise Unresolved('UNREVIEWED_CONTROL_' + hex(b))
            else:
                kind = 'LITERAL'
                if 0x81 <= b <= 0x9f or 0xe0 <= b <= 0xfc:
                    trail = self.byte()
                    if not (0x40 <= trail <= 0xfc and trail != 0x7f):
                        raise Unresolved('INVALID_GLYPH_TRAIL')
                    if (b << 8 | trail) not in self.mapping:
                        raise Unresolved('UNKNOWN_GLYPH')
                elif b not in self.mapping and b != 32:
                    raise Unresolved('UNKNOWN_SINGLE_GLYPH')
            if kind == 'LITERAL' and self.fields and self.fields[-1].kind == kind:
                self.fields[-1].end = self.i
            else:
                self.fields.append(Field(kind, start, self.i))
        return self


def inspect(data, mapping):
    p = Parser(data, mapping)
    error = None
    try:
        p.parse()
    except Unresolved as exc:
        error = str(exc)
    return dict(complete=error is None, error=error, stopped_at=p.i,
                fields=[vars(f) for f in p.fields], edges=p.edges,
                atoms=p.atoms,
                admission=False, runtime_verified=False)


def structural_signature(data, result, keep_layout=True):
    return [(f['kind'], data[f['start']:f['end']].hex())
            for f in result['fields']
            if f['kind'] != 'LITERAL' and (keep_layout or f['kind'] != 'LAYOUT')]
