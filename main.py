import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ১. Render-কে Active রাখার জন্য Flask Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# ২. Telegram Bot Setup
# BotFather থেকে পাওয়া আপনার অরিজিনাল বট টোকেনটি এখানে বসাবেন
BOT_TOKEN = 8662076126:AAF-3f9Qwg6AujM9c-qE99QLUl_Quv0uuEA
bot = telebot.TeleBot(BOT_TOKEN)

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    
    # ফুড মেনু বাটন
    btn1 = InlineKeyboardButton("🍕 Burger - ৳180", callback_data="order_burger")
    btn2 = InlineKeyboardButton("🍕 Pizza - ৳350", callback_data="order_pizza")
    markup.add(btn1, btn2)
    
    bot.reply_to(
        message, 
        f"স্বাগতম {message.from_user.first_name}!\nআমাদের ফুড ডেলিভারি সার্ভিস থেকে কি পেতে চান নিচে নির্বাচন করুন:", 
        reply_markup=markup
    )

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "order_burger":
        bot.answer_callback_query(call.id, "বার্গার সিলেক্ট করা হয়েছে!")
        bot.send_message(call.message.chat.id, "🍔 বার্গার অর্ডার নিশ্চিত করতে আপনার ডেলিভারি এড্রেস ও ফোন নম্বর লিখুন:")
    elif call.data == "order_pizza":
        bot.answer_callback_query(call.id, "পিজ্জা সিলেক্ট করা হয়েছে!")
        bot.send_message(call.message.chat.id, "🍕 পিজ্জা অর্ডার নিশ্চিত করতে আপনার ডেলিভারি এড্রেস ও ফোন নম্বর লিখুন:")

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে Flask সার্ভার চালু করা
    threading.Thread(target=run_flask).start()
    
    # টেলিগ্রাম বট স্টার্ট করা
    bot.infinity_polling()
