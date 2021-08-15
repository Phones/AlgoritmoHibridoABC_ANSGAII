#!/bin/bash

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

echo "------------------------------------------"
echo "Criando terminais para execução"
python cria_todos_terminais_e_executa_teste.py