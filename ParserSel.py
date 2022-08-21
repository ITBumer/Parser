from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import telebot
from telebot import types
import os
bot = telebot.TeleBot('1930263092:AAEUYmVp0Ezf9DzCn7HQgEp1y-iMO9MvOJE');
URL = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mv]=udtf8&p='
word = '3080'   # Переиенная для храниения значений
symbol = '₽'    # Переиенная для храниения значений
urlpag = 1      # Счётчик страниц
vol_data = []   # Пустой список для данных

# Функция создания кнопки

def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.add('Pars',)
    bot.send_message(message.from_user.id, "ОК !",reply_markup=markup)

# Функция перехода страниц

def pag():
    global urlpag
    global URL
    urlpag += 1
    URL = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mv]=udtf8&p='
    URL = URL + str(urlpag)     # Увеличиваем значение URL на 1
    main(URL)

# Функция для работы парсера

def main(url):
    global var_1
    global var_2
    global vol_data
    global urlpag
    driver = webdriver.Chrome(ChromeDriverManager().install())              # Запускаем ChromeDriverManager
    driver.get(url)                                                         # Посылаем запрос
    title = driver.find_element_by_class_name('products-list__content')     # Выбираем из HTML class для парсинга
    time.sleep(0.5)
    list = title.text                                                       # Записываем в переменную полученный текст
    driver.quit()
    # Цикл для перебора значений
    for i in list.split('\n'):
        if word in i:
            time.sleep(0.3)
            var_1 = i
        if symbol in i:
            time.sleep(0.3)
            var_2 = i
            vol_data.append(var_1 + str('-') + var_2)                  # Записываем получнные данные из цикла в список

    # Проверяем если в данных есть значение "3080" то вызываем функцию pag(), если нет то обнуляем счётчик
    index = list.find('3080')
    if index != -1:
        time.sleep(0.3)
        pag()
    else:
        urlpag = 1

# Основная функция для работы бота

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    send_welcome(message)
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Добрый день ! Нажмите на Pars")
        bot.send_message(message.from_user.id, "\U0001F60E")
    if message.text == 'Pars':
        bot.send_message(message.from_user.id, "Начинаю загрузку данных подождите...")
        with open("Pars.csv", "w", encoding="utf8") as file:   # Открываем фаил для записи данных
            URL = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mv]=udtf8&p='
            main(URL)
            file.write(",\n".join(map(str, vol_data)))  # Записываем данные
        bot.send_document(message.from_user.id, document=open('Pars.csv', 'rb')) # Отправляем данные в телеграмм данные
        bot.send_message(message.from_user.id, "Данные успешно загружены !")
        vol_data.clear()
        os.remove('Pars.csv')


bot.polling(none_stop=True, interval=0)

