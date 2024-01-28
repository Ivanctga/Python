"""
Iterável -> str, range, etc
Iterador -> quem saber entregar um valor por vez
next -> me entregue o próximo valor 
iter -> me entregue seu interador
"""
texto = 'Ivan'
# iteratador = iter(texto)

# while True:
#     try:
#         letra = next(iteratador)
#         print(letra)
#     except StopIteration:
#         break

for letra in texto:
    print(letra)

