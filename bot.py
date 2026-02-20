import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random

# ==========================================
TOKEN = '8503220872:AAF6Hw3zcB04uoyxWO4VM7H7P5d3KuENMbE'
BOT_USERNAME = '@My_Stories213_bot'
WEBSITE_URL = 'https://qisas-dz.web.app'
# ==========================================

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# القصص الحقيقية مع ملخص 10 كلمات فقط
stories_database = [
    {
        "id": "1",
        "title": "مسمار جحا",
        "category": "ذكاء",
        "summary": "باع جحا بيته واشترط بقاء مسمار له فيه، فماذا حدث؟",
        "url": f"{WEBSITE_URL}/story1.html"
    },
    {
        "id": "2",
        "title": "بائعة الكبريت",
        "category": "عالمية",
        "summary": "طفلة فقيرة تبيع الكبريت في ليلة شتاء باردة، قصة مؤثرة.",
        "url": f"{WEBSITE_URL}/story2.html"
    }
]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📚 تصفح القصص"), KeyboardButton("🎲 قصة عشوائية"))
    markup.add(KeyboardButton("🌐 موقعنا الرسمي"), KeyboardButton("📞 تواصل معنا"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"أهلاً <b>{user_name}</b> في {BOT_USERNAME} ✨\n\nنقدم لك قصصاً حقيقية وممتعة، اختر من القائمة بالأسفل:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "🎲 قصة عشوائية" or text == "📚 تصفح القصص":
        # عرض القصص بتنسيق قصير جداً (عنوان + 10 كلمات + زر)
        if text == "🎲 قصة عشوائية":
            stories_to_show = [random.choice(stories_database)]
        else:
            stories_to_show = stories_database

        for story in stories_to_show:
            story_text = f"📖 <b>{story['title']}</b>\n\n📝 <i>{story['summary']}</i>"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔗 لقراءة القصة كاملة اضغط هنا", url=story['url']))
            bot.send_message(chat_id, story_text, reply_markup=markup)

    elif text == "🌐 موقعنا الرسمي":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚀 فتح الموقع", url=WEBSITE_URL))
        bot.send_message(chat_id, "تصفح جميع قصصنا عبر موقعنا الرسمي:", reply_markup=markup)
        
    elif text == "📞 تواصل معنا":
        bot.send_message(chat_id, "للتواصل مع إدارة الموقع والبوت: @telegram")
    else:
        bot.send_message(chat_id, "استخدم الأزرار السفلية 👇", reply_markup=main_menu())

print(f"✅ تم تشغيل البوت بالقصص الحقيقية!")
try:
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
except Exception as e:
    print(f"حدث خطأ: {e}")



