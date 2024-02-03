"""
Exercício
Peça ao usúario para digitar seu nome.
Peça ao usúario para digitar sua idade.
Se nome e idade forem digitados:
.....Exiba:
...........Seu nomo é {nome}
...........Seu nome invertido é {nome invertido}
...........Seu nome contém (ou, não) espaços
...........Seu Nome tem {n} letras
...........A primeira letra do seu nome é {letra}
...........A última letra do seu nome é {letra}
se nada or digitado em seu nome ou idade:
.....exiba "Desculpe, você deixou campos vazios."
"""

nome = input('Digite seu nome: ')
idade = input('Digite sua idade: ')

if nome and idade:
    print(f'Seu nome é: {nome}')
    print(f'Seu nome invertido é: {nome[::-1]}')   

    if ' ' in nome:
        print(f'Seu nome tem espaços')
    else:
        print(f'Seu nome não contem espaços')

    print(f'Seu nome tem {len(nome)} letras')
    
    print(f'A primeira letra do seu nome é: {nome[0]}')      
    print(f'a última letra do seu nome é: {nome[-1]} ')

else:
    print("Desculpe, você deixou campos vazios.")



