from lib2to3.pgen2.grammar import Grammar
import copy
import pprint
from utils import *
import re
tokens = []
VARS_REGEX = "(([a-z]|[A-Z])+(_|[0-9])*)+"
STRING_REGEX = (
    r"""(?=["])(?:"[^"\\]*(?:\\[\s\S][^"\\]*)*"|'[^'\\]*(?:\\[\s\S][^'\\]*)*)"""
)
COMMENT_REGEX = r"//.*"
INT_REGEX = r"[0-9]+"
FLOAT_REGEX = r"\d+\.\d+"

type_translation = {
  "integer": "_TKN_INT",
  "float": "_TKN_FLOAT",
  "id": "_TKN_ID",
}

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
                tokens.append(ans)
                #print(ans)
            # print("match",left_part,":",len(left_part),"D",delta)
            return (right_part, row, col + len(left_part) + delta)
        i -= 1
    ##TODO implement error
    return (False, row, col + 1 + delta)




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

####################################### FINAL ANALISIS LEXICO ######################
####################################### FINAL ANALISIS LEXICO ######################
####################################### FINAL ANALISIS LEXICO ######################
####################################### FINAL ANALISIS LEXICO ######################
#for token in tokens:
#  print(token.token_id)
INICIAL = 'OPERACION'
E = ""
END  = "$"
grammar = {
  'A': [('B', 'uno'), 
        ('dos',)
      ],
  'B': [('tres',),
        ('cuatro', 'A'),
      ],
  }

grammar = {}
#arithmetical grammar
grammar['OPERACION'] = [
    ('(', 'OPERACION', ')', 'OPERADOR'),
    ('SIGNO', 'OPERACION'),
    ('TERM', 'OPERADOR'),
  ]
grammar['OPERADOR'] = [
    ('*', 'OPERACION'),
    ('+', 'OPERACION'),
    ('-', 'OPERACION'),
    ('/', 'OPERACION'),
    (E,),
  ]
grammar['TERM'] = [
    ('_TKN_ID',),
    ('_TKN_INT',),
    ('_TKN_FLOAT',),
]
grammar['SIGNO'] = [
    ('+',),
    ('-',),
    ('*',),
    ('/',),
]


primeros = {v:set() for v in grammar}
siguientes = {}
prediccion = {}

# Rule is a list of symbols, meaning the right part of a rule
def process_rule(rule):
  if(rule in primeros and len(primeros[rule]) != 0):
    return
  a1 = rule[0]
  if isinstance(rule, str):
    a1 = rule
  if ''.join(rule) == E:
    insert_in_set(primeros, rule, E)
  else:
    if is_terminal(a1, grammar):
      insert_in_set(primeros, rule, a1)
    else:
      get_firsts(a1)
      res = primeros[a1].difference({E})
      update_set(primeros, rule, res)
    if a1 in primeros and E in primeros[a1]:
      if rule == a1:
        insert_in_set(primeros, rule, E)
      else:
        if len(rule) > 1:
          process_rule(rule[1:])
          primeros[rule].update(primeros[rule[1:]])
    if not is_terminal(a1, grammar):
      for subrule in grammar[a1]:
        process_rule(subrule)
        update_set(primeros, subrule, primeros[subrule])


# function that creates the firsts set of every non-terminal symbol of the given grammar
def get_firsts(non_terminal_symbol):
  if(len(primeros[non_terminal_symbol]) != 0):
    return
  #check for every possible rule for the given non terminal
  primeros[non_terminal_symbol] = set()
  for rule in grammar[non_terminal_symbol]:
    #print("pasa",non_terminal_symbol)
    process_rule(rule)
    #PRIMEROS[non_terminal_symbol].update(PRIMEROS[rule])
    update_set(primeros, non_terminal_symbol, primeros[rule])


def get_nexts():
  siguientes[INICIAL] = {END}
  while(True):
    preSiguientes = copy.deepcopy(siguientes)
    for non_terminal in grammar:
      A = non_terminal
      for non_terminal_b in grammar:
        B = non_terminal_b
        for rule in grammar[B]:
          #print(type(rule))
          for i in range(len(rule)):
            if rule[i] == A:
              #B
              if i == len(rule)-1:
                if A != B:
                  update_set(siguientes, A, siguientes[B])
              else:
                #print("nont:",non_terminal," | B:",B," | rule:",rule," | i",i, " | rule[i]:",rule[i])
                if is_terminal(rule[i+1], grammar):
                  #print(rule[i+1])
                  insert_in_set(siguientes, A, rule[i+1])
                else:
                  #print("else")
                  update_set(siguientes, A, primeros[rule[i+1]].difference({E}))
                  if E in primeros[rule[i+1]]:
                    if i == len(rule)-2:
                      update_set(siguientes, A, siguientes[B])
                    else:
                      update_set(siguientes, A, siguientes[rule[i+2]]) 
    if siguientes == preSiguientes:
      break

# Function that creates the prediction table for the given grammar
def get_pred():
  for non_terminal in grammar:
    for rule in grammar[non_terminal]:
      if E in primeros[rule]:
        res = (primeros[rule].difference({E})).union(siguientes[non_terminal])
      else:
        res = primeros[rule]
      prediccion[(non_terminal, rule)] = res


def next_token():
  if len(tokens) == 0:
    return
  tokens.pop(0)
  return

#Decies if the symbol that is being readed is valid
def match(waited_token):
  print("Matcheando terminal:", waited_token, "con token:", tokens[0].token_id)
  token = tokens[0]
  token = token.lexema
  if tokens[0].token_id in type_translation:
    token_id = type_translation[tokens[0].token_id]
  #elif tokens[0].token_id in operators:
  #  token_id = operators[tokens[0].token_id]
  else:
    token_id = ""
  if token == waited_token or token_id == waited_token:
    print("se matcheo", token,"********"*5, waited_token)
    if waited_token != "":
      next_token()
  else:
    message = "Syntax error, se esperarba " + waited_token + "pero se encontro " + token
    raise SyntaxError (message)


# Function that will match the appropriate rule for the given input
def match_rule(non_terminal):
  print("Matcheando regla", non_terminal)
  token = tokens[0].lexema
  if tokens[0].token_id in type_translation:
    token_id = type_translation[tokens[0].token_id]
  else:
    token_id = ""
  matched = False
  for rule in grammar[non_terminal]:
    if token in prediccion[(non_terminal, rule)] or token_id in prediccion[(non_terminal, rule)]: #means that we must apply this rule
      matched = True
      for symbol in rule:
        if is_terminal(symbol, grammar):
          print("probar matchear con:  ", non_terminal,'->', rule)
          match(symbol)
        else:
          match_rule(symbol)
  if not matched:
    message = "Error de sintaxis, token not matched " + token
    raise SyntaxError (message)


for k in grammar:
  primeros[k] = set()
  siguientes[k] = set()
for k in grammar:
  get_firsts(k)

#primeros['A'] = primeros['A'] - set(E)
newPrimeros = {}
for k in primeros:
  if k in grammar:
    newPrimeros[k] = primeros[k]
#primeros = newPrimeros
get_nexts()
get_pred()
pp = pprint.PrettyPrinter(width=41, compact=True)
#print("Prediction sets:")
#pp.pprint(prediccion)
#Start matching
token = tokens[0]
match_rule(INICIAL)
print("Analisis sintáctico finalizado exitosamente")
