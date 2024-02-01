"""
Enumerate - enumera iteráveis (indices)
"""

lista = ['Maria', 'Helena', 'Luiz']
lista.append('João')

# lista_enumerada = enumerate(lista)

# for indice, nome in enumerate(lista):
#     print(indice, nome)

for item in enumerate(lista):
    indice, nome = item
    print(indice, nome)

