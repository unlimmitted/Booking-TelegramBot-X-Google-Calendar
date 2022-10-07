import telebot
import re

bot = telebot.TeleBot("5531011857:AAH8ySL_cvBEtFI8fUz5WMCcWiJRmeeXAKE")


@bot.message_handler(commands=['start'])
def get_command(message):
    first_msg = bot.send_message(message.chat.id, "Message")
    message_id = first_msg.message_id
    get_message.name(message, message_id)


class get_message():
    def name(message, id_message):
        global mssg
        konf_name = message.text
        mssg = bot.edit_message_text(chat_id=message.chat.id,message_id=id_message, text="Укажите время начала конференции в формате ЧЧ.ММ")
        message_id = message.message_id
        bot.register_next_step_handler(mssg, get_message.start)
        return konf_name

    def start(message):
        konf_start = (" ".join(re.findall(r'\d{2}.\d{2}', message.text)))
        if message.text == konf_start:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mssg.message_id, text=
            "Укажите продолжительность мероприятия в формате Ч.М\n"
            "Пример ввода: 1.5(1 час 30 минут)")
            return konf_start
        else:
            bot.send_message(message.chat.id, "Несоблюдён формат ЧЧ.ММ\n"
                                              "Введите команду /booking и попробуйте снова")


bot.polling(none_stop=True)
