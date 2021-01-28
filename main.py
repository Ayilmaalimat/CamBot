import logging
import aiogram
import asyncio
import aioschedule

import config
import db

# Initialize bot and dispatcher
bot = aiogram.Bot(token=config.API_TOKEN)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: aiogram.types.Message):
    """
    Приветственное сообщение!
    :param message: Команда start или help.
    :type message: object
    :return: Приветствие.
    :rtype: str
    """
    await message.answer("Здравствуйте!\nЯ КамБот - телеграм бот для мониторинга посещений!")


@dp.message_handler(commands=['statistics'])
async def send_statistics(message: aiogram.types.Message):
    """
    Отправка статистики по запросу.
    :param message: Команда запроса.
    :type message: object
    :return: Статистика посещаемости.
    :rtype: file
    """
    if db.check_user(message['from']['id']):
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-= MESSAGE EDIT =-=-=-=-=-=-=-=-=-=-=-=-=-=-
        await message.answer("статистика")
    else:
        await message.answer('К сожалению, у вас нет доступа к статистике!')


@dp.message_handler(lambda message: message.text == 'hsdfjfkhusdgiy38945h')
async def registration_users(message: aiogram.types.Message):
    """
    Идентификация пользователя с помощью токена.
    :param message: Токен для идентификации.
    :type message: object
    :return: Ответное сообщение.
    :rtype: str
    """
    query_result = db.crete_user(
        userID=message['from']['id'],
        username=message['from']['first_name']
    )

    await message.answer(text=query_result)


@dp.message_handler(lambda message: message.text == 'Отправить всем пользователям!')
async def event_loop_statistics():
    """
    Отправка пользователям статистики за промежуток времени.
    :return: Статистика посещаемости.
    :rtype: file
    """
    for i in db.all_users():

        try:
            # -=-=-=-=-=-=-=-=-=-=-=-=-=-= TEXT EDIT =-=-=-=-=-=-=-=-=-=-=-=-=-=-
            await bot.send_message(chat_id=i[1], text='test loop')
        except Exception as e:
            print(f'-->Error send message! \nId: {i[1]} \nUsername: {i[2]} \nError: {e}')


async def scheduler():
    """ Инициализация петли """
    aioschedule.every().day.at("11:00").do(event_loop_statistics)
    aioschedule.every().day.at("19:00").do(event_loop_statistics)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    """ Создание таска петли """
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
