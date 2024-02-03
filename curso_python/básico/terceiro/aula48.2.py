"""
Listas em Python
Tipo list - Mutável
Suporta vários valores de qualquer tipo
Conchecimentos reutilizáveis - indices e fatiamento
Métodos úteis: 
    append - Adiciona um item ao final 
    insert - Adiciona um item no índice escolhido 
    pop - Remove do final ou do índice escolhido 
    del - Apaga um índice
    clear - Limpa a lista
    extend - Estende a lista
    + - Concaterna listas
Create Read Update Delete
Criar, ler, alterar, apagar = lista[i] (CRUD)
"""

#........0...1...2...3
lista = [10, 20, 30, 40]

lista.append(1234)
del lista[-1]
lista.insert(0, 5)
print(lista)

print('-------------------------------')

lista_a = [1, 2, 3]
lista_b = [4, 5, 6]
lista_c = lista_a + lista_b

print(lista_a, 'lista A')
print('')
print(lista_b, 'lista B')
print('')
print(lista_c, 'lista C')
print('')