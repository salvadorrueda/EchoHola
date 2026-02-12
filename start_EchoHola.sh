#!/bin/bash

# Configuration
APP_URL="https://localhost:5000"
VENV_DIR=".venv"

echo "🚀 Iniciant EchoHola..."

# 1. Iniciar Docker Compose
echo "🐳 Iniciant Docker containers..."
docker compose up -d

# 2. Comprovar l'entorn virtual de Python
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creant l'entorn virtual de Python..."
    python3 -m venv "$VENV_DIR"
fi

echo "🔌 Activant l'entorn virtual..."
source "$VENV_DIR/bin/activate"

# 3. Comprovar i instal·lar dependències
echo "📦 Comprovant dependències..."
pip install -r requirements.txt

# 4. Obrir el navegador (en segon pla)
echo "🌐 Obrint el navegador a $APP_URL..."
if command -v xdg-open > /dev/null; then
    xdg-open "$APP_URL" &
elif command -v open > /dev/null; then
    open "$APP_URL" &
else
    echo "⚠️ No s'ha pogut obrir el navegador automàticament. Visita $APP_URL"
fi

# 5. Executar l'aplicació Python
echo "⚡ Executant app.py..."
python app.py --https
