import re

VARS_REGEX = "(([a-z]|[A-Z])+(_|[0-9])*)+"
STRING_REGEX = (
    r"""(?=["])(?:"[^"\\]*(?:\\[\s\S][^"\\]*)*"|'[^'\\]*(?:\\[\s\S][^'\\]*)*)"""
)
COMMENT_REGEX = r"//.*"
INT_REGEX = r"[0-9]+"
FLOAT_REGEX = r"\d+\.\d+"

regex = {
    VARS_REGEX: "id",
    COMMENT_REGEX: "comment",
    STRING_REGEX: "str",
    INT_REGEX: "integer",
    FLOAT_REGEX: "float",
}
operators = {
    "=": "assign",
    ".": "period",
    ",": "comma",
    ";": "semicolon",
    "]": "closing_bra",
    "[": "opening_bra",
    ")": "closing_par",
    "(": "opening_par",
    "+": "plus",
    "-": "minus",
    "*": "times",
    "/": "div",
    "%": "mod",
    "==": "equal",
    "!=": "neq",
    "<": "less",
    "<=": "leq",
    ">": "greater",
    ">=": "geq",
    "?": "question_mark",
}

reserved_words = {
    "Get",
    "next",
    "input",
    "Put",
    "to",
    "output",
    "if",
    "elseif",
    "else",
    "while",
    "for",
    "integer",
    "float",
    "array",
    "Function",
    "returns",
    "SquareRoot",
    "RaiseToPower",
    "AbsoluteValue",
    "RandomNumber",
    "SeedRandomNumbers",
    "with",
    "decimal",
    "places",
    "size",
    "Main",
    "or",
    "and",
    "nothing",
    "not",
    "evaluates",
}

class Token:
    def __init__(self, row, column, lexema="", token_id=None):
        self.row = row
        self.column = column
        self.lexema = lexema
        self.token_id = token_id

    def add_lexema(self, c):
        self.lexema += c

    def edit_id(self, token_id):
        self.token_id = token_id

    def __str__(self):
        if self.token_id == None:
            return (
                "<" + self.lexema + "," + str(self.row) + "," + str(self.column) + ">"
            )
        elif self.lexema in operators:
            return (
                "<"
                + "tkn_"
                + self.token_id
                + ","
                + str(self.row)
                + ","
                + str(self.column)
                + ">"
            )
        else:
            id_tkn = self.token_id
            if id_tkn != "id":
                id_tkn = "tkn_" + id_tkn
            return (
                "<"
                + id_tkn
                + ","
                + self.lexema
                + ","
                + str(self.row)
                + ","
                + str(self.column)
                + ">"
            )


# Try to create a new token using the provided regex
# returns the created token
def try_regex(token, REGEX):
    if not is_begin_of_line and REGEX == COMMENT_REGEX:
        return False
    word = token[0]
    row = token[1]
    col = token[2]
    reg = re.compile(REGEX)
    result = reg.match(word)
    name = regex[REGEX]
    if result == None:
        return False
    word_result = str(result[0])
    if word != word_result:
        return False
    else:
        if REGEX == STRING_REGEX:
            word = word[1:-1]
        tkn = Token(row, col, word, name)
        return tkn


def match(token):
    word = token[0]
    row = token[1]
    col = token[2]
    # try reserved word
    if word in reserved_words:
        tkn = Token(row, col, word)
        return tkn
    # try operator
    if word in operators:
        tkn = Token(row, col, word, operators[word])
        return tkn
    # try COMMENT_REGEX
    tkn = try_regex(token, COMMENT_REGEX)
    if tkn != False:
        return tkn
    # try string
    tkn = try_regex(token, STRING_REGEX)
    if tkn != False:
        return tkn
    # try id
    tkn = try_regex(token, VARS_REGEX)
    if tkn != False:
        return tkn
    # try int
    tkn = try_regex(token, INT_REGEX)
    if tkn != False:
        return tkn
    # try float
    tkn = try_regex(token, FLOAT_REGEX)
    if tkn != False:
        return tkn
    return False


def solve(line, row, col):
    delta = len(line) - len(line.lstrip(" "))
    line = line.lstrip(" ")
    i = len(line)
    while i > 0:
        left_part = line[:i]
        right_part = line[i:]
        ans = match((left_part, row, col + 1 + delta))
        if ans != False:
            if ans.token_id != "comment":
                print(ans)
            # print("match",left_part,":",len(left_part),"D",delta)
            return (right_part, row, col + len(left_part) + delta)
        i -= 1
    ##TODO implement error
    return (False, row, col + 1 + delta)




def run():
    stack = []
    row = 0
    col = 0
    is_begin_of_line = True
    error = False
    while True:
        line = ""
        try:
            line = input().rstrip()
            is_begin_of_line = True
            row += 1
            col = 0
            if line == "":
                continue
        except EOFError:
            break
        while line != False:
            line, row, col = solve(line, row, col)
            is_begin_of_line = False
            if line == False:
                print(">>> Error lexico (linea: {0}, posicion: {1})".format(row, col))
                error = True
                break
            if line == "":
                break
        if error:
            break

