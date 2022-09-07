line = input()
tokens = line.split()
oo = 1e9
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
    "for",
    "float",
    "size",
    "integer",
    "if",
    "elseif",
    "Get",
    "Put",
    "array",
    "Function",
    "SquareRoot",
    "RaiseToPower",
    "AbsoluteValue",
    "RandomNumber",
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
        else:
            return (
                "<" + self.token_id  + ","+ self.lexema + "," + str(self.row) + "," + str(self.column) + ">"
            )



def isalphabetic(c):
    if (ord(c) >= 97 and ord(c) <= 122) or (ord(c) >= 65 and ord(c) <= 90):
        return True
    return False

def isfloat(element):
    try:
        float(element)
    except ValueError:
        return False
    else:
        return True

def is_number_with_sign(element):
    if len(element) <= 1:
        return False
    if element[1:].isnumeric():
        return True
def is_float_with_sign(element):
    if len(element) <= 1:
        return False
    if isfloat(element[1:]):
        return True

state = 0
row, column = 1,1
for lexema in tokens:
    token = None
    if lexema in reserved_words:
        token = Token(row,column,lexema)
    elif lexema in operators:
        token = Token(row,column,lexema, operators[lexema])
    elif lexema.isnumeric():
        token = Token(row,column,lexema, "integer")
        pass
    elif isfloat(lexema):
        token = Token(row,column,lexema, "float")
        pass
    elif is_number_with_sign(lexema):
        sign = "plus"
        if lexema[0] == '-':
            sign = "minus"
        token = Token(row,column,lexema[0], sign)
        token = Token(row,column,lexema[1:], "integer")
    elif is_float_with_sign(lexema):
        sign = "plus"
        if lexema[0] == '-':
            sign = "minus"
        token = Token(row,column,lexema[0], sign)
        token = Token(row,column,lexema[1:], "float")
    else:
        token = Token(row,column,"",token_id = "id")
        for c in lexema:
            if state == 0:
                if isalphabetic(c):
                    token.add_lexema(c)
                    state = 1
                else:
                    state = -1
            elif state == 1:
                if isalphabetic(c) or c == "_":
                    token.add_lexema(c)
                    continue
                else:
                    state = -1
            if state == -1:
                break
    if state == -1:
        #TODO make error
        pass
    else:
        print(token)
    
    row += 1
    #Add the size of word and 1 cause of the space
    column += len(lexema)+ 1
