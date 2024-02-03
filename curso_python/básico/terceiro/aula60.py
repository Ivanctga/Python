import re
import sys

# cpf_enviado = '746.824.890-70' \
#     .replace('.','')\
#     .replace(' ','')\
#     .replace('-','')

entrada = input('CPF [746.824.890-70]: ')

cpf_enviado = re.sub(r'[^0-9]','', entrada)

entrada_e_sequecial = entrada == entrada[0] * len(entrada)

if entrada_e_sequecial:
    print('Você enviou dados sequenciais.')
    sys.exit()

print('CPF enviado ',cpf_enviado)
print()
    
nove_digitos = cpf_enviado[:9]
contador_regressivo_1 = 10

resultado_digito_1 = 0

for digito in nove_digitos:
    resultado_digito_1 += int(digito) * contador_regressivo_1
    contador_regressivo_1 -= 1

digito_1 = (resultado_digito_1 * 10 ) % 11
digito_1 = digito_1 if digito_1 <= 9 else 0

dez_digito = nove_digitos + str(digito_1)
contador_regressivo_2 = 11

resultado_digito_2 = 0 

for digito in dez_digito:
    resultado_digito_2 += int(digito) * contador_regressivo_2
    contador_regressivo_2 -= 1

digito_2 = (resultado_digito_2 * 10) % 11
digito_2 = digito_2 if digito_2 <= 9 else 0

novo_cpf = f'{nove_digitos}{digito_1}{digito_2}'

if cpf_enviado == novo_cpf:
    print(f'{cpf_enviado} é valido')
else:
    print('CPF inválido')
print()




