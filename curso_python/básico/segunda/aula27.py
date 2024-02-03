"""
Fatiamento de strings
012345678
olá mundo
-987654321
Fatiamento [i:f:p] [::]
Obs.: a função len retorna a qtd
de caracteres da str
"""

variavel = 'Olá mundo'

print(variavel[4:]) 
print(variavel[4:7])
print(variavel[:5])
print(variavel[0:5])
print(variavel[-8:-2])

print(len(variavel))
print(variavel[::-1])