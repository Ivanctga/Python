texto = 'Python'

# i = 0 
# tamanho_string = len(texto)

# while i < tamanho_string:
#     print(texto[i], i)

#     i += 1

novo_texto = ''
for letra in texto:
    novo_texto += f'*{letra}'
    print(letra)
print(novo_texto + '*')



print('----------------------------------')

senha_salva = '123456'
senha_digitada = ''
repeticoes = 0 

while senha_salva != senha_digitada:
    senha_digitada = input(f'Sua senha ({repeticoes}x): ')

    repeticoes += 1

print(repeticoes)
print('Aquela laço acima pode ter repetições infinitas')