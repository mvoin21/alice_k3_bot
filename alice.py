import telebot
from telebot import types
import time
import json
import threading

token = '1189810253:AAF9V_tdUPxFdgqRGSPjouhATU4vQJy8W9I'

bot = telebot.TeleBot(token)

actions = ''
intentions = ''
difficulties = ''
user = ''
frases = ['Что Вы сделали?', 'Что Вы будете делать?', 'Какие сложности?']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        f'Добро пожаловать {message.from_user.first_name}. '
        f'Нажмите кнопку "standUP" для записи информации или "help" для вызова аннотации', 
        reply_markup=keyboard())


    def daily():
        time_1 = time.localtime()
        text = f'{time_1.tm_hour}:{time_1.tm_min}'
        t = threading.Timer(60, daily)
        t.start()
        if text == '14:00':
            bot.send_message(
                message.chat.id, 
                'Alice++++++++ хочет провести StandUP!',
                reply_markup=keyboard()
                )

    if True:
        daily()

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('standUP')
    btn2 = types.KeyboardButton('help')
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(content_types=['text'])
def start(message):
    global user
    if message.text == 'help':
        bot.send_message(
            message.chat.id, 
            'Вам будут заданы три вопроса, на которые потребуется ответить. На основе Ваших ответов ментора окажут Вам помощь.',
            reply_markup=keyboard()
            )
    elif message.text == 'standUP':
        bot.send_message(message.chat.id, 'Что Вы сделали?')
        bot.register_next_step_handler(message, get_actions)
        user = message.from_user.first_name

def get_actions(message):
    global actions
    actions = message.text
    bot.send_message(message.chat.id, 'Что Вы планируте делать?')
    bot.register_next_step_handler(message, get_intentions)

def get_intentions(message):
    global intentions
    intentions = message.text
    bot.send_message(
        message.chat.id, 
        'Какие сложности у Вас возникли во время выпонения задания?'
        )
    bot.register_next_step_handler(message, get_difficulties)

def get_difficulties(message):
    global difficulties
    difficulties = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Введенные ниже данные верны?\n\n1) {str(actions)}\n2) {str(intentions)}\n3) {str(difficulties)}'
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        global intentions, difficulties, frases, user, strings

        data = {
            'Имя студента': user,
            'Что сделал': actions, 
            'Что будет делать': intentions, 
            'Какие сложности возникли': difficulties
            }
        with open("data_file.json", "w") as write_file:
            json.dump(data, write_file,  ensure_ascii=False, sort_keys=True, indent=4)

        GROUP_ID = -451324106
        report = f'Имя студента: {user}\nЧто сделал: {actions}\nЧто будет делать: {intentions}\nКакие сложности возникли: {difficulties}'
        bot.send_message(GROUP_ID, report)

        bot.send_message(call.message.chat.id, 'Данные были записаны и отправлены.')

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Записанные данные были стерты')


bot.polling()
