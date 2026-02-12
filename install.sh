#!/bin/bash

# EchoHola Installer
# Aquest script crea un enllaç a /usr/local/bin per a que puguis executar 'echohola' des de qualsevol lloc.

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BIN_PATH="/usr/local/bin/echohola"
WRAPPER_PATH="$PROJECT_DIR/echohola_wrapper.sh"

echo "🛠️ Preparant la instal·lació d'EchoHola..."

# 1. Crear el wrapper script
cat << EOF > "$WRAPPER_PATH"
#!/bin/bash
cd "$PROJECT_DIR"
./start_EchoHola.sh
EOF

chmod +x "$WRAPPER_PATH"
chmod +x "$PROJECT_DIR/start_EchoHola.sh"

echo "🚀 Creant la comanda 'echohola' a $BIN_PATH..."
echo "Nota: Es requeriran permisos de sudo per escriure a /usr/local/bin"

if sudo ln -sf "$WRAPPER_PATH" "$BIN_PATH"; then
    echo "✅ Instal·lació completada correctament!"
    echo "Ara pots executar 'echohola' des de qualsevol terminal."
else
    echo "❌ Error en crear l'enllaç simbòlic. Intenta-ho manualment amb sudo."
    exit 1
fi
