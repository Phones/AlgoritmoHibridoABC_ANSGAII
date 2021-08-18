import os
from time import sleep

caminho = os.getcwd() + "/Plots/"
lista = os.listdir(caminho)

valor_final = 99999999999999.0
caminho_final = ''

for name in lista:
	if len(name) > 5:
		continue

	caminho_pasta_arquivo = caminho + name + "/custos_e_soma_caminho_GA.txt"
	try:
		arq = open(caminho_pasta_arquivo, 'r')
		linhas = arq.readlines()
		arq.close()
		
		valor = float(linhas[0].split(" ")[-1])
		if valor < valor_final:
			valor_final = valor
			caminho_final = caminho_pasta_arquivo
	except:
		print("Erro na hora de verificar o resultado da pasta de caminho:")
		print(caminho_pasta_arquivo)
		print("----------------------------------------------------------")


print("menor encontrado: ", valor_final)
print("Caminho para esse valor: ", caminho_final)
