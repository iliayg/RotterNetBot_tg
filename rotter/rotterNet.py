import json
import time
import asyncio
from telegram import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from main import main, new_user, check_news_update, save_in_json, token

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["לקבל עידכונים"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("ברוכים הבאים לבוט המבזקים של רוטר!", parse_mode="Markdown", reply_markup=keyboard)


@dp.message_handler(Text(equals="לקבל עידכונים"))
async def get_fresh_news(message: types.Message):
    new_user()
    await send_news()

async def send_news():
    while True:
        updated_news = check_news_update()
        with open("users_dict.json") as file:
            info = json.load(file)
        user_id = []
        for i in info:
            user_id.append(i['user_id'])
        for each in user_id:
                for k, v in sorted(updated_news):
                    news = f"<a href='{(v['article_url'])}'> {'מבזק'}</a>"
                    await bot.send_message(each, news, parse_mode=ParseMode.HTML)
                    save_in_json()
                    time.sleep(5)
        print("I'm alive!")
        await asyncio.sleep(900)


if __name__ == '__main__':
    main()
    save_in_json()
    loop = asyncio.get_event_loop()
    loop.create_task(send_news())
    executor.start_polling(dp, skip_updates=True)
