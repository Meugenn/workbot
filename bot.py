# *-* coding utf-8 *-*
# Import all modules we need
import os
import time 
import random
import pickle
from sql import add_user, change_cond

import telebot  # API
from flask import Flask, request # Tools for server

import constants # File with token, tasks etc.
from functions import fuzzy_search # Function for search

bot = telebot.TeleBot(constants.token)        # Create bot with token
server = Flask(__name__)

names_of_tasks = constants.dict_of_names
 
Main_mark_up = telebot.types.ReplyKeyboardMarkup(True , False)  # Creating custom keyboards
Main_mark_up.row('Список задач' , 'Поиск') 
Main_mark_up.row('Получить задачу по сложности' ,'Книги')
Main_mark_up.row('Отправить решение', 'Отправить отзыв')

categoryes_mark_up = telebot.types.ReplyKeyboardMarkup(True , False)
categoryes_mark_up.row('Легкие', 'Средние' , 'Сложные')	
categoryes_mark_up.row('Отмена')

cancel_mark_up = telebot.types.ReplyKeyboardMarkup(True , False)
cancel_mark_up.row('Отмена')


with open('logs.pickle', 'rb') as logs:
    message_cache = pickle.load(logs) # Loading of logs

###############################################################################################################

@bot.message_handler(commands = ['start'])  # Start
def start(message):
    text_of_message = constants.start_command_message
    bot.send_message(message.from_user.id, text_of_message, reply_markup = Main_mark_up)
    add_user(message.chat.id)    # Creating logs of current user


@bot.message_handler(commands = ['help'])   # Help
def help(message):
    text_of_message = constants.help_command_message
    bot.send_message(message.from_user.id, text_of_message, reply_markup = Main_mark_up)


@bot.message_handler(commands = ['about']) # About
def about(message):
    text_of_message = constants.about_command_message
    bot.send_message(message.from_user.id, text_of_message, reply_markup = Main_mark_up)


@bot.message_handler(regexp= ['Список задач',], func= lambda message: message_cache[message.from_user.id] != 'Поиск' )
def task_handler(message):
    text_of_message = 'Ловите список задач - https://telegra.ph/Unique-Lectures-06-13 🏻. Выбирайте следующее действие.'
    bot.send_message(message.from_user.id, text_of_message, reply_markup = Main_mark_up)
    change_cond(message.chat.id, 'Список задач')


@bot.message_handler(regexp=['Получить задачу по сложности',], func = lambda message: message_cache[message.from_user.id][-1] != 'Поиск' )
def get_task(message):
    bot.send_message(message.from_user.id, 'Выберите категорию.', reply_markup = categoryes_mark_up)
    change_cond(message.chat.id, 'Категории')


@bot.message_handler(regexp=['Книги',], func = lambda message: message_cache[message.from_user.id][-1] != 'Поиск')
def books(message):
    bot.send_message(message.from_user.id,
                     'Подборочка с книгами : http://telegra.ph/UniLecsBooks-OsnovyCHast1-07-06 ! Выбирайте следующее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Книги')


@bot.message_handler(regexp=['Отправить отзыв'], func = lambda message:message_cache[message.from_user.id][-1] != 'Поиск')
def review_handler(message):
    bot.send_message(message.from_user.id,
                     'В следующем сообщении введите свой отзыв. Чтобы отменить написание отзыва, введите "Отмена".',
                     reply_markup=cancel_mark_up)
    change_cond(message.chat.id, 'Отзыв')


@bot.message_handler(regexp=['Отправить решение'], func=lambda message:message_cache[message.from_user.id][-1] != 'Поиск')
def answer (message):
    bot.send_message(message.from_user.id,
                     'В следующем сообщении введите свое решение последней опубликованной задачи. Чтобы отменить отправку решения, введите "Отмена".',
                     reply_markup=cancel_mark_up)
    change_cond(message.chat.id, 'Решение')


@bot.message_handler(regexp='Поиск', func=lambda message:message_cache[message.from_user.id][-1] != 'Поиск')
def search(message):
    bot.send_message(message.from_user.id, 'Введите название задачи или ее номер.', reply_markup=cancel_mark_up)
    change_cond(message.chat.id, 'Поиск')


@bot.message_handler(regexp=['Легкие'], func=lambda message: message_cache[message.from_user.id][-1] == 'Категории')
def easy_tasks(message):
    bot.send_message(message.from_user.id,
                     '*Легкие задачи:*\n http://telegra.ph/UniLecsLight-07-10 . Выбирайте следующее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Легкие задачи')


@bot.message_handler(regexp=['Средние'],
                     func =lambda message: message_cache[message.from_user.id][-1] == 'Категории')
def middle_tasks(message):
    bot.send_message(message.from_user.id,
                     '*Средние задачи:*\n http://telegra.ph/UniLecsMedium-07-10 . Выбирайте следующее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Средние задачи')


@bot.message_handler(regexp=['Сложные'],
                     func=lambda message: message_cache[message.from_user.id][-1] == 'Категории')
