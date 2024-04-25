from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton



def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
    btn_1 = KeyboardButton("Топ чарты")
    btn_2 = KeyboardButton("Топ артисты")
    btn_3 = KeyboardButton("Поиск")
    keyboard.add(btn_1, btn_2, btn_3)
    return keyboard



if __name__ == "__main__":
    pass