from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import re
from DB import dbCreate
import telebot
from bot_token import BotToken

bot = telebot.TeleBot(BotToken.bookingToken)


def main(konf_start, konf_name, konf_time, konf_date, konf_description, chat_id):
    days = ("".join(re.findall(r'^\d.', konf_date))).replace(".", "")
    mounth = ("".join(re.findall(r'.\d{2}.', konf_date))).replace(".", "")
    years = ("".join(re.findall(r'(.\d{2})', konf_date))).replace(".", "").replace(mounth, "")

    hours = int(("".join(re.findall(r'\d{2}.', konf_start))).replace(".", "")) - 2
    minuts = int(("".join(re.findall(r'.\d{2}', konf_start))).replace(".", ""))

    service = get_calendar_service()
    d = datetime.now().date()
    tomorrow = datetime(int(f"20{years}"), int(mounth), int(days), hours, minuts)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=float(konf_time))).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": konf_name,
                                               "description": konf_description,
                                               "start": {"dateTime": start, "timeZone": 'Europe/London'},
                                               "end": {"dateTime": end, "timeZone": 'Europe/London'},
                                           }
                                           ).execute()
    dbCreate.add_id_konf(chat_id, event_result['id'])
