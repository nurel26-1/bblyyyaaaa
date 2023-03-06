from aiogram import types, executor, Dispatcher, Bot

import requests
from bs4 import BeautifulSoup


from selenium import webdriver

bot = Bot(token='6035103069:AAG4-9-6rgCvmSpwHar665UDXqejBwFPf7U')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def begin(massage: types.Message):
    await bot.send_message(massage.chat.id, "hello")


@dp.message_handler(content_types=['text'])
async def text(massage: types.Message):
    url = "https://ru.wikipedia.org/w/index.php?go=Перейти&search=" + massage.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    links = soup.find_all("div", class_="mw-search-result-heading")

    if len(links) > 0:
        url = "https://ru.wikipedia.org" + links[0].find("a")["href"]
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)

    driver.execute_script("window.scrollTo(0,200)")
    driver.save_screenshot("img.png")
    driver.close()

    photo = open("img.png", 'rb')
    await bot.send_photo(massage.chat.id, photo=photo, caption=f"ссылка:{url}")


executor.start_polling(dp)
