"""
Listas em Python
Tipo list - Mutável
Suporta vários valores de qualquer tipo
Conchecimentos reutilizáveis - indices e fatiamento
Métodos úteis: append, insert, pop, del, clear, extend,
Create Read Update Delete
Criar, ler, alterar, apagar = lista[i] (CRUD)
"""
#........0...1...2...3
lista = [10, 20, 30, 40]
# numero = lista[2]

lista.append(50)
lista.append(60)
lista.pop()
lista.append(70)
lista[2] = 300
del lista[2]
print(lista)
print(lista[2])
ultimo_valor = lista.pop()
print(lista, 'Removido,', ultimo_valor)
