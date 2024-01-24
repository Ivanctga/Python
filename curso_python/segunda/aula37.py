
# contador = 0

# while contador <= 10:
#     contador += 1
#     print(contador)

#     if contador == 4:        
#         break
# print('-------------------------------')


contador_1 = 0

while contador_1 <= 30:
    contador_1 += 1

    if contador_1 == 6:
        print('Não vou mostrar o 6.')
        continue

    if contador_1 >= 15 and contador_1 <= 20: 
        print('Não vou mostrar o', contador_1)       
        continue

    print(contador_1)

    if contador_1 == 25:
        break
print('--------------------------------------------')