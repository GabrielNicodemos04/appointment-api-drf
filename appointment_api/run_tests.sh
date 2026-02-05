#!/bin/bash

# Script para executar testes da Appointment API

echo "🚀 Executando testes da Appointment API..."

# Verificar se estamos no diretório correto
if [ ! -f "core/manage.py" ]; then
    echo "❌ Erro: Execute este script do diretório raiz do projeto (appointment_api/)"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
    echo "✅ Ambiente virtual ativado"
fi

# Executar testes
echo "🧪 Executando testes..."
python -m pytest api/tests/ -v

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
else
    echo "❌ Alguns testes falharam. Verifique a saída acima."
    exit 1
fi