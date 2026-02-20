# استدعاء المكتبات
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineQueryResultArticle, InputTextMessageContent
import random

# ==========================================
TOKEN = '8503220872:AAF6Hw3zcB04uoyxWO4VM7H7P5d3KuENMbE'
BOT_USERNAME = '@My_Stories213_bot'
WEBSITE_URL = 'https://qisas-dz.web.app'
# ==========================================

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# قاعدة بيانات القصص (مع إضافة صور مصغرة للبحث المضمن)
stories_database = [
    {
        "id": "1",
        "title": "مسمار جحا",
        "category": "ذكاء",
        "summary": "باع جحا دارو وشرط يخلي مسمار تاعو فيها، شوف واش صرا في لخر!",
        "url": f"{WEBSITE_URL}/story1.html",
        "thumb_url": "https://cdn-icons-png.flaticon.com/512/3069/3069172.png"
    },
    {
        "id": "2",
        "title": "بائعة الكبريت",
        "category": "عالمية",
        "summary": "طفلة فقيرة تبيع الكبريت في ليلة شتا باردة، قصة تبكي الحجر.",
        "url": f"{WEBSITE_URL}/story2.html",
        "thumb_url": "https://cdn-icons-png.flaticon.com/512/3224/3224424.png"
    }
]

# الكلافي تاع البوت
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📚 تصفح الحكايات"), KeyboardButton("🎲 حكاية زهر"))
    markup.add(KeyboardButton("🌐 السيت نتاعنا"), KeyboardButton("🔗 بارطاجي البوت"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"مرحبا بيك <b>{user_name}</b> في بوت {BOT_USERNAME} 🇩🇿✨\n\n"
        "أقوى بوت تاع حكايات وقصص. تقدر تقرا، تقيّم، وتبارطاجي مع أصحابك!\n"
        "👇 خيّر واش راك حاب دير:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "🎲 حكاية زهر" or text == "📚 تصفح الحكايات":
        stories_to_show = [random.choice(stories_database)] if text == "🎲 حكاية زهر" else stories_database

        for story in stories_to_show:
            story_text = f"📖 <b>{story['title']}</b>\n\n📝 <i>{story['summary']}</i>"
            markup = InlineKeyboardMarkup(row_width=2)
            # زر القراءة
            btn_read = InlineKeyboardButton("🔗 أقرا الحكاية كاملة", url=story['url'])
            # أزرار التقييم
            btn_like = InlineKeyboardButton("👍 فور", callback_data="rate_up")
            btn_dislike = InlineKeyboardButton("👎 عيانة", callback_data="rate_down")
            
            markup.add(btn_read)
            markup.add(btn_like, btn_dislike)
            
            bot.send_message(chat_id, story_text, reply_markup=markup)

    elif text == "🌐 السيت نتاعنا":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚀 أدخل للسيت (Dark/Light Mode)", url=WEBSITE_URL))
        bot.send_message(chat_id, "أدخل تقرأ كامل الحكايات في السيت نتاعنا الجديد والأسطوري:", reply_markup=markup)
        
    elif text == "🔗 بارطاجي البوت":
        share_text = f"أقرا أحلى القصص في هذا البوت الخرافي: {BOT_USERNAME}"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📤 أرسل لصاحبك", url=f"https://t.me/share/url?url={BOT_USERNAME}&text={share_text}"))
        bot.send_message(chat_id, "شارك البوت مع أصحابك باش تكبر اللمة! 🤩", reply_markup=markup)
        
    else:
        bot.send_message(chat_id, "استعمل الأزرار لي لتحت خويا 👇", reply_markup=main_menu())

# نظام التقييم (عند الضغط على 👍 أو 👎)
@bot.callback_query_handler(func=lambda call: call.data.startswith('rate_'))
def handle_rating(call):
    if call.data == "rate_up":
        bot.answer_callback_query(call.id, "يعطيك الصحة! فرحتنا لي عجباتك الحكاية 😍", show_alert=True)
    elif call.data == "rate_down":
        bot.answer_callback_query(call.id, "معليش، نوعدوك نجيبولك حكايات خير منها المرة الجاية 🫡", show_alert=True)

# الميزة الخرافية: البحث المضمن (Inline Query)
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    results = []
    search_text = query.query.lower()
    
    for story in stories_database:
        if search_text in story['title'].lower() or search_text in story['summary'].lower():
            # تجهيز النتيجة لي تخرج في البحث
            msg_content = InputTextMessageContent(f"📖 <b>{story['title']}</b>\n\n📝 <i>{story['summary']}</i>\n\n🔗 أقراها هنا: {story['url']}", parse_mode="HTML")
            
            item = InlineQueryResultArticle(
                id=story['id'],
                title=story['title'],
                description=story['summary'],
                input_message_content=msg_content,
                thumbnail_url=story['thumb_url'],
                thumbnail_width=50,
                thumbnail_height=50
            )
            results.append(item)
            
    bot.answer_inline_query(query.id, results)

print("✅ البوت الخرافي راهو خدام (بميزة الإنلاين والتقييم)!")
try:
    bot.infinity_polling()
except Exception as e:
    print(f"مشكل: {e}")



