from macropy.case_classes import macros, case

@case
class Point(x, y): pass

p = Point(1, 2)

print str(p) # Point(1, 2)
print p.x    # 1
print p.y    # 2
print Point(1, 2) == Point(1, 2) # True
x, y = p
print x, y # (1, 2)

from macropy.quick_lambda import macros, f, _

basetwo=f[int(_,base=2)]
print basetwo('10010')


from macropy.peg import macros, peg, cut
from macropy.quick_lambda import macros, f

def decode(x):
    x = x.decode('unicode-escape')
    try:
        return str(x)
    except:
        return x

escape_map = {
    '"': '"',
    '/': '/',
    '\\': '\\',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t'
}

"""
Sample JSON PEG grammar for reference, shameless stolen from
https://github.com/azatoth/PanPG/blob/master/grammars/JSON.peg

JSON <- S? ( Object / Array / String / True / False / Null / Number ) S?

Object <- "{"
             ( String ":" JSON ( "," String ":" JSON )*
             / S? )
         "}"

Array <- "["
            ( JSON ( "," JSON )*
            / S? )
        "]"

String <- S? ["] ( [^ " \ U+0000-U+001F ] / Escape )* ["] S?

Escape <- [\] ( [ " / \ b f n r t ] / UnicodeEscape )

UnicodeEscape <- "u" [0-9A-Fa-f]{4}

True <- "true"
False <- "false"
Null <- "null"

Number <- Minus? IntegralPart fractPart? expPart?

Minus <- "-"
IntegralPart <- "0" / [1-9] [0-9]*
fractPart <- "." [0-9]+
expPart <- ( "e" / "E" ) ( "+" / "-" )? [0-9]+
S <- [ U+0009 U+000A U+000D U+0020 ]+
"""
with peg:
        json_doc = (space, (obj | array), space) // f[_[1]]
        json_exp = (space, (obj | array | string | true | false | null | number), space) // f[_[1]]

        pair = (string is k, space, ':', cut, json_exp is v) >> (k, v)
        obj = ('{', cut, pair.rep_with(",") // dict, space, '}') // f[_[1]]
        array = ('[', cut, json_exp.rep_with(","), space, ']') // f[_[1]]

        string = (space, '"', (r'[^"\\\t\n]'.r | escape | unicode_escape).rep.join is body, '"') >> "".join(body)
        escape = ('\\', ('"' | '/' | '\\' | 'b' | 'f' | 'n' | 'r' | 't') // escape_map.get) // f[_[1]]
        unicode_escape = ('\\', 'u', ('[0-9A-Fa-f]'.r * 4).join).join // decode

        true = 'true' >> True
        false = 'false' >> False
        null = 'null' >> None

        number = decimal | integer
        integer = ('-'.opt, integral).join // int
        decimal = ('-'.opt, integral, ((fract, exp).join) | fract | exp).join // float

        integral = '0' | '[1-9][0-9]*'.r
        fract = ('.', '[0-9]+'.r).join
        exp = (('e' | 'E'), ('+' | '-').opt, "[0-9]+".r).join

        space = '\s*'.r