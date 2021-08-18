#!/bin/bash

function quant_terminais_abertos()
{
	declare -i quant_terminais=$(ls /dev/pts/  | wc -l)
	echo $quant_terminais
}

function espera_processos_finalizarem()
{
	echo "ESPERANDO RODADA ANTERIOR FINALIZAR, PARA INICIAR A PROXIMA"
	cont=0
	while [ $cont -lt 1 ]
	do
		num_terminais=`quant_terminais_abertos`
		#echo "Numero terminais $num_terminais"
		if [ $num_terminais -lt 3 ]
		then
			let cont=cont+1
		fi
	done
	echo "!!!!!!!!!!!!!!!!!!!!! RODADA COMPLETA !!!!!!!!!!!!!!!!!!!!!"
}

echo "Iniciando execução dos testes!"

echo "------------------------------------------"
echo "parametro: $1"

if [ "$1" == "at" ]
then
	echo "------------------------------------------"
	echo "Atualizando codigo BASE!"
	./atualiza_codigo_base.sh
else
	echo "------------------------------------------"
	echo "Executando testes, sem atualizar codigo!"
fi

echo "------------------------------------------"
echo "Apagando pastas de teste antigas!"
./copy_or_delete.sh rm

echo "------------------------------------------"
echo "Gerando novas pastas de teste!"
./copy_or_delete.sh

declare -i quant_rodadas_teste=5

for i in $(seq 1 $quant_rodadas_teste);
do
	echo "------------- INICIANDO RODADA DE TESTE NÚMERO: $i -------------"
	echo "  --- Criando terminais para execução e executando testes ---"
	python cria_todos_terminais_e_executa_teste.py
	espera_processos_finalizarem
	./move_arquivo_saida_terminal.sh
done
