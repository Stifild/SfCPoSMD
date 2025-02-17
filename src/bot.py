from apscheduler.schedulers.background import BackgroundScheduler
from src.utils import Utils
from src.database_utils import Database
import telebot, logging
from zoneinfo import ZoneInfo


msk = ZoneInfo("Europe/Moscow")
io = Utils()
db = Database()
scheduler = BackgroundScheduler(timezone=msk)

config = io.load_config()

bot = telebot.TeleBot(config["Token"])

logging.basicConfig(
    filename="./logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Регистрация"))
    bot.send_message(message.chat.id, 'Привет, я бот-регистратор для "Дня Самоуправления" в Наношколе. Для продолжения нажми на кнопку "Регистрация"', reply_markup=markup)
    db.add_user(message.chat.id, message.from_user.username)
    logging.debug(f"Пользователь {message.from_user.id} зарегистрировался")
    bot.register_next_step_handler(message, registration)

def registration(message: telebot.types.Message):
    if message.text == "Регистрация":
        bot.send_message(message.chat.id, "Введите свое имя")
        bot.register_next_step_handler(message, registration_name)
    else:
        bot.send_message(message.chat.id, "Для регистрации нажмите на кнопку 'Регистрация'")

def registration_name(message: telebot.types.Message):
    db.update_value(message.from_user.id, "first_name", message.text)
    bot.send_message(message.chat.id, "Введите свою фамилию")
    bot.register_next_step_handler(message, registration_surname)

def registration_surname(message: telebot.types.Message):
    db.update_value(message.from_user.id, "second_name", message.text)
    bot.send_message(message.chat.id, "Введите свой номер телефона")
    bot.register_next_step_handler(message, registration_phone)

def registration_phone(message: telebot.types.Message):
    db.update_value(message.from_user.id, "phone", message.text)
    bot.send_message(message.chat.id, "Регистрация завершена! Ожидайте розыгрыша. А пока можете ознакомится с расписанием.")
    bot.send_message(message.chat.id, f"Расписание: {config['Schedule']}")

def first_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["1"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем первый урок! Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, first_lesson_result)

def second_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["2"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем второй урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "second_lesson")

def third_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["3"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем третий урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "third_lesson")

def fourth_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["4"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем четвертый урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "fourth_lesson")

def fifth_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["5"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем пятый урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "fifth_lesson")

def sixth_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["6"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем шестой урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "sixth_lesson")

def seventh_lesson(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for teacher in config["Teachers"]["7"]:
        markup.add(telebot.types.KeyboardButton(teacher))
    bot.send_message(message.chat.id, "Разыгрываем седьмой урок. Выбери преподавателя которого хочешь заменять из списка", reply_markup=markup)
    bot.register_next_step_handler(message, lesson_result, "seventh_lesson")

def first_lesson_result(message: telebot.types.Message):
    db.update_value(message.from_user.id, "first_lesson", message.text)
    bot.send_message(message.chat.id, "Преподаватель выбран")
    # scheduler.add_job(second_lesson, 'cron', )











bot.polling(none_stop=True)