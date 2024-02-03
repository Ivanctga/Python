"""
Faça um programa que peça ou usúario paa digitar um número,
informe se este número é par ou ímpar. Caso o usúario não digitar
um número inteiro, informe que não é um número inteiro.
"""

# entrada = input('Digite um número: ')

# if entrada.isdigit():
#     entrada_int = int(entrada)
#     par_impar = entrada_int % 2 == 0
#     par_impar_texto = 'impar'
    
#     if par_impar:
#         par_impar_texto = "par"

#     print(f'O número {entrada_int} é {par_impar_texto}')

# else:
#     print('Você não digitou um número inteiro')


entrada = input('Digite um número: ')

try:
    entrada_int = float(entrada)
    par_impar = entrada_int % 2 == 0
    par_impar_texto = 'impar'
    
    if par_impar:
        par_impar_texto = "par"

    print(f'O número {entrada_int} é {par_impar_texto}')

except:
    print('Você não digitou um número inteiro')