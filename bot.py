import os
import random
import difflib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from telegram.request import HTTPXRequest
from telegram.error import BadRequest, TimedOut, NetworkError

BOT_TOKEN = os.environ["BOT_TOKEN"]

# =========================
# LANGUAGES
# =========================

languages = [
    "Yoruba","Igbo","Hausa","French","Spanish","German","Italian","Portuguese",
    "Arabic","Hindi","Chinese","Japanese","Korean","Russian","Turkish","Swahili",
    "Dutch","Greek","Thai","Vietnamese","Polish","Indonesian","Malay","Persian","Urdu"
]

# =========================
# TRANSLATIONS
# =========================

translations = {
    "How are you?": {
        "Yoruba": "Bawo ni?",
        "Igbo": "Kedu ka ị mere?",
        "Hausa": "Yaya kake?",
        "French": "Comment ça va ?",
        "Spanish": "¿Cómo estás?",
        "German": "Wie geht es dir?",
        "Italian": "Come stai?",
        "Portuguese": "Como você está?",
        "Arabic": "كيف حالك؟",
        "Hindi": "आप कैसे हैं?",
        "Chinese": "你好吗?",
        "Japanese": "元気ですか?",
        "Korean": "어떻게 지내세요?",
        "Russian": "Как дела?",
        "Turkish": "Nasılsın?",
        "Swahili": "Habari yako?",
        "Dutch": "Hoe gaat het met je?",
        "Greek": "Πώς είσαι;",
        "Thai": "คุณเป็นอย่างไรบ้าง?",
        "Vietnamese": "Bạn khỏe không?",
        "Polish": "Jak się masz?",
        "Indonesian": "Apa kabar?",
        "Malay": "Apa khabar?",
        "Persian": "حالت چطوره؟",
        "Urdu": "آپ کیسے ہیں؟"
    },
    "What did you do today?": {
        "Yoruba": "Kí ni o ṣe loni?",
        "Igbo": "Kedu ihe ị mere taa?",
        "Hausa": "Me ka ka yi yau?",
        "French": "Qu'as-tu fait aujourd'hui ?",
        "Spanish": "¿Qué hiciste hoy?",
        "German": "Was hast du heute gemacht?",
        "Italian": "Cosa hai fatto oggi?",
        "Portuguese": "O que você fez hoje?",
        "Arabic": "ماذا فعلت اليوم؟",
        "Hindi": "आपने आज क्या किया?",
        "Chinese": "你今天做了什么?",
        "Japanese": "今日は何をしましたか?",
        "Korean": "오늘 무엇을 했나요?",
        "Russian": "Что ты делал сегодня?",
        "Turkish": "Bugün ne yaptın?",
        "Swahili": "Ulifanya nini leo?",
        "Dutch": "Wat heb je vandaag gedaan?",
        "Greek": "Τι έκανες σήμερα;",
        "Thai": "วันนี้คุณทำอะไรบ้าง?",
        "Vietnamese": "Hôm nay bạn đã làm gì?",
        "Polish": "Co robiłeś dzisiaj?",
        "Indonesian": "Apa yang kamu lakukan hari ini?",
        "Malay": "Apa yang awak buat hari ini?",
        "Persian": "امروز چیکار کردی؟",
        "Urdu": "آپ نے آج کیا کیا؟"
    },
    "Complete: I ___ happy.": {
        "Yoruba": "Parí gbolohun yii: Mo ___ dun.",
        "Igbo": "Mezuo ahịrịokwu a: I ___ obi ụtọ.",
        "Hausa": "Cika wannan jimla: Ina ___ farin ciki.",
        "French": "Complète : Je suis ___ heureux.",
        "Spanish": "Completa: Yo ___ feliz.",
        "German": "Vervollständige: Ich ___ glücklich.",
        "Italian": "Completa: Io ___ felice.",
        "Portuguese": "Complete: Eu ___ feliz.",
        "Arabic": "أكمل: أنا ___ سعيد.",
        "Hindi": "पूरा करें: मैं ___ खुश हूँ।",
        "Chinese": "完成句子:我___很高兴。",
        "Japanese": "完成させてください:私は___幸せです。",
        "Korean": "완성하세요: 나는 ___ 행복하다.",
        "Russian": "Заполни пропуск: Я ___ счастлив.",
        "Turkish": "Tamamla: Ben ___ mutluyum.",
        "Swahili": "Kamilisha: Mimi ni ___ furaha.",
        "Dutch": "Maak af: Ik ben ___ blij.",
        "Greek": "Συμπλήρωσε: Είμαι ___ χαρούμενος.",
        "Thai": "เติมให้สมบูรณ์: ฉัน ___ มีความสุข",
        "Vietnamese": "Hoàn thành: Tôi ___ vui.",
        "Polish": "Uzupełnij: Jestem ___ szczęśliwy.",
        "Indonesian": "Lengkapi: Saya ___ senang.",
        "Malay": "Lengkapkan: Saya ___ gembira.",
        "Persian": "کامل کن: من ___ خوشحالم.",
        "Urdu": "مکمل کریں: میں ___ خوش ہوں۔"
    },
    "What is the opposite of big?": {
        "Yoruba": "Kí ni idakeji 'big'?",
        "Igbo": "Gịnị bụ ihe megidere 'big'?",
        "Hausa": "Menene akasin 'big'?",
        "French": "Quel est le contraire de « grand » ?",
        "Spanish": "¿Cuál es el opuesto de \"grande\"?",
        "German": "Was ist das Gegenteil von \"groß\"?",
        "Italian": "Qual è il contrario di \"grande\"?",
        "Portuguese": "Qual é o oposto de \"grande\"?",
        "Arabic": "ما عكس كلمة \"كبير\"؟",
        "Hindi": "\"बड़ा\" का विपरीत क्या है?",
        "Chinese": "\"大\"的反义词是什么?",
        "Japanese": "「大きい」の反対は何ですか?",
        "Korean": "\"큰\"의 반대말은 무엇인가요?",
        "Russian": "Какое слово противоположно \"большой\"?",
        "Turkish": "\"Büyük\" kelimesinin zıttı nedir?",
        "Swahili": "Kinyume cha \"kubwa\" ni nini?",
        "Dutch": "Wat is het tegenovergestelde van \"groot\"?",
        "Greek": "Ποιο είναι το αντίθετο του \"μεγάλος\";",
        "Thai": "คำตรงข้ามของ \"ใหญ่\" คืออะไร?",
        "Vietnamese": "Từ trái nghĩa của \"lớn\" là gì?",
        "Polish": "Jakie jest przeciwieństwo słowa \"duży\"?",
        "Indonesian": "Apa lawan kata dari \"besar\"?",
        "Malay": "Apakah lawan kata bagi \"besar\"?",
        "Persian": "متضاد \"بزرگ\" چیست؟",
        "Urdu": "\"بڑا\" کا مخالف کیا ہے؟"
    },
    "Change to past: I go to school.": {
        "Yoruba": "Yi pada si igba atijo: I go to school.",
        "Igbo": "Gbanwee gaa oge gara aga: I go to school.",
        "Hausa": "Canza zuwa baya: I go to school.",
        "French": "Mets au passé : I go to school.",
        "Spanish": "Cambia al pasado: I go to school.",
        "German": "Ändere ins Präteritum: I go to school.",
        "Italian": "Cambia al passato: I go to school.",
        "Portuguese": "Mude para o passado: I go to school.",
        "Arabic": "غيّر إلى الماضي: I go to school.",
        "Hindi": "भूतकाल में बदलें: I go to school.",
        "Chinese": "改为过去式:I go to school.",
        "Japanese": "過去形にしてください:I go to school.",
        "Korean": "과거형으로 바꾸세요: I go to school.",
        "Russian": "Измени на прошедшее время: I go to school.",
        "Turkish": "Geçmiş zamana çevir: I go to school.",
        "Swahili": "Badilisha kuwa wakati uliopita: I go to school.",
        "Dutch": "Verander naar de verleden tijd: I go to school.",
        "Greek": "Άλλαξέ το σε παρελθόντα χρόνο: I go to school.",
        "Thai": "เปลี่ยนเป็นอดีตกาล: I go to school.",
        "Vietnamese": "Đổi sang thì quá khứ: I go to school.",
        "Polish": "Zmień na czas przeszły: I go to school.",
        "Indonesian": "Ubah ke bentuk lampau: I go to school.",
        "Malay": "Tukar kepada bentuk lampau: I go to school.",
        "Persian": "به زمان گذشته تغییر بده: I go to school.",
        "Urdu": "ماضی میں تبدیل کریں: I go to school."
    },
    "Describe your future goals.": {
        "Yoruba": "Ṣàpèjúwe awọn ibi-afẹde ọjọ iwaju rẹ.",
        "Igbo": "Kọwaa ebumnuche gị n'ọdịnihu.",
        "Hausa": "Bayyana burinka na gaba.",
        "French": "Décris tes objectifs futurs.",
        "Spanish": "Describe tus metas futuras.",
        "German": "Beschreibe deine Zukunftsziele.",
        "Italian": "Descrivi i tuoi obiettivi futuri.",
        "Portuguese": "Descreva seus objetivos futuros.",
        "Arabic": "صف أهدافك المستقبلية.",
        "Hindi": "अपने भविष्य के लक्ष्यों का वर्णन करें।",
        "Chinese": "描述你未来的目标。",
        "Japanese": "あなたの将来の目標を説明してください。",
        "Korean": "당신의 미래 목표를 설명하세요.",
        "Russian": "Опиши свои будущие цели.",
        "Turkish": "Gelecekteki hedeflerini anlat.",
        "Swahili": "Eleza malengo yako ya baadaye.",
        "Dutch": "Beschrijf je toekomstige doelen.",
        "Greek": "Περιέγραψε τους μελλοντικούς σου στόχους.",
        "Thai": "อธิบายเป้าหมายในอนาคตของคุณ",
        "Vietnamese": "Mô tả mục tiêu tương lai của bạn.",
        "Polish": "Opisz swoje przyszłe cele.",
        "Indonesian": "Jelaskan tujuan masa depanmu.",
        "Malay": "Terangkan matlamat masa depan awak.",
        "Persian": "اهداف آینده‌ات را توصیف کن.",
        "Urdu": "اپنے مستقبل کے اہداف بیان کریں۔"
    }
}

