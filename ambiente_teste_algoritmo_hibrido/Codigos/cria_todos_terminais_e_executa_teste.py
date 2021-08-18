import os
import random
from time import sleep

arq = open('quant_testes.txt', 'r')
quant_testes = int(arq.read())
arq.close()

random.seed(None)
print("Quantidade de terminais que serão executados: ", quant_testes)

def monta_lista_parametros_de_teste():
	# limite_tempo_execucao_ABC, limite_tempo_execucao_GA, quant_abelhas,quant_indv, numero_teste
	lista_final_teste = []
	for i in range(1, quant_testes + 1):
		parametros_ = '1200 3600 ' + str(random.randint(1,5) * 100) + " " + str(random.randint(1,15)) + " " + str(i)
		# parametros_ = '5 5 100 10 ' + str(i) # parametros para teste
		lista_final_teste.append(parametros_)

	return lista_final_teste

lista_parametros = monta_lista_parametros_de_teste()
for i in range(1, quant_testes + 1):
	print("RODANDO TESTE DE NUMERO: ", i)
	comando = "gnome-terminal -e 'python executa_teste_por_terminal.py " + lista_parametros[i - 1] + "'"
	print("COMANDO PARA INICIAR TERMINAL PRONTO: ", comando)
	os.system(comando)
	sleep(0.5)
