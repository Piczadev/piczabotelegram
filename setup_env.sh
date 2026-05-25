#!/usr/bin/env zsh

echo "Iniciando andamiaje del proyecto Telegram SysBot..."

# Crear estructura de directorios
mkdir -p bot docs

# Crear archivos base
touch bot/__init__.py bot/main.py bot/handlers.py bot/system_ops.py
touch .env requirements.txt

# Inyectar dependencias iniciales
cat <<EOT > requirements.txt
python-telegram-bot[job-queue]>=20.0
python-dotenv>=1.0.0
EOT

# Configurar .gitignore de forma segura
cat <<EOT > .gitignore
# Entornos virtuales
venv/
.env

# Caché de Python
__pycache__/
*.py[cod]
*$py.class
EOT

# Crear entorno virtual e instalar dependencias
echo "Creando entorno virtual e instalando dependencias (esto puede tardar unos segundos)..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Estructura creada y entorno virtual activado. Ejecuta 'git status' para verificar."
