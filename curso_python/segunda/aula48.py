"""
Listas em Python
Tipo list - Mutável
Suporta vários valores de qualquer tipo
Conchecimentos reutilizáveis - indices e fatiamento
Métodos úteis: append, insert, pop, del, clear, extend,
"""
#........01234
#........-54321

string = 'ABCDE'  # 5 caracteres
#print(boll([])) # false
# print(listaa, type(lista))

#........0....1......2............3....4
#.......-5...-4.....-3...........-2...-1
lista = [123, True, 'Ivan Lopes', 1.2, []]
lista[-3] = 'Arthur'
print(lista)
print(lista[2], type(lista[2]))
