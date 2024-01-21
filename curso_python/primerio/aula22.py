# Operadores lógicos
# and (e) or (ou) not (não)
# or - Qualquer condição vcerdaderia avalia
# Toda a expressão como verdaderia
# Se qualquer valor for considerado falso,
# a expressão inteira será avaliada naquele valor
# São considerados falsy (que vc já viu
# 0 0.0 '' False
# Também exixte o tipo Nome que é
# usado para representar um não valor


# entrar = input('[E]ntrar [S]air: ')
# senha_digitada = input('Senha: ')

# senha_permitida = '123456'

# if entrar == 'E' and senha_digitada == senha_permitida:
#     print('entrar')
# else:
#     print('Sair')

senha = input('Senha: ') or 'Sem senha'
print(senha)