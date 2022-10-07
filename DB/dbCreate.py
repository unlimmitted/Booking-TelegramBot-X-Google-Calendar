import sqlite3 as sql
import telebot
from bot_token import BotToken


def create(chat_id, first_name, last_name):
    global sad
    con = sql.connect(f'DB/users.db')
    cur = con.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS user_{chat_id} (first_name TEXT, last_name TEXT, chat_id INT, id_last_konf TEXT)""")
    cur.execute(f"INSERT INTO user_{chat_id} VALUES ( ?, ?, ?, ?)", (first_name, last_name, chat_id, "0"))
    con.commit()
    con.close()
    sad = chat_id
    return sad


def add_id_konf(chat_id, event_result):
    con = sql.connect(f'DB/users.db')
    cur = con.cursor()
    cur.execute(f"UPDATE user_{chat_id} SET id_last_konf = ? WHERE chat_id = ?", (event_result, chat_id))
    cur = con.cursor()

    con.commit()
    con.close()


def select_into_db(chat_id):
    con = sql.connect(f'DB/users.db')
    cur = con.cursor()
    cur.execute(f"SELECT last_name, first_name FROM user_{chat_id}")
    id_last_konf = cur.fetchone()
    return id_last_konf
