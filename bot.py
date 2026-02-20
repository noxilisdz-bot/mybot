import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
import io
import os
import threading
from flask import Flask

# ==========================================
# إعدادات البوت
# ==========================================
TOKEN = '8503220872:AAF6Hw3zcB04uoyxWO4VM7H7P5d3KuENMbE'
BOT_USERNAME = '@My_Stories213_bot'
WEBSITE_URL = 'https://qisas-dz.web.app'
SECRET_WORD = 'بيڨاز2003'
# ==========================================

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ==========================================
# خادم Flask لإبقاء Render يعمل 24/24
# ==========================================
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ بوت Noxilis يعمل بنجاح على سيرفر Render!"

def run_web_server():
    # Render يعطينا بورت أوتوماتيكي، إذا لم يجد نستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# تشغيل خادم الويب في خلفية البوت
threading.Thread(target=run_web_server, daemon=True).start()

# ==========================================
# ذاكرة البوت
# ==========================================
admins = []
temp_story = {}

# ==========================================
# أزرار البوت (الكلافي)
# ==========================================
def main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📚 تصفح الموقع"), KeyboardButton("📞 تواصل معنا"))
    
    if user_id in admins:
        markup.add(KeyboardButton("👑 مصنع القصص (Noxilis)"))
    return markup

def cancel_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton("❌ إلغاء العملية"))
    return markup

# ==========================================
# تفاعلات البوت
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبا بيك في بوت الحكايات 🇩🇿✨", reply_markup=main_menu(message.from_user.id))

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id

    # التعامل مع زر الإلغاء
    if text == "❌ إلغاء العملية":
        if chat_id in temp_story:
            del temp_story[chat_id]
            bot.send_message(chat_id, "تم إلغاء العملية 🗑️", reply_markup=main_menu(user_id))
        else:
            bot.send_message(chat_id, "لا توجد عملية لإلغائها.", reply_markup=main_menu(user_id))
        return

    # تفعيل الآدمن السري
    if text == SECRET_WORD:
        if user_id not in admins:
            admins.append(user_id)
            bot.send_message(chat_id, "👑 أهلاً بك سيدي (Noxilis).\nتم تفعيل صلاحيات الآدمن بنجاح 🔒", reply_markup=main_menu(user_id))
        else:
            bot.send_message(chat_id, "أنت ديجا آدمن يا خويا 😎")
            
    elif text == "👑 مصنع القصص (Noxilis)" and user_id in admins:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("➕ إنشاء قصة جديدة", callback_data="create_story"))
        bot.send_message(chat_id, "🛠️ <b>مصنع Noxilis للأكواد:</b>\nهذا المصنع يقوم بتوليد ملفات HTML جاهزة، ومحمية، ومهيئة للـ SEO.", reply_markup=markup)

    elif text == "📚 تصفح الموقع":
        bot.send_message(chat_id, f"أدخل تقرأ كامل الحكايات هنا:\n{WEBSITE_URL}")
        
    elif text == "📞 تواصل معنا":
        bot.send_message(chat_id, "للتواصل مع الإدارة والمطور: Noxilis")

# ==========================================
# نظام مصنع القصص (توليد الأكواد)
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data == "create_story")
def create_story_start(call):
    user_id = call.from_user.id
    if user_id not in admins:
        return
    msg = bot.send_message(call.message.chat.id, "📝 أرسل <b>عنوان</b> القصة:", reply_markup=cancel_menu())
    bot.register_next_step_handler(msg, step_title)

def step_title(message):
    if message.text == "❌ إلغاء العملية": return handle_text(message)
    if not message.text:
        msg = bot.send_message(message.chat.id, "❌ خطأ: يرجى إرسال نص للعنوان وليس شيء آخر:")
        return bot.register_next_step_handler(msg, step_title)

    temp_story[message.chat.id] = {'title': message.text}
    msg = bot.send_message(message.chat.id, "🖼️ أرسل <b>رابط الصورة</b> (URL):", reply_markup=cancel_menu())
    bot.register_next_step_handler(msg, step_image)

def step_image(message):
    if message.text == "❌ إلغاء العملية": return handle_text(message)
    if not message.text:
        msg = bot.send_message(message.chat.id, "❌ خطأ: أرسل رابط الصورة كنص:")
        return bot.register_next_step_handler(msg, step_image)

    temp_story[message.chat.id]['image'] = message.text
    msg = bot.send_message(message.chat.id, "✍️ أرسل <b>مستخلص</b> القصة (سطرين):", reply_markup=cancel_menu())
    bot.register_next_step_handler(msg, step_summary)

def step_summary(message):
    if message.text == "❌ إلغاء العملية": return handle_text(message)
    if not message.text:
        msg = bot.send_message(message.chat.id, "❌ خطأ: أرسل المستخلص كنص:")
        return bot.register_next_step_handler(msg, step_summary)

    temp_story[message.chat.id]['summary'] = message.text
    msg = bot.send_message(message.chat.id, "📜 أرسل <b>نص القصة الكامل</b> (ألصق كل شيء هنا):", reply_markup=cancel_menu())
    bot.register_next_step_handler(msg, step_text)

