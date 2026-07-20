#!/bin/bash

echo "🚀 Instalando Macro Recorder..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3 primeiro."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "⚠️ IMPORTANTE: Você precisa configurar as permissões do macOS:"
echo "1. Abra Preferências do Sistema > Segurança e Privacidade > Privacidade"
echo "2. Na guia 'Acessibilidade', clique no cadeado e adicione Python"
echo "3. Na guia 'Monitoramento de Entrada', faça o mesmo"
echo "4. Reinicie este script após configurar as permissões"
echo ""
echo "Para executar o Macro Recorder, use:"
echo "python3 run.py"
echo ""