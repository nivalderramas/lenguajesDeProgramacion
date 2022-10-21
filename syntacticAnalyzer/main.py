import sys
import copy
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
  "str": "_TKN_STRING",
}
type_translation_inverse = {
  "_TKN_INT": "integer_value",
  "_TKN_FLOAT": "float_value",
  "_TKN_ID": "id",
  "_TKN_STRING": "string_literal",
  "$": "EOF",
  '$': "EOF",
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
    "Get",#
    "next",#
    "input",#
    "Put",#
    "to",#
    "output",#
    "if",#
    "elseif",#
    "else",#
    "while",#
    "for",#
    "integer",#
    "float",#
    "array",#
    "Function",#
    "returns",#
    "size",#
    "Main",#
    "or",#
    "and",#
    "nothing",#
    "not",#
    "SeedRandomNumbers",#
    "AbsoluteValue",#
    "SquareRoot",#
    "RaiseToPower",#
    "RandomNumber",#
    "with",#
    "decimal",#
    "places",#
}

#function that insert element in the set of the given key and creates the set if it doesn't exist
def insert_in_set(dictionary, key, element):
  if key in dictionary:
    dictionary[key].add(element)
  else:
    dictionary[key] = {element}
  
#function that updates a set if the key exists and creates it if it doesn't
def update_set(dictionary, key, element):
  if key in dictionary:
    dictionary[key].update(element)
  else:
    dictionary[key] = element

def is_terminal(symbol, grammar):
  return symbol not in grammar


def is_contained(A, B, grammar):
  # Check if A is contained in B
  for rule in grammar[B]:
    if A in rule:
      return True
  return False
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


def match_regex(token):
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
        ans = match_regex((left_part, row, col + 1 + delta))
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
columnEND = -1
rowEND = -1
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
        columnEND = 1
        rowEND = row + 1
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
INICIAL = 'INICIAL'
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
grammar[INICIAL] = [
  ('FUNCTION_INICIAL',END),
  ('CODEBLOCK',END),
]
grammar['FUNCTION_INICIAL'] = [
  #('Function','FUNC_DEF','FUNCTION_INICIAL','MAIN_DEF',END),
  ('Function','INICIAL_MAIN_VS_ID'),
]
grammar['FUNCTION_NO_INICIAL'] = [
  #('Function','FUNC_DEF','FUNCTION_INICIAL','MAIN_DEF',END),
  ('Function','MAIN_VS_ID'),
]
grammar['INICIAL_MAIN_VS_ID'] = [
  ('_TKN_ID','FUNC_DEF'),
]
grammar['MAIN_VS_ID'] = [
  ('_TKN_ID','FUNC_DEF'),
  ('MAIN_DEF',),
]
grammar['FUNC_DEF'] = [
  ('(','PARAMS_DEF',')','returns', 'FUNC_DEF_RETURNS', 'CODEBLOCK','Function','MAIN_VS_ID'),
]
grammar['MAIN_DEF'] = [
  ('Main','(',')','returns','nothing','CODEBLOCK'),
]
grammar['FUNC_DEF_RETURNS'] = [
  ('integer','FUNC_DEF_RETURNS_SUFFIX'),
  ('float','FUNC_DEF_RETURNS_SUFFIX'),
  ('nothing',),
]
grammar['FUNC_DEF_RETURNS_SUFFIX'] = [
  ('array','(','TERM_NEW_ARRAY',')','_TKN_ID'),
  ('_TKN_ID',),
  (E,),
]
grammar['PARAMS_DEF'] = [
  ('float','_TKN_ID','PARAMS_SUFFIX_DEF'),
  ('integer','_TKN_ID','PARAMS_SUFFIX_DEF'),
  (E,),
]
grammar['PARAMS_DEF_NON_EMPTY'] = [
  ('float','_TKN_ID','PARAMS_SUFFIX_DEF'),
  ('integer','_TKN_ID','PARAMS_SUFFIX_DEF'),
]
grammar['PARAMS_SUFFIX_DEF'] = [
  (',','PARAMS_DEF_NON_EMPTY',),
  (E,),
]
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
    ('%', 'OPERACION'),
    (E,),
  ]
grammar['TERM'] = [
    ('_TKN_INT',),
    ('_TKN_ID','ID_SUFFIX'), #Suffix might be "" for id, [] for array, () for function
    ('_TKN_FLOAT',),
    ('RandomNumber','(','OPERACION', ',' ,'OPERACION',')'),
    ('AbsoluteValue','(','OPERACION',')'),
    ('SquareRoot','(','OPERACION',')'),
    ('RaiseToPower','(','OPERACION', ',' ,'OPERACION',')'),
]
grammar['TERM_NEW_ARRAY'] = [
  ('_TKN_INT',),
  ('?',),
]
grammar['SIGNO'] = [
    ('+',),
    ('-',),
]
grammar['ID_SUFFIX'] = [
  ('ARRAY_LOC',),
  ('FUNCTION_CALL',),
  ('.','size'),
  (E,),
]
grammar['ARRAY_LOC'] = [
  ('[', 'OPERACION', ']'),
]
grammar["FUNCTION_CALL"] = [
  ('(', 'PARAMS', ')'),
]
grammar['PARAMS'] = [
  ('OPERACION', 'PARAMS_SUFFIX'),
  (E,),
]
grammar['PARAMS_SUFFIX'] = [
  (',', 'PARAMS'),
  (E,),
]

