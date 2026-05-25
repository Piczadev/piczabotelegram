# Telegram SysBot Analyzer

## Descripción
Bot de Telegram desarrollado en Python diseñado para la ingesta, análisis de mensajes y ejecución de tareas de integración con el sistema local (macOS). Actúa como una interfaz móvil para el ecosistema de trabajo principal, permitiendo automatización y consulta remota.

## Stack Tecnológico
- **Lenguaje:** Python 3.11+
- **Librería Principal:** `python-telegram-bot` (Asíncrono)
- **Gestión de Entorno:** Entorno virtual nativo / dependencias en `requirements.txt`
- **Integración:** Obsidian URI, Shell scripting (Zsh)

## Estructura del Proyecto
```text
BotTelegram_Sys/
├── bot/
│   ├── __init__.py
│   ├── main.py           # Entry point y configuración asíncrona
│   ├── handlers.py       # Lógica de comandos (/start, /analyze)
│   └── system_ops.py     # Interacción con el sistema operativo local
├── docs/                 # Documentación técnica (MOC)
├── .env                  # Variables de entorno (TELEGRAM_TOKEN)
├── agent.md              # Instrucciones del Agente de IA
└── README.md
