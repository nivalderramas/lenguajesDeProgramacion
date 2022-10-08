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