import telebot
import py.config as cfg
import py.database as DB
import py.keyboards as Keyboards
import py.modules.deezer_module as Deezer



def start(bot: telebot.TeleBot, message):
    user_id = message.chat.id
    user_name = message.from_user.first_name

    if not DB.is_exist(user_id):
        DB.register(user_id, user_name)

    bot.send_sticker(user_id, cfg.STICKER_ID)
    bot.send_message(user_id, f'Привет, {user_name}. Я эксперт в области музыке! Можешь сам в этом убедиться, например, нажимай на кнопку "Топ чарты"')



def get_data(bot: telebot.TeleBot, message, func, *args):
    user_id = message.chat.id
    user = DB.get_user(user_id)

    if user is None:
        return None
    
    if user.status != cfg.FREE:
        return None

    DB.update(user_id, status = cfg.WORKING)

    bot.send_message(user_id, "Ожидайте, получаю информацию...")

    data = func(*args)

    DB.update(user_id, status = cfg.FREE)

    return data



def top_tracks(bot: telebot.TeleBot, message):
    user_id = message.chat.id

    tracks = get_data(bot, message, Deezer.get_charts)['tracks']['data']

    if tracks != None:
        answer = f"ТОП {len(tracks)} ТРЕКОВ:\n"
        
        for i, track in enumerate(tracks):
            answer += f"{i + 1}) {track['title']} - {track['artist']['name']}\n"

        bot.send_message(user_id, answer)

    

def top_artists(bot: telebot.TeleBot, message):
    user_id = message.chat.id

    artists = get_data(bot, message, Deezer.get_charts)['artists']['data']

    if artists != None:
        answer = f"ТОП {len(artists)} АРТИСТОВ:\n"
        
        for i, artist in enumerate(artists):
            answer += f"{i + 1}) {artist['name']}\n"

        bot.send_message(user_id, answer)



def search(bot: telebot.TeleBot, message):
    user_id = message.chat.id
    text = message.text

    args = text.split(" ")
    
    if len(args) < 3:
        bot.send_message(user_id, "Неверное число аргументов! Проверьте еще раз:\n/найти <Тип (track или artist)> <Название>", reply_markup = Keyboards.get_keyboard())
        return

    query = " ".join(args[2:])

    data_type = "track"
        
    if args[1].lower() == "track":
        data_type = "track"

    elif args[1].lower() == "artist":
        data_type = "artist"

    data = get_data(bot, message, Deezer.search, query, data_type)

    if data != None:
        
        if data_type == "track":
            title = f"{data['title']} - {data['artist']['name']}"
            preview = Deezer.get_content(data['preview'])
            bot.send_audio(user_id, audio = preview, title = title)

        elif data_type == "artist":
            caption = f"{data['name']}"
            photo = Deezer.get_content(data['picture_big'])
            bot.send_photo(user_id, photo = photo, caption = caption)
    
    else:
        bot.send_message(user_id, "Произошла ошибка... Попробуйте позже")



def content_text(bot: telebot.TeleBot, message):
    user_id = message.chat.id
    text = message.text

    if "чарты" in text.lower():
        top_tracks(bot, message)

    elif "артисты" in text.lower():
        top_artists(bot, message)

    elif "поиск" in text.lower():
        bot.send_message(user_id, "Вы можете искать треки и исполнителей. Шаблон:\n/найти <Тип (track или artist)> <Название>")
    
    else:
        bot.send_message(user_id, "Не понимаю твою команду, попробуй другую :)", reply_markup = Keyboards.get_keyboard())



if __name__ == "__main__":
    pass