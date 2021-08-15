echo "Iniciando atualizando do Codigo base para os testes!"

echo "Deletando codigo base antigo"
rm -rf teste

echo "Copiando codigo mais recente para ambiente de teste!"
cp -r "/home/paulohenrique/Área de Trabalho/codigo_hibridoIC/AlgoritmoHibridoABC_ANSGAII/CodigoPrincipal" "`pwd`/"

echo "Renomeando pasta do codigo base para teste"
mv "CodigoPrincipal" "teste"

echo "Fim do programa!"