levels_order = ["beginner", "intermediate", "advanced"]

lessons = {
    "beginner": [
        {"q": "How are you?", "a": None},
        {"q": "Complete: I ___ happy.", "a": "am"},
        {"q": "What is the opposite of big?", "a": "small"}
    ],
    "intermediate": [
        {"q": "What did you do today?", "a": None},
        {"q": "Change to past: I go to school.", "a": "I went to school"}
    ],
    "advanced": [
        {"q": "Describe your future goals.", "a": None},
        {"q": "Explain your opinion about technology.", "a": None}
    ]
}

# =========================
# MULTI USER STORAGE (in memory, per Telegram user id)
# =========================
users = {}


def new_user_state():
    return {
        "stage": "choose_language",   # choose_language -> choose_level -> choose_style -> lesson -> chat
        "language": None,
        "level": None,
        "style": None,
        "score": 0,
        "total_questions": 0,
        "level_index": 0,
        "question_index": 0
    }


def is_close(user_input, correct_answer):
    similarity = difflib.SequenceMatcher(None, user_input.lower(), correct_answer.lower()).ratio()
    return similarity >= 0.75


def teacher_reply(style, correct=None):
    if style == "friendly":
        if correct:
            return f"Great job! 😊 Correct answer: {correct}"
        return random.choice(["Nice try 😊", "Good effort 💪", "Keep going 🚀"])
    else:
        if correct:
            return f"Correction: {correct}"
        return random.choice(["Try again.", "Focus more.", "Improve your answer."])


