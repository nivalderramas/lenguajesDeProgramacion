line = input()
tokens = line.split()
oo = 1e9
symbols = {
        '=': "assign",
        '.': "period",
        ',': "comma",
        ';':"semicolon",
        ']':"closing_bra",
        '[':"opening_bra",
        ')':"closing_par",
        '(':"opening_par",
        '+':"plus",
        '-':"minus",
        '*':"times",
        '/':"div",
        '%':"mod",
        '==':"equal",
        '!=':"neq",
        '<':"less",
        '<=':"leq",
        '>':"greater",
        '>=':"geq",
        '?':"question_mark",
        }
reserved_word_state = 1000
else_state = 21
id_state = 99
symbol_state = 199
error = -oo

def isValidCharForId(c):
    if (ord(c) >=  97 and ord(c)<=122) or (ord(c)>=65 and ord(c) <=90) or c=='_':
        return True
    return False

def afd(c, state):
    match state:
        case 0:
            if c == 'F':
                return 1
            if c == 'f':
                return 8
            if c == 'i':
                return 13
            if c == 'e':
                return 18
            if c == 'G':
                return 23
            if c == 'P':
                return 24
            if c == 'a':
                return 25
            if isValidCharForId(c):
                return id_state
            if c in symbols:
                return symbol_state
            return error
        case 199: # SYMBOL STATE
            if c in symbols:
                return symbol_state
            return error
        case 1:
            if c == 'u':
                return 2
            if isValidCharForId(c):
                return id_state
            return -oo
        case 2:
            if c == 'n':
                return 3
            if isValidCharForId(c):
                return id_state
            return -oo
        case 3:
            if c == 'c':
                return 4
            if isValidCharForId(c):
                return id_state
            return -oo
        case 4:
            if c == 't':
                return 5
            if isValidCharForId(c):
                return id_state
            return -oo
        case 5:
            if c == 'i':
                return 6
            if isValidCharForId(c):
                return id_state
            return -oo
        case 6:
            if c == 'o':
                return 7
            if isValidCharForId(c):
                return id_state
            return -oo
        case 7:
            if c == 'n':
                return  reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case 8:
            if c == 'o':
                return 9
            if c == 'l':
                return 10
            if isValidCharForId(c):
                return id_state
            return -oo
        case 9:
            if c == 'r':
                return reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case 10:
            if c == 'o':
                return 11 
            if isValidCharForId(c):
                return id_state
            return -oo
        case 11:
            if c == 'a':
                return 12
            if isValidCharForId(c):
                return id_state
            return -oo
        case 12:
            if c == 't':
                return reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case 13:
            if c == 'n':
                return 14 
            if c == 'f':
                return reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case 14:
            if c == 't':
                return 15
            if isValidCharForId(c):
                return id_state
            return -oo
        case 15:
            if c == 'e':
                return 16
            if isValidCharForId(c):
                return id_state
            return -oo
        case 16:
            if c == 'g':
                return 17
            if isValidCharForId(c):
                return id_state
            return -oo
        case 17:
            if c == 'e':
                return 9
            if isValidCharForId(c):
                return id_state
            return -oo
        case 18:
            if c == 'l':
                return 19
            if isValidCharForId(c):
                return id_state
            return -oo
        case 19:
            if c == 's':
                return 20
            if isValidCharForId(c):
                return id_state
            return -oo
        case 20: #ELSE STATE
            if c == 'e':
                return 21
            if isValidCharForId(c):
                return id_state
            return -oo
        case 21:
            if c == 'i':
                return 22
            if isValidCharForId(c):
                return id_state
            return -oo
        case 22:
            if c == 'f':
                return reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case 23:
            if c == 'e':
                return 12
            if isValidCharForId(c):
                return id_state
            return -oo
        case 24:
            if c == 'u':
                return 12
            if isValidCharForId(c):
                return id_state
            return -oo
        case 25:
            if c == 'r':
                return 26
            if isValidCharForId(c):
                return id_state
            return -oo
        case 26:
            if c == 'r':
                return 27
            if isValidCharForId(c):
                return id_state
            return -oo
        case 27:
            if c == 'a':
                return 28
            if isValidCharForId(c):
                return id_state
            return -oo
        case 28:
            if c == 'y':
                return reserved_word_state
            if isValidCharForId(c):
                return id_state
            return -oo
        case _:
            return "Error"

state = 0
for token in tokens:
    for c in token:
        state = afd(c,state)
if(state == reserved_word_state or state == else_state):
    print("reservada")
elif(state == id_state):
    print("id")
elif(state == symbol_state):
    print("symbol")
else:
    print("error")