grammar['ID_PREFIJO_CODEBLOCK'] = [
  ('_TKN_ID','ID_SUFIJO_CODEBLOCK'),
]
grammar['ID_SUFIJO_CODEBLOCK'] = [
  ('=','OPERACION_VS_INPUT'),
  ('[','OPERACION',']','=','OPERACION_VS_INPUT'),
  ('(','PARAMS',')'),
  ('.','size','=','OPERACION_VS_INPUT'),
]
grammar['OPERACION_VS_INPUT'] = [
  ('Get','next','input'),
  ('OPERACION',),
]
grammar['PUT_PRECISION']=[
  ('with','OPERACION','decimal','places'),
  (E,),
]
grammar['CODEBLOCK'] = [
  ('DECLARACION_TYPE','NON_FIRST_CODEBLOCK'),
  ('ID_PREFIJO_CODEBLOCK','NON_FIRST_CODEBLOCK'),
  ('Put','PUT_SUFFIX','to', 'output','PUT_PRECISION','NON_FIRST_CODEBLOCK'),
  ('FOR','NON_FIRST_CODEBLOCK'),
  ('WHILE','NON_FIRST_CODEBLOCK'),
  ('IF','NON_FIRST_CODEBLOCK'),
  ('SeedRandomNumbers','(','OPERACION',')','NON_FIRST_CODEBLOCK'),
  #('BUILTINS',),
]
grammar['NON_FIRST_CODEBLOCK'] = [
  ('DECLARACION_TYPE','NON_FIRST_CODEBLOCK'),
  ('ID_PREFIJO_CODEBLOCK','NON_FIRST_CODEBLOCK'),
  ('Put','PUT_SUFFIX','to', 'output','PUT_PRECISION','NON_FIRST_CODEBLOCK'),
  ('FOR','NON_FIRST_CODEBLOCK'),
  ('WHILE','NON_FIRST_CODEBLOCK'),
  ('IF','NON_FIRST_CODEBLOCK'),
  ('SeedRandomNumbers','(','OPERACION',')','NON_FIRST_CODEBLOCK'),
  #('BUILTINS',),
  (E,),
]
grammar['FOR'] = [
  ('for','ASIGNACION',';','PRE_LOPERACION',';','ASIGNACION','CODEBLOCK'),
]
grammar['WHILE'] = [
  ('while','PRE_LOPERACION','CODEBLOCK'),
]
grammar['IF'] = [
  ('if','PRE_LOPERACION','CODEBLOCK','ELSEIF','ELSE'),
  ('if','(','PRE_LOPERACION',')','CODEBLOCK','ELSEIF','ELSE'),
]
grammar['ELSEIF'] = [
  ('elseif','PRE_LOPERACION','CODEBLOCK','ELSEIF'),
  (E,),
]
grammar['ELSE'] = [
  ('else','CODEBLOCK'),
  (E,),
]
grammar['PUT_SUFFIX'] = [
  #('_TKN_ID',('PUT_SUFFIX_ID_ARRAY')), #TODO array
  ('_TKN_STRING',),
  ('OPERACION',),
]
grammar['PUT_SUFFIX_ID_ARRAY'] = [
  ('[','OPERACION',']'),
  (E,),
  ]
grammar['DECLARACION_TYPE'] = [
  ('float','DECLARACION',),
  ('integer','DECLARACION'),
]
grammar['DECLARACION'] = [
  ('array','(','TERM_NEW_ARRAY',')','_TKN_ID'),
  ('_TKN_ID',),
]
grammar['ASIGNACION'] = [
  ('_TKN_ID','ASIGNACION_ID_SUFIJO'), #Todo array
]
grammar['ASIGNACION_ID_SUFIJO'] = [
  ('[','OPERACION',']','=','ASIGNACION_SUFFIX'),
  ('.','size','=','ASIGNACION_SUFFIX'),
  ('=','ASIGNACION_SUFFIX'),
]
grammar['ASIGNACION_SUFFIX'] = [
  ('OPERACION',),
  ('Get','next','input'),
]
grammar['PRE_LOPERACION'] = [
  ('not','(','LOPERACION',')'),
  ('LOPERACION',),
]
grammar['LOPERACION'] = [
  ('(','PRE_LOPERACION',')','LOPERADOR','LANIDADOR'),
  ('SIGNO','PRE_LOPERACION','LANIDADOR'),
  ('TERM','LOPERADOR','LANIDADOR'),
]
grammar['LANIDADOR'] = [
  ('and','PRE_LOPERACION'),
  ('or','PRE_LOPERACION'),
  (E,),
]
grammar['LOPERADOR'] = [
  ('==','PRE_LOPERACION'),
  ('!=','PRE_LOPERACION'),
  ('==','PRE_LOPERACION'),
  ('<' ,'PRE_LOPERACION'),
  ('>' ,'PRE_LOPERACION'),
  ('?' ,'PRE_LOPERACION'),
  ('>=','PRE_LOPERACION'),
  ('<=','PRE_LOPERACION'),
  ('*', 'PRE_LOPERACION'),
  ('+', 'PRE_LOPERACION'),
  ('-', 'PRE_LOPERACION'),
  ('/', 'PRE_LOPERACION'),
  ('%', 'PRE_LOPERACION'),
  (E,),
]

