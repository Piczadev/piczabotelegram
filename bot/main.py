import asyncio
import logging
import os
import signal
from pathlib import Path
import os
import signal
from contextlib import suppress

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.handlers import start, handle_message, pete, save_cmd, task, hermes


logger = logging.getLogger(__name__)


def build_application() -> Application:
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is not configured in the environment.")

    # Read the Gemini key now so the bootstrap owns both required secrets.
    os.getenv("GEMINI_API_KEY")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pete", pete))
    application.add_handler(CommandHandler("save", save_cmd))
    application.add_handler(CommandHandler("task", task))
    application.add_handler(CommandHandler("hermes", hermes))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    return application


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    application = build_application()
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    for signame in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError, RuntimeError):
            loop.add_signal_handler(signame, stop_event.set)

    logger.info("Starting Telegram SysBot bootstrap.")
    await application.initialize()
    await application.start()

    if application.updater is None:
        raise RuntimeError("Telegram application updater is not available.")

    await application.updater.start_polling()

    try:
        await stop_event.wait()
    finally:
        logger.info("Stopping Telegram SysBot.")
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