def step_text(message):
    if message.text == "❌ إلغاء العملية": return handle_text(message)
    if not message.text:
        msg = bot.send_message(message.chat.id, "❌ خطأ: أرسل النص الكامل كرسالة نصية:")
        return bot.register_next_step_handler(msg, step_text)

    chat_id = message.chat.id
    story_data = temp_story[chat_id]
    story_data['text'] = message.text
    story_id = str(random.randint(1000, 9999)) # رقم عشوائي
    
    # 1. تنسيق النص ليناسب HTML
    text_html = "".join([f"<p>{p}</p>" for p in story_data['text'].split('\n') if p.strip()])
    
    # 2. توليد كود HTML الأسطوري مع الـ SEO والحماية
    story_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{story_data['title']} | Noxilis</title>
    
    <!-- إعدادات المشاركة (SEO & Open Graph) -->
    <meta property="og:title" content="{story_data['title']}" />
    <meta property="og:description" content="{story_data['summary']}" />
    <meta property="og:image" content="{story_data['image']}" />
    <meta property="og:type" content="article" />

    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0f172a; --gold: #fbbf24; --text: #f8fafc; --card: #1e293b; }}
        body {{ 
            background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; 
            margin: 0; padding: 20px; line-height: 1.8;
            -webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; 
        }}
        .container {{ max-width: 800px; margin: 0 auto; background: var(--card); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .header-img {{ width: 100%; height: 350px; object-fit: cover; border-radius: 15px; border-bottom: 3px solid var(--gold); margin-bottom: 25px; }}
        h1 {{ color: var(--gold); text-align: center; font-size: 2.2rem; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; text-shadow: 0 0 10px rgba(251,191,36,0.3); }}
        p {{ font-size: 1.2rem; text-align: justify; margin-bottom: 20px; }}
        .btn-back {{ display: block; width: 200px; margin: 40px auto 0; text-align: center; background: linear-gradient(45deg, var(--gold), #f59e0b); color: #000; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 1.1rem; box-shadow: 0 5px 15px rgba(251,191,36,0.3); transition: 0.3s; }}
        .btn-back:hover {{ transform: scale(1.05); }}
        footer {{ text-align: center; margin-top: 40px; color: var(--gold); font-weight: bold; padding: 20px; }}
    </style>
</head>
<body oncontextmenu="return false;">
    <div class="container">
        <!-- تم تصحيح خطأ الأقواس هنا -->
        <img src="{story_data['image']}" class="header-img" alt="{story_data['title']}">
        <h1>{story_data['title']}</h1>
        {text_html}
        <a href="index.html" class="btn-back">العودة للرئيسية ➔</a>
    </div>
    <footer>جميع الحقوق محفوظة &copy; 2026 | تطوير Noxilis</footer>
    
    <script>
        // منع الكليك يمين
        document.addEventListener('contextmenu', event => event.preventDefault());
        
        // منع اختصارات لوحة المفاتيح والنسخ
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey || e.keyCode == 123 || (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 67 || e.keyCode == 74))) {{
                e.preventDefault();
                alert('عذراً! النسخ ممنوع، حقوق Noxilis محفوظة 🔒');
            }}
        }});
        // منع النسخ
        document.addEventListener('copy', function(e) {{
            e.preventDefault();
            alert('النسخ غير مسموح ❌');
        }});
    </script>
</body>
</html>"""

    # 3. إرسال الملف جاهز
    filename = f"story_{story_id}.html"
    html_file = io.BytesIO(story_html.encode('utf-8'))
    html_file.name = filename 
    html_file.seek(0)
    
    bot.send_document(chat_id, html_file, caption=f"✅ <b>تم بناء الملف بنجاح!</b>\nأرفد هذا الملف (`{filename}`) وحطو في موقعك.", reply_markup=main_menu(message.from_user.id))
    
    # 4. توليد كود البطاقة للموقع
    card_html = f"""
        <!-- قصة: {story_data['title']} -->
        <div class="story-card" data-title="{story_data['title']}">
            <div class="img-placeholder" style="background-image: url('{story_data['image']}'); background-size: cover; background-position: center; border-bottom: 3px solid #fbbf24; height: 200px;"></div>
            <div class="content">
                <div class="meta-info">
                    <span>⏱️ جديد</span>
                    <span>👁️ حصري</span>
                </div>
                <h2 class="title">{story_data['title']}</h2>
                <p class="summary">{story_data['summary']}</p>
                <a href="{filename}" class="btn">أقرا الحكاية ➔</a>
            </div>
        </div>"""
    
    bot.send_message(chat_id, "👇 <b>انسخ هذا الكود وحطو في ملف index.html نتاعك:</b>")
    bot.send_message(chat_id, f"```html\n{card_html}\n```", parse_mode="Markdown")
    
    del temp_story[chat_id]

print("✅ البوت خدام 100% بدون أخطاء!")
try:
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
except Exception as e:
    print(f"حدث خطأ: {e}")



