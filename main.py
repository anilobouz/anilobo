import telebot
from telebot import types
import time

# ----------------- SOZLAMALAR -----------------
TOKEN = "8695352551:AAECgz6VJJmj12xJzf_rAD-NTOUeign35FU"  # O'zingizning bot tokeningizni yozing
BOT_USERNAME = "anilebobot"        # Botingiz username-i

bot = telebot.TeleBot(TOKEN)

# ----------------- ANIME MA'LUMOTLAR BAZASI -----------------
# SIZNING_RASM_ID degan joyga o'sha bot bergan rasm ID-sini qo'ying.
# Videolar ID-larini esa "1", "2", ... deb pastga terib chiqasiz.
ANIMELAR = {
    "1": {
        "nomi": "Qora chaqiruvchi",
        "rasm": "AgACAgIAAxkBAAMqalcK3PX7nqkEq0_gFWuh6ZdzPoAAAjYVaxseorhKDBJt7zNaeLoBAAMCAAN4AAM9BA", 
        "holati": "12 qism",
        "qismlar_soni": 12,
        "qismlar": {
            "1": "BAACAgIAAxkBAAM9alcM9Ny8zk8JrRqdFxDr9Xk7TfoAAsiNAAJ5kzFK1_Gg_BiU-DI9BA",
            "2": "BAACAgIAAxkBAANOalcNiqRBpaLiy8wgAbtBcpCWpQsAAuOTAALf7alJLno9SyPz_VA9BA",
            "3":"BAACAgIAAxkBAANQalcOHUdNyhUttDKj0qMqm0LyzeUAAqOSAALQ7JhIsaTaTPOjSx89BA",
            "4":"BAACAgIAAxkBAANValcPGK7xPsOkP0SXVes64iDpkEYAAq-SAALQ7JhIZIZX6jyo-4k9BA",
 "5":"BAACAgIAAxkBAANZalcQ2qYXINg2PRqIdAuiLevVIOgAAjuaAAIxlsBJlW19o1h_Hmk9BA",
 "6":"BAACAgIAAxkBAANbalcRAlJnqj37vNRnhr0WRbJ0L6oAAkCaAAIxlsBJIVJS02C1IaA9BA",
 "7":"BAACAgIAAxkBAANdalcRDzRgQzs3kMEkr1WM0T4jVr8AAkGUAAJKjphIIgvQJw9xgj49BA",
 "8":"BAACAgIAAxkBAANfalcRFs4rIHOmcwnaN0TqQmcT4NkAAj2UAAJKjphIvJpLmVKhXuk9BA",
 "9":"BAACAgIAAxkBAANhalcRIJvLwto_d87FfiTnxbXbZAAD8pQAAkqOmEjaKMocK93hZz0E",
 "10":"BAACAgIAAxkBAANjalcRJ0k14y5nRELjG4prh2FK8bEAAgKVAAJKjphIJsRfsxth7ig9BA",
 "11":"BAACAgIAAxkBAANlalcRMaZS6yREfK7qBEs5EA6GHRkAAp-VAAJKjphIznHIiRc1YFw9BA",
 "12":"BAACAgIAAxkBAANnalcRPKNeuz9JhaKlknW_TMyYudAAAqiVAAJKjphIQ-WfAmCwRVc9BA"
            # Qolgan qismlarni ham video ID-sini olib, shu yerga qo'shib borasiz:
            # "3": "video_id_bu_yerda",
            # "4": "video_id_bu_yerda",
        }
    }
}

# ----------------- 🚨 FAYL ID OLISH TIZIMI -----------------
@bot.message_handler(content_types=['photo', 'video', 'document'])
def get_file_id(message):
    try:
        file_id = ""
        f_type = ""
        
        if message.photo:
            file_id = message.photo[-1].file_id
            f_type = "Rasm (Photo)"
        elif message.video:
            file_id = message.video.file_id
            f_type = "Video"
        elif message.document:
            file_id = message.document.file_id
            f_type = "Fayl"
            
        text = (
            f"📥 **{f_type} qabul qilindi!**\n\n"
            f"Kodingizga qo'yish uchun uning ID kodi:\n\n"
            f"`{file_id}`\n\n"
            f"👆 Ushbu kodni nusxalab, koddagi kerakli qismga qo'ying."
        )
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception as e:
        print(f"ID olishda xato: {e}")

# ----------------- /START BUYRUG'I -----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_search = types.InlineKeyboardButton("🔍 Anime Izlash", callback_data="anime_search")
    markup.add(btn_search)
    
    welcome_text = (
        "Salom! Botimizga xush kelibsiz😊\n"
        "Anime kormoqshi bolsangiz Anime Izlashni bosing!"
    )
    
    bot.send_message(chat_id=message.chat.id, text=welcome_text, reply_markup=markup)

