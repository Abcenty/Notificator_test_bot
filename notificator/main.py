import asyncio

from aiogram import Dispatcher
from handlers import user_handlers, notes_handlers, incorrect_message_handler
from bot import get_bot
from logger import logger
from services.uttils.send_reminder import check_reminders


# Функция конфигурирования и запуска бота
async def main():
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    
    global bot
    # Инициализируем бот и диспетчер
    bot = get_bot()
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(notes_handlers.router)
    dp.include_router(incorrect_message_handler.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())