def hard_tasks(message):
    bot.send_message(message.from_user.id,
                     '*Сложные задачи:*\n http://telegra.ph/UniLecsHard-07-10 . Выбирайте следующее действие.',
                     reply_markup = Main_mark_up)
    change_cond(message.chat.id, 'Сложные задачи')


@bot.message_handler(regexp=['Отмена'],
                     func=lambda message: message_cache[message.from_user.id][-1] == 'Категории')
def cancel(message):
    bot.send_message(message.from_user.id, 'Выберите следующее действие.', reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Отмена')


@bot.message_handler(lambda message: message_cache[message.from_user.id][-1] == 'Категории')
def bad_category(message):
    bot.send_message(message.from_user.id, 'Такой категории нет. Попробуйте еще раз.', reply_markup=categoryes_mark_up)


@bot.message_handler(regexp=['Отмена'], func=lambda message: message_cache[message.from_user.id][-1] == 'Отзыв')
def cancel_feedback(message):
    bot.send_message(message.from_user.id, 'Вы отменили написание отзыва. Выберите дальнейшее действие',
                     reply_markup = Main_mark_up)
    change_cond(message.chat.id, 'Отмена')


@bot.message_handler(func=lambda message: message_cache[message.from_user.id][-1] == 'Отзыв')
def feedback(message):
    timeNow = time.strftime("%H:%M:%S %Y.%m.%d", time.localtime())
    form = '''Feedback from {0}-@{1}({2});
    Date: {3};
    Text^ {4}'''.format(message.from_user.first_name, message.from_user.username, message.from_user.id, timeNow,
                        message.text)
    bot.send_message('@unilecs_test', form)
    bot.send_message(message.from_user.id, 'Спасибо за ваш отзыв. Выберите следующее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Отзыв отправлен')


@bot.message_handler(regexp=['Отмена'], func=lambda message:message_cache[message.from_user.id][-1] == 'Решение')
def cancel_solution(message):
    bot.send_message(message.from_user.id, 'Вы отменили отправку решения. Выберите дальнейшее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Отмена')


@bot.message_handler(regexp=[], func=lambda message:message_cache[message.from_user.id][-1] == 'Решение')
def solution(message):
    timeNow = time.strftime("%H:%M:%S %Y.%m.%d", time.localtime())
    form = '''Feedback from {0}-@{1}({2});
    Date: {3};
    Text^ {4}'''.format(message.from_user.first_name, message.from_user.username, message.from_user.id, timeNow,
                        message.text)
    bot.send_message('@unilecs_test', form)
    bot.send_message(message.from_user.id, 'Спасибо за ваше решение. Выберите следующее действие.',
                     reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Решение отправлено')


@bot.message_handler(regexp=['Отмена'], func=lambda message: message_cache[message.from_user.id][-1] == 'Поиск')
def cancel_search(message):
    text_of_message = ''
    bot.send_message(message.from_user.id, 'Выберите следующее действие.', reply_markup=Main_mark_up)
    change_cond(message.chat.id, 'Отмена')




@bot.message_handler(func=lambda message: message_cache[message.from_user.id][-1] == 'Поиск' and
                                                     message.text.isnumeric())
def search(message):
    text_of_message = ''
    try:
        text_of_message += '*Task {0}* : {1}\n'.format(message.text, constants.dict_of_tasks[int(message.text)])
        bot.send_message(message.from_user.id, text_of_message, reply_markup=Main_mark_up)
        change_cond(message.chat.id, 'Задача найдена')
    except KeyError:
        bot.send_message(message.from_user.id, 'Задачи с таким номером не найдено. Попробуйте еще раз.',
                         reply_markup=cancel_mark_up)


@bot.message_handler(regexp=[], func=lambda message:message_cache[message.from_user.id][-1] == 'Поиск'
                                                    and not message.text.isnumeric())
def not_num_search(message):
    text_of_message = ''
    for task in names_of_tasks:
        if names_of_tasks[task].lower().find(message.text.lower()) != -1:
            text_of_message += '*Task {0}* : {1}\n'.format(task, constants.dict_of_tasks[task])
    if text_of_message == '':
        bot.send_message(message.from_user.id, 'Ни одной задачи не найдено. Попробуйте еще раз.',
                         reply_markup=cancel_mark_up)
    else:
        try:
            bot.send_message(message.from_user.id, text_of_message, reply_markup=Main_mark_up)
            bot.send_message(message.from_user.id, 'Выберите следующее действие.', reply_markup=Main_mark_up)
            change_cond(message.chat.id, 'Задачи найдены.')
        except Exception:
            bot.send_message(message.from_user.id,
                             'Найдено слишком много задач. Попробуйте ввести более корректный запрос.',
                             reply_markup=cancel_mark_up)

@bot.message_handler(content_types = ['text'])
def handle_message(message):
    bot.send_message(message.from_user.id, 'Простите, я вас не понимаю. Попробуйте еще раз.', reply_markup = Main_mark_up)


                    
'''@server.route('/' + constants.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://server-name.herokuapp.com/' + constants.token)
    return "!", 200'''

if __name__ == "__main__":
    bot.polling(interval = 0.5, none_stop = True)

