from lib2to3.pgen2.grammar import Grammar
import copy
import pprint
from utils import *
INICIAL = 'S'
E = ""
END  = "$"
grammar = {
  'S': [
    ('A', 'uno', 'B', 'C', 'S-'),
    ('dos', 'S-',),
    (E,),
    ],
  'S-': [
    ('dos', 'S-',),
    (E,),
    ],
  'A': [
    ('B', 'C','D','A-'),
    ('A-'),
    ],
  'A-': [
    ('tres','A-'),
    (E,),
    ],
  'B': [
    ('D', 'cuatro', 'C', 'tres'),
    (E,),
    ],
  'C': [
    ('cinco', 'D', 'B'),
    ],
  'D': [
    ('seis'),
    (E,),
    ],
}
# grammar = {
#   'S': [('A', 'B'), 
#         ('HOLA', 'MUNDO')
#       ],
#   'A': [('apasd'),
#         (E,)
#       ],
#   'B': [('basas')],
#   }
# grammar = {
#   'A': [('B', 'C'), 
#         ('ant', 'A', 'all')
#       ],
#   'B': [('big', 'C'),
#         ('bus', 'A', 'boss'),
#         (E,)
#       ],
#   'C': [('cat'),
#         ('cow')
#     ],
#   }
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
          for i in range(len(rule)):
            if rule[i] == A:
              #B
              if i == len(rule)-1:
                if A != B:
                  update_set(siguientes, A, siguientes[B])
              else:
                if is_terminal(rule[i+1], grammar):
                  insert_in_set(siguientes, A, rule[i+1])
                else:
                  update_set(siguientes, A, primeros[rule[i+1]]-set(E))
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


for k in grammar:
  primeros[k] = set()
  siguientes[k] = set()
for k in grammar:
  get_firsts(k)

primeros['A'] = primeros['A'] - set(E)
newPrimeros = {}
for k in primeros:
  if k in grammar:
    newPrimeros[k] = primeros[k]
#primeros = newPrimeros
get_nexts()
get_pred()
pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(primeros)
print('*'*20)
pp.pprint(siguientes)
print('*'*20)
pp.pprint(prediccion)