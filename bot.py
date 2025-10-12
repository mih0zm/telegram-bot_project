import telebot
from telebot import types
from config import TOKEN
from logic import init_db, add_user
import sqlite3

bot = telebot.TeleBot(TOKEN)
init_db()

# Главное меню
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, message.from_user.username)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📅 Понедельник", callback_data="day_06.10.2025"),
        types.InlineKeyboardButton("📅 Вторник", callback_data="day_07.10.2025"),
        types.InlineKeyboardButton("📅 Среда", callback_data="day_08.10.2025"),
        types.InlineKeyboardButton("📅 Четверг", callback_data="day_09.10.2025"),
        types.InlineKeyboardButton("📅 Пятница", callback_data="day_10.10.2025"),
        types.InlineKeyboardButton("📖 Всё расписание", callback_data="all_schedule")
    )

    bot.send_message(
        message.chat.id,
        "Привет! Я бот который поможет тебе с расписанием уроков на неделю📚." \
        "\nВыбери день, чтобы увидеть расписание:",
        reply_markup=markup
    )

# Показываем расписание по дню
@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def show_day_schedule(call):
    date = call.data.replace("day_", "")
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subject, time, teacher, link FROM schedule WHERE date = ?', (date,))
    lessons = cursor.fetchall()
    conn.close()

    if not lessons:
        bot.send_message(call.message.chat.id, f"❌ На {date} уроков нет.")
    else:
        text = f"📅 *Расписание на {date}:*\n\n"
        for subject, time, teacher, link in lessons:
            text += f"📖 *{subject}*\n⏰ {time}\n👩‍🏫 {teacher}\n🔗 [{link}]({link})\n\n"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# Показываем всё расписание за неделю
@bot.callback_query_handler(func=lambda call: call.data == "all_schedule")
def show_all_schedule(call):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subject, date, time, teacher, link FROM schedule ORDER BY date, time')
    lessons = cursor.fetchall()
    conn.close()

    if not lessons:
        bot.send_message(call.message.chat.id, "❌ Расписание пока пустое.")
    else:
        text = "📚 *Расписание на всю неделю:*\n\n"
        current_date = ""
        for subject, date, time, teacher, link in lessons:
            if date != current_date:
                text += f"🗓 *{date}:*\n"
                current_date = date
            text += f"  • *{subject}* ({time}) — {teacher}\n"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

print("✅ Бот запущен...")
bot.polling(none_stop=True)


    

