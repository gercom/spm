#!/bin/bash

function chk_root()
{
  # Para prosseguir é feita antes essa verificação de usuário root  
  if [ $(whoami) != "root" ]; then
    echo "Preciso de privilégios root para continuar!"
    exit 2
  fi
}

chk_root

echo "Estou criando o repositório local..."
# estabelece o repositório local 
mkdir /var/lib/managerapp
echo "O repositório local está disponível, para ir até ele acesse: /var/lib/managerapp "

if [ ! -f spm.py ]; then
  echo "Não pude encontrar o arquivo SPM, coloque o arquivo na pasta corrente onde se encontra este instalador!"
exit 1
fi


if [ ! -x spm.py ]; then
  chmod a+x spm
fi

echo "A ferramenta SPM está sendo instalada em seu sistema..."

cp spm.py /usr/bin
echo "Pronto, você agora pode usar o comando spm seguido de algum argumento válido, antes disso, consulte o manual. Obrigado!"
