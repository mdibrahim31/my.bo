import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ১. Render Active রাখার জন্য Flask Web App
app = Flask(__name__)

@app.route('/')
def home():
    return "Food Delivery Bot is Running 24/7!"

# ২. Telegram Bot Setup
BOT_TOKEN = "8662076126:AAF-3f9Qwg6AujM9c-qE99QLUl_Quv0uuEA" 
bot = telebot.TeleBot(BOT_TOKEN)

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    
    # ফুড মেনু বাটন
    btn1 = InlineKeyboardButton("🍔 Burger - ৳180", callback_data="order_burger")
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

# ব্যাকগ্রাউন্ডে টেলিগ্রাম বটের Polling রান করা
def run_bot():
    bot.infinity_polling(skip_pending=True)

# থ্রেড চালনা
polling_thread = threading.Thread(target=run_bot)
polling_thread.daemon = True
polling_thread.start()
