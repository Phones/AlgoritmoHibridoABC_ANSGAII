import os
import sys
from time import sleep

limite_tempo_execucao_ABC = str(sys.argv[1])
limite_tempo_execucao_GA = str(sys.argv[2])
quant_abelhas = str(sys.argv[3])
quant_indv = str(sys.argv[4])
numero_teste = str(sys.argv[5])

parametros = "-QT_ABC {} -QT_GA {} -TA_ABC {} -Q_indv {} -N_teste {}".format(limite_tempo_execucao_ABC, limite_tempo_execucao_GA, quant_abelhas,quant_indv, numero_teste)

# MONTA CAMINHO BASE ATÉ A PASTA DO TESTE
caminho_base_pasta_teste = '"/home/paulohenrique/Área de Trabalho/codigo_hibridoIC/AlgoritmoHibridoABC_ANSGAII'
caminho_base_pasta_teste = caminho_base_pasta_teste + "/ambiente_teste_algoritmo_hibrido/Codigos/teste" + numero_teste
print("caminho base: ", caminho_base_pasta_teste)

# ADICIONA CHAMADA DO PYTHON, O ARQUIVO QUE SERÁ EXECUTADO E OS PARAMETROS
comando_pronto = "python " + caminho_base_pasta_teste + '/ABC.py" ' + parametros

# ADICIONA CAMINHO PARA ARQUIVO ONDE SAIDA SERA ARMAZENADA
comando_pronto = comando_pronto + " > " + caminho_base_pasta_teste +'/saida_terminal.txt"'

# DIRECIONA SAIDA DO ERRO PARA UM ARQUIVO DE TEXTO SEPARADO
comando_pronto = comando_pronto + " 2> " + caminho_base_pasta_teste + '/erros.txt"'

print("Comando pronto: ", comando_pronto)

print("INICIANDO EXECUÇÃO DO TESTE NUMERO: ", numero_teste)
os.system(comando_pronto)

print("Fim da execução do teste " + numero_teste + " deste terminal!")