def chat_brain(msg):
    msg = msg.lower()
    if "hello" in msg or "hi" in msg:
        return "Hello! 😊"
    if "how are you" in msg:
        return "I'm here to help you learn English!"
    if len(msg.split()) < 3:
        return "Try making a longer sentence."
    return random.choice(["Nice sentence!", "Good, keep practicing!", "You're improving!"])


def question_text(state, item):
    q = item["q"]
    lang = state["language"]
    text = f"Teacher: {q}\n👉 Please answer in English."
    if q in translations and lang in translations[q]:
        text += f"\n\n{lang}: {translations[q][lang]}"
    return text


async def send_question(update_or_query, context, state, chat_id):
    level = levels_order[state["level_index"]]
    lesson = lessons[level]
    item = lesson[state["question_index"]]
    text = question_text(state, item)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = new_user_state()

    keyboard = []
    row = []
    for i, lang in enumerate(languages, 1):
        row.append(InlineKeyboardButton(lang, callback_data=f"lang|{lang}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await update.message.reply_text(
        "🌍 Welcome to Crystal Language AI ✨\nYour personal English learning teacher.\n\nChoose your language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id

    try:
        await query.answer()
    except (BadRequest, TimedOut, NetworkError):
        # The tap arrived too late / query expired. Ignore and let the user try again.
        try:
            await context.bot.send_message(chat_id=chat_id, text="That button expired — please tap the latest option again.")
        except Exception:
            pass
        return

    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = new_user_state()
    state = users[user_id]

    data = query.data

    try:
        if data.startswith("lang|"):
            state["language"] = data.split("|", 1)[1]
            state["stage"] = "choose_level"
            keyboard = [
                [InlineKeyboardButton("Beginner", callback_data="level|beginner")],
                [InlineKeyboardButton("Intermediate", callback_data="level|intermediate")],
                [InlineKeyboardButton("Advanced", callback_data="level|advanced")]
            ]
            await query.edit_message_text(
                f"Language set to {state['language']} ✅\n\nChoose your starting English level:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data.startswith("level|"):
            state["level"] = data.split("|", 1)[1]
            state["level_index"] = levels_order.index(state["level"])
            state["stage"] = "choose_style"
            keyboard = [
                [InlineKeyboardButton("Friendly 😊", callback_data="style|friendly")],
                [InlineKeyboardButton("Strict 📚", callback_data="style|strict")]
            ]
            await query.edit_message_text(
                f"Level set to {state['level']} ✅\n\nChoose teacher style:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data.startswith("style|"):
            state["style"] = data.split("|", 1)[1]
            state["stage"] = "lesson"
            state["question_index"] = 0

            await query.edit_message_text(
                f"Mode set to {state['style']} ✅\n\nNice to meet you, {update.effective_user.first_name}! 🚀\n"
                f"Language: {state['language']} | Level: {state['level']} | Mode: {state['style']}"
            )

            level = levels_order[state["level_index"]]
            await context.bot.send_message(chat_id=chat_id, text=f"📚 Starting {level.upper()} lesson...")
            await send_question(update, context, state, chat_id)

    except (BadRequest, TimedOut, NetworkError) as e:
        try:
            await context.bot.send_message(chat_id=chat_id, text="Something timed out — please tap the button again or send /start to restart.")
        except Exception:
            pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await _handle_message_inner(update, context)
    except (BadRequest, TimedOut, NetworkError):
        try:
            await update.message.reply_text("Something timed out — please send your last message again.")
        except Exception:
            pass


async def _handle_message_inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Send /start to begin your English lesson!")
        return

    state = users[user_id]

    if state["stage"] != "lesson" and state["stage"] != "chat":
        await update.message.reply_text("Please choose an option above first 👆")
        return

    if state["stage"] == "chat":
        await update.message.reply_text(f"Teacher: {chat_brain(text)}")
        return

    # stage == "lesson"
    level = levels_order[state["level_index"]]
    lesson = lessons[level]
    item = lesson[state["question_index"]]
    state["total_questions"] += 1

    if item["a"]:
        if is_close(text, item["a"]):
            state["score"] += 10
            await update.message.reply_text(teacher_reply(state["style"]))
            if text.lower() != item["a"].lower():
                if state["style"] == "friendly":
                    await update.message.reply_text(f"😊 Nice try, but the correct answer is: {item['a']}")
                else:
                    await update.message.reply_text(f"Correction: {item['a']}")
        else:
            await update.message.reply_text(teacher_reply(state["style"], item["a"]))
    else:
        await update.message.reply_text(teacher_reply(state["style"]))

    state["question_index"] += 1

    if state["question_index"] >= len(lesson):
        await update.message.reply_text(f"✅ {level.upper()} level completed!")
        state["level_index"] += 1
        state["question_index"] = 0

        if state["level_index"] >= len(levels_order):
            total = state["total_questions"] * 10
            percentage = (state["score"] / total) * 100 if total else 0

            result_text = f"📊 YOUR RESULTS\nScore: {state['score']} / {total}\n"
            if percentage >= 80:
                result_text += "🏆 Excellent performance!"
            elif percentage >= 50:
                result_text += "👍 Good job, keep improving!"
            else:
                result_text += "📚 Keep practicing, you will improve!"

            await update.message.reply_text(result_text)
            await update.message.reply_text("🎉 All levels completed! Chat mode activated. Just type to chat with the teacher.")
            state["stage"] = "chat"
        else:
            next_level = levels_order[state["level_index"]]
            await update.message.reply_text(f"📚 Starting {next_level.upper()} lesson...")
            await send_question(update, context, state, chat_id)
    else:
        await send_question(update, context, state, chat_id)


request = HTTPXRequest(connect_timeout=30, read_timeout=30, connection_pool_size=8)
app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling(drop_pending_updates=True)
