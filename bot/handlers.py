import os
import aiofiles
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

ALLOWED_USER_ID = 7209407129
INBOX_DIR = "docs/inbox"
FILES_DIR = os.path.join(INBOX_DIR, "files")

# Ensure inbox dirs exist
os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

async def check_whitelist(update: Update) -> bool:
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        if update.effective_message:
            await update.effective_message.reply_text("⛔ Acceso denegado. No tienes autorización.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return
    await update.effective_message.reply_text("🟢 Sistema base en línea. Todo lo enviado aquí será capturado.")

# --- Nuevos Comandos (Placeholders) ---
async def pete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return
    await update.effective_message.reply_text("📡 Comando /pete activado. Conectando con piczadev...")

async def save_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return
    await update.effective_message.reply_text("☁️ Comando /save. Envía cualquier archivo y lo enviaré a tus mensajes guardados (privado).")

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return
    await update.effective_message.reply_text("📝 Comando /task. Función de creación de tareas en standby.")

async def hermes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return
    await update.effective_message.reply_text("🦉 Comando /hermes. Interfaz conversacional en standby.")

# --- Manejador Principal (Texto y Archivos) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_whitelist(update): return

    message = update.effective_message
    if not message: return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = message.chat_id
    chat_type = message.chat.type
    chat_name = message.chat.title if chat_type in ["group", "supergroup"] else "Privado"
    
    # 1. Guardar historial completo en texto plano (por chat)
    text_content = message.text or message.caption or ""
    history_file = os.path.join(INBOX_DIR, f"chat_history_{chat_id}.txt")
    
    async with aiofiles.open(history_file, mode='a', encoding='utf-8') as f:
        # Formato simple de historial
        await f.write(f"[{timestamp}] {message.from_user.first_name}: {text_content}\n")
    
    # Si tiene archivos adjuntos, los descargamos localmente
    has_attachment = bool(message.document or message.photo or message.video or message.audio or message.voice)
    
    if has_attachment:
        try:
            # Identificar el tipo de archivo y obtener el file_id
            file_id = None
            ext = ".file"
            
            if message.photo:
                file_id = message.photo[-1].file_id  # Obtener la foto de mayor resolución
                ext = ".jpg"
            elif message.document:
                file_id = message.document.file_id
                # Intentar mantener la extensión original si es posible
                if message.document.file_name:
                    ext = os.path.splitext(message.document.file_name)[1]
            elif message.video:
                file_id = message.video.file_id
                ext = ".mp4"
            elif message.audio:
                file_id = message.audio.file_id
                ext = ".mp3"
            elif message.voice:
                file_id = message.voice.file_id
                ext = ".ogg"
            
            if file_id:
                # Obtener el archivo desde los servidores de Telegram
                tg_file = await context.bot.get_file(file_id)
                file_path = os.path.join(FILES_DIR, f"{timestamp.replace(' ', '_').replace(':', '-')}_{file_id[:8]}{ext}")
                
                # Descargar el archivo físicamente en local
                await tg_file.download_to_drive(custom_path=file_path)
                
                # Registrar la descarga en el historial
                async with aiofiles.open(history_file, mode='a', encoding='utf-8') as f:
                    await f.write(f"[{timestamp}] 📎 Archivo descargado localmente en: {file_path}\n")
                    
                await message.reply_text("📥 Archivo descargado y guardado en local (docs/inbox/files/).")
                
        except Exception as e:
            await message.reply_text(f"⚠️ Error al descargar el archivo: {e}")
            
    # Si es solo texto en chat privado, responder sutilmente
    elif chat_type == "private":
        await message.reply_text("📝 Mensaje registrado en el historial.")
