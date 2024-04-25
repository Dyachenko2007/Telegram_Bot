import os
import telebot
import py.config as cfg
import py.database as DB
import py.bot_handlers as BHandlers



def start_bot():
    bot = telebot.TeleBot(cfg.TELEGRAM_BOT_TOKEN)
    print("[BOT] Бот успешно запущен!")
    
    try:
        @bot.message_handler(commands = ["start"])
        def start(message):
            BHandlers.start(bot, message)

        @bot.message_handler(commands = ["чарты"])
        def top_tracks(message):
            BHandlers.top_tracks(bot, message)  

        @bot.message_handler(commands = ["артисты"])
        def top_artists(message):
            BHandlers.top_artists(bot, message)   

        @bot.message_handler(commands = ["найти"])
        def search(message):
            BHandlers.search(bot, message)     

        @bot.message_handler(content_types=["text"])
        def content_text(message):
            BHandlers.content_text(bot, message) 

    except Exception as e:
        print(f"[BOT] Произошла ошибка: {e}")
              
    bot.infinity_polling()



def main():
    os.system("cls || clear")

    DB.create()
    DB.reset_status()

    start_bot()



if __name__ == "__main__":
    main()