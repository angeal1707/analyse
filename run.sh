#!/bin/bash

# Script untuk menjalankan Aplikasi Analisis Emiten BEI

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"

# Cek apakah virtual environment ada
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment tidak ditemukan!"
    echo "Membuat virtual environment..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    source "$VENV_PATH/bin/activate"
fi

# Jalankan aplikasi
echo "🚀 Menjalankan Aplikasi Analisis Emiten BEI..."
echo "📱 Buka browser: http://localhost:5001"
echo "⏹️  Tekan CTRL+C untuk menghentikan"
python "$SCRIPT_DIR/app.py"