primeros = {v:set() for v in grammar}
siguientes = {}
prediccion = {}

def finish():
  print("El analisis sintactico ha finalizado exitosamente.")
  sys.exit()

def syntax_error(found, required):
  required = required.difference({E})
  required_str = ""
  required = list(required)
  aux_list = []
  aux_dict = {}
  for item in required:
    if item in operators:
      aux_list.append("tkn_"+operators[item])
      aux_dict["tkn_"+operators[item]] = item
    elif item in type_translation_inverse:
      aux_list.append(type_translation_inverse[item])
      aux_dict[type_translation_inverse[item]] = item
    else:
      aux_list.append(item.lower())
      aux_dict[item.lower()] = item
  #print("aux",aux_list)
  aux_list.sort()
  required = []
  for item in aux_list:
    required.append(aux_dict[item])
  if found == END:
    found = "final de archivo"
  for r in required:
    if r in type_translation_inverse:
      required_str += '"'+type_translation_inverse[r] + '", '
    else:
      required_str += '"'+r + '", '
  required_str = required_str[:-2]
  required_str += "."
  if len(tokens) != 0:
    print('<'+str(tokens[0].row)+':'+str(tokens[0].column)+'>','Error sintactico: se encontro: "'+str(found)+'"; se esperaba:',required_str )
  else:
    print('<'+str(rowEND)+':'+str(columnEND)+'> Error sintactico: se encontro '+str(found)+'; se esperaba:',required_str )
  sys.exit()

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

def get_token():
  if(len(tokens) == 0):
    token = END
    token_id = END
  else:
    token = tokens[0].lexema if len(tokens)>0 else ""
    if tokens[0].token_id in type_translation:
      token_id = type_translation[tokens[0].token_id]
    elif token in operators:
      token_id = operators[token]
    else:
      token_id = token
  return token, token_id


#Function that matches the whole grammar and raise the error if it is not valid with the corresponding expected values
def match_terminal2(token,token_id,waited_token, expected_tokens = set()):
  #TODO END of file
  #print("token",token,"token_id",token_id,"se esperaba",waited_token,"y ademas",expected_tokens)
  error = False
  if token == waited_token or token_id == waited_token:
    #print("matched **correctly**", waited_token, "con", token)
    next_token()
    return False, set()
  else:
    return True, expected_tokens.union({waited_token})

def match_program(non_terminal, expected_tokens):
  token, token_id = get_token()
  error = False
  matched = False
  #Find the rule to apply
  #print("Matching non terminal", non_terminal,"con TOKEN",token,token_id,"expected",expected_tokens)
  for rule in grammar[non_terminal]:
    if token in prediccion[(non_terminal, rule)] or token_id in prediccion[(non_terminal, rule)] or rule==(E,):
      matched = True
      if rule == (E,):
        #Si matchea con E, entonces agregamos lo que se podía esperar y retornamos para seguir el proceso
        expected_tokens = expected_tokens.union(primeros[non_terminal]).difference({E})
        #print("matchea con E",expected_tokens, "-----------",primeros[non_terminal])
        return False, expected_tokens
      for symbol in rule:
        if is_terminal(symbol, grammar):
          #print("non terminal",non_terminal,"llama a terminal",symbol)
          error, expected_tokens = match_terminal2(token,token_id,symbol, expected_tokens)
          token, token_id = get_token()
          #print("se devuelve el terminal",symbol,"expected",expected_tokens," sigo en ",non_terminal)
        else:
          #print("non terminal",non_terminal,"llama a non terminal",symbol)
          error, expected_tokens = match_program(symbol,expected_tokens)
          token, token_id = get_token()
          #print("se devuelve",symbol,"con error",error,"expected_tokens",expected_tokens)
        if error:
          return error, expected_tokens
      break
  if not matched:
    #print("no matchea con nada",non_terminal,expected_tokens)
    error = True
    expected_tokens = expected_tokens.union(primeros[non_terminal])
  return error, expected_tokens

  

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
get_nexts()
get_pred()
if len(tokens) == 0:
  finish()
error, waited_tokens = match_program(INICIAL,set())
if error:
  if len(tokens) == 0:
    syntax_error(END, waited_tokens)
  else:
    syntax_error(tokens[0].lexema, waited_tokens)
else:
  finish()
