#!/bin/bash

echo "🎬 Macro Recorder - Iniciando..."
echo ""

# Verificar se está na pasta correta
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Este script deve ser executado na pasta macro-recorder/"
    echo "Navegue até a pasta primeiro:"
    echo "cd macro-recorder"
    echo "./start.sh"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado"
    echo "Por favor, instale o Python 3 em python.org"
    exit 1
fi

echo "✅ Python 3 encontrado"

# Verificar se dependências estão instaladas
echo "📦 Verificando dependências..."
python3 -c "import pynput" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⬇️ Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências"
        exit 1
    fi
    echo "✅ Dependências instaladas"
else
    echo "✅ Dependências já instaladas"
fi

# Verificar permissões
echo ""
echo "⚠️ VERIFICANDO PERMISSÕES DO MACOS..."
echo ""

# Tentar importar as bibliotecas para ver se funcionam
python3 -c "
import sys
try:
    from pynput import mouse, keyboard
    print('✅ Bibliotecas importadas com sucesso')
except Exception as e:
    print(f'❌ Erro ao importar bibliotecas: {e}')
    print('Você precisa conceder permissões no macOS:')
    print('1. Preferências do Sistema > Segurança e Privacidade > Privacidade')
    print('2. Acessibilidade: adicione Python ou Terminal')
    print('3. Monitoramento de Entrada: adicione Python ou Terminal')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️ PERMISSÕES NECESSÁRIAS!"
    echo ""
    echo "Siga estes passos:"
    echo "1. Abra 'Preferências do Sistema' (Apple  > Preferências do Sistema)"
    echo "2. Vá em 'Segurança e Privacidade' > 'Privacidade'"
    echo "3. Clique no cadeado 🔒 e digite sua senha"
    echo "4. Na guia 'Acessibilidade', clique em '+' e adicione:"
    echo "   - Terminal (ou Python, dependendo do seu sistema)"
    echo "5. Na guia 'Monitoramento de Entrada', faça o mesmo"
    echo "6. Execute este script novamente após configurar"
    echo ""
    exit 1
fi

echo ""
echo "🚀 Iniciando Macro Recorder..."
echo ""

# Executar o programa
python3 run.py