# ----------------- ANIME BAFSILOTLARI GENERATORI -----------------
def generate_anime_view(anime_code):
    anime = ANIMELAR[anime_code]
    
    caption = (
        f"📝 Anime nomi: {anime['nomi']}\n\n"
        f"┣ Holati: {anime['holati']}\n"
        f"┣ Sifat: 720p - 1080p\n"
        f"┣ Kanal: @anilebobot\n"
        f"┗ Anime ID: {anime_code}\n\n"
        f"Link: https://t.me/{BOT_USERNAME}?start={anime_code}"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    
    for q_num in range(1, anime['qismlar_soni'] + 1):
        btn = types.InlineKeyboardButton(f"{q_num}-qism", callback_data=f"get_{anime_code}_{q_num}")
        buttons.append(btn)
        
    markup.add(*buttons)
    return anime['rasm'], caption, markup

# ----------------- INLINE TUGMALAR (CALLBACKS) -----------------
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    try:
        if call.data == "anime_search":
            markup = types.InlineKeyboardMarkup()
            btn_name = types.InlineKeyboardButton("✏️ Anime nomi orqali", callback_data="search_by_name")
            btn_code = types.InlineKeyboardButton("🔢 Anime kod orqali", callback_data="search_by_code")
            btn_all = types.InlineKeyboardButton("📚 Barcha Animelar", callback_data="all_animes")
            markup.add(btn_name)
            markup.add(btn_code)
            markup.add(btn_all)
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Qanday usulda qidirmoqchisiz? Tanlang 👇",
                reply_markup=markup
            )

        elif call.data == "search_by_name":
            sent_msg = bot.send_message(call.message.chat.id, "Salom! Anime nomi yozing😊")
            bot.register_next_step_handler(sent_msg, search_anime_by_name)
            
        elif call.data == "search_by_code":
            sent_msg = bot.send_message(call.message.chat.id, "Salom! Anime kodini yozing😊")
            bot.register_next_step_handler(sent_msg, search_anime_by_code)
            
        elif call.data == "all_animes":
            if not ANIMELAR:
                bot.send_message(call.message.chat.id, "Hozircha botda hech qanday anime yo'q.")
                return
                
            markup = types.InlineKeyboardMarkup()
            for code, anime in ANIMELAR.items():
                markup.add(types.InlineKeyboardButton(anime['nomi'], callback_data=f"view_{code}"))
                
            bot.send_message(call.message.chat.id, "📚 Barcha animelar ro'yxati:", reply_markup=markup)
            
        elif call.data.startswith("view_"):
            anime_code = call.data.split("_")[1]
            if anime_code in ANIMELAR:
                photo, caption, markup = generate_anime_view(anime_code)
                bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=markup)
                
        # 🎬 VIDEO YUBORISH SAHIFASI (SIZ SO'RAGAN DEKORATSIYA)
        elif call.data.startswith("get_"):
            parts = call.data.split("_")
            anime_code = parts[1]
            qism_num = parts[2]
            
            if anime_code in ANIMELAR:
                anime_data = ANIMELAR[anime_code]
                if qism_num in anime_data['qismlar']:
                    video_source = anime_data['qismlar'][qism_num]
                    anime_name = anime_data['nomi']
                    
                    # Video tagidagi doimiy chiroyli yozuv:
                    caption_text = (
                        f"🎬 {anime_name}\n"
                        f"📦 {qism_num}-qism\n"
                        f"kanal: @anilebo"
                    )
                    
                    bot.send_video(call.message.chat.id, video_source, caption=caption_text)
                else:
                    bot.answer_callback_query(call.id, "Bu qism videosi hali yuklanmagan! 🚫", show_alert=True)
            
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        print(f"Tugmada xatolik: {e}")

# ----------------- QIDIRUV FUNKSIYALARI -----------------
def search_anime_by_name(message):
    try:
        query = message.text.strip().lower()
        found_animes = {}
        
        for code, anime in ANIMELAR.items():
            if query in anime["nomi"].lower():
                found_animes[code] = anime["nomi"]
                
        if found_animes:
            markup = types.InlineKeyboardMarkup()
            for code, name in found_animes.items():
                markup.add(types.InlineKeyboardButton(name, callback_data=f"view_{code}"))
                
            bot.send_message(
                chat_id=message.chat.id, 
                text=f"*{message.text}* qidiruvi bo'yicha natijalar: 👇", 
                reply_markup=markup,
                parse_mode="Markdown"
            )
        else:
            bot.send_message(message.chat.id, "Anime topilmadi🚫")
            
    except Exception as e:
        bot.send_message(message.chat.id, "Anime topilmadi🚫")

def search_anime_by_code(message):
    try:
        code = message.text.strip()
        
        if code in ANIMELAR:
            photo, caption, markup = generate_anime_view(code)
            bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Anime topilmadi🚫")
            
    except Exception as e:
        bot.send_message(message.chat.id, "Anime topilmadi🚫")

# ----------------- BOTNI ISHLATISH -----------------
print("Bot muvaffaqiyatli ishga tushdi...")

while True:
    try:
        bot.polling(none_stop=True, interval=2, timeout=20)
    except Exception as err:
        time.sleep(5)
                                  
