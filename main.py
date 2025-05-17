from Parser import Parser

P = Parser('corpus/')
P.traverse()

for name in P.documents:
  print(P.get_abstract(name))