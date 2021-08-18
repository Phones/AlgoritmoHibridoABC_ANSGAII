#!/bin/bash

eclare -i quant_testes

quant_testes=`cat quant_testes.txt`

echo "Quantidade de teste -> $quant_testes"

caminho_pasta_atual=`pwd`

echo "caminho pasta atual: $caminho_pasta_atual"

for i in $(seq 1 $quant_testes)
do
	caminho_pasta_arquivo=$caminho_pasta_atual"/teste1"
	echo "Caminho pasta do teste: $caminho_pasta_arquivo"

	caminho_pasta_resultados=`cat "$caminho_pasta_arquivo/caminho_pasta_resultado.txt"`
	echo "Caminho pasta do resultado: $caminho_pasta_resultados"
	
	echo "Movendo saida de terminal do teste: $1"
	mv "$caminho_pasta_arquivo/saida_terminal.txt" "$caminho_pasta_resultados/"
done




