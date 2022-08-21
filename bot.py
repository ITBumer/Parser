import telebot
from telebot import types
import os


bot = telebot.TeleBot('1930263092:AAEUYmVp0Ezf9DzCn7HQgEp1y-iMO9MvOJE')

def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.add('Pars',)
    bot.send_message(message.from_user.id, "ОК !",reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    send_welcome(message)
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Добрый день ! Нажмите на Pars")
        bot.send_message(message.from_user.id, "\U0001F60E")
    if message.text == 'Pars':
        bot.send_message(message.from_user.id, "Начинаю загрузку данных подождите...")
        os.system('python Parssel.py')
        bot.send_document(message.from_user.id, document=open('Pars.csv', 'rb')) # Отправляем данные в телеграмм данные
        bot.send_message(message.from_user.id, "Данные успешно загружены !")
        os.remove('Pars.csv')


bot.polling(none_stop=True, interval=0)