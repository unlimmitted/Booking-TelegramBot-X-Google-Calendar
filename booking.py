import telebot
from telebot import types
import create_event
from DB import dbCreate
from bot_token import BotToken
import sqlite3 as sql
import re

bot = telebot.TeleBot(BotToken.bookingToken)

@bot.message_handler(commands=['conference_today'])
def get_conference(message):
    bot.send_message(message.chat.id,
                     f"")

@bot.message_handler(commands=['reg'])
def get_reg_command(message):
    con = sql.connect(f'DB/users.db')
    cur = con.cursor()
    cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='user_{message.chat.id}';""")
    r = cur.fetchone()
    if r == None:
        kb = types.InlineKeyboardMarkup(row_width=2)
        key_accept = types.InlineKeyboardButton(text="Все верно", callback_data='Accept')
        key_disclaim = types.InlineKeyboardButton(text="Внести изменения", callback_data='Rename')
        kb.add(key_accept, key_disclaim)
        bot.send_message(message.chat.id,
                         f"Добрый день!\n\nПроверьте, совпадает ли ваши реальные Фамилия Имя с нашей информацией:\n"
                         f"{message.chat.last_name} "
                         f"{message.chat.first_name} \n"
                         "\n(Если в тексте выше пресутствует None, нажмите кнопку "
                         "\"Внести изменения\")",
                         reply_markup=kb)
    else:
        bot.send_message(message.chat.id, "Ваша учетная запись уже существует")
    con.close()


@bot.message_handler(commands=['booking'])
def get_booking_command(message):
    con = sql.connect(f'DB/users.db')
    cur = con.cursor()
    cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='user_{message.chat.id}';""")
    r = cur.fetchone()
    if r == None:
        bot.send_message(message.chat.id, "Не видим вашу учетную запись, пройдите"
                                          " пожалуйста регистрацию по команде /reg")
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Добрый день!\n"
                                                                         "\nУкажите название мероприятия"),
                                       get_messages.name)
    con.close()


@bot.message_handler(commands=['info'])
def get_info_command(message):
    bot.send_message(message.chat.id, "Учетные записи без корректного "
                                      "\"Фамилия Имя\" будут удаляться. ")


class get_messages():
    def name(message):
        global konf_name
        konf_name = message.text
        msg = bot.send_message(message.chat.id, "Укажите время начала конференции строго в формате ЧЧ.ММ\n"
                                                "Пример 14.30")
        bot.register_next_step_handler(msg, get_messages.start)
        return konf_name

    def start(message):
        global konf_start
        konf_start = (" ".join(re.findall(r'\d{2}.\d{2}', message.text)))
        if message.text == konf_start:
            msg = bot.send_message(message.chat.id,
                                   "Укажите продолжительность мероприятия в часах по формату Ч.М\n"
                                   "Пример: 2.0 означает два часа, 1.5 означает 1 час 30 минут")
            bot.register_next_step_handler(msg, get_messages.end)
            return konf_start
        else:
            bot.send_message(message.chat.id, "Несоблюдён формат ЧЧ.ММ\n"
                                              "Введите команду /booking и попробуйте снова")

    def end(message):
        global konf_end
        konf_end = (" ".join(re.findall(r'\d{1}.\d{1}', message.text)))
        if message.text == konf_end:
            msg = bot.send_message(message.chat.id, "Укажите дату проведения конференции строго в формате ДД.ММ.ГГ\n"
                                                    "Пример 01.12.22")
            bot.register_next_step_handler(msg, get_messages.date)
            return konf_end
        else:
            bot.send_message(message.chat.id, "Несоблюдён формат Ч.М\n"
                                              "Введите команду /booking и попробуйте снова")
            get_messages.name(message)

    def date(message):
        global konf_date
        konf_date = (" ".join(re.findall(r'\d{2}.\d{2}.\d{2}', message.text)))
        if message.text == konf_date:
            chat_id = message.chat.id
            create_event.main(konf_start, konf_name, konf_end, konf_date, dbCreate.select_into_db(chat_id), chat_id)
            bot.send_message(message.chat.id,
                             f"Название: {konf_name}\n"
                             f"Дата: {konf_date}\n"
                             f"Начало/Продолжительность: {konf_start} / {konf_end}\n"
                             f"\n"
                             f"Бронирование  успешно")
            return konf_date
        else:
            bot.send_message(message.chat.id, "Несоблюдён формат ДД.ММ.ГГ\n"
                                              "Введите команду /booking и попробуйте снова")


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data == 'Accept':
        dbCreate.create(call.from_user.id, call.from_user.first_name, call.from_user.last_name)
        bot.send_message(call.from_user.id, "Учетная запись создана")
    if call.data == 'Rename':
        bot.send_message(call.from_user.id, "Для корректной работы бота "
                                            "\nтребуется ваше корректное \n\"Фамилия Имя\""
                                            "\nИзменить его можно в настройках Telegram")


bot.polling(none_stop=True)
