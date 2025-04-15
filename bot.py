import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
import asyncio
import os

API_TOKEN = os.getenv("8151839888:AAFSKa2K6Ns8wAG8wLhJY1JbUIFmz1ylkgk")
bot = Bot(token=8151839888:AAFSKa2K6Ns8wAG8wLhJY1JbUIFmz1ylkgk)
dp = Dispatcher(bot)

# تحميل بيانات المستخدمين
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_id = str(msg.from_user.id)
    if user_id not in users:
        users[user_id] = {"coins": 0, "daily_claimed": False, "ref": None}
        if " " in msg.text:
            ref = msg.text.split()[1]
            if ref != user_id and ref in users:
                users[ref]["coins"] += 10
                await msg.answer(f"تمت إضافة 10 كوين لصديقك {ref} لدعوتك.")
                users[user_id]["ref"] = ref
        save_users()
    await msg.answer("مرحباً بك في كوين بوت!
استخدم /daily للحصول على كوين يومي.")

@dp.message_handler(commands=["daily"])
async def daily(msg: types.Message):
    user_id = str(msg.from_user.id)
    if not users[user_id]["daily_claimed"]:
        users[user_id]["coins"] += 5
        users[user_id]["daily_claimed"] = True
        save_users()
        await msg.answer("أخذت 5 كوين! ارجع بكرة تحصل غيرها.")
    else:
        await msg.answer("أنت أخذت مكافأتك اليوم! ارجع بكرة.")

@dp.message_handler(commands=["profile"])
async def profile(msg: types.Message):
    user_id = str(msg.from_user.id)
    coins = users[user_id]["coins"]
    await msg.answer(f"رصيدك: {coins} كوين.")

@dp.message_handler(commands=["invite"])
async def invite(msg: types.Message):
    user_id = str(msg.from_user.id)
    await msg.answer(f"شارك الرابط التالي لدعوة أصدقائك:
https://t.me/YOUR_BOT_USERNAME?start={user_id}")

@dp.message_handler(commands=["reset_daily"])
async def reset_all_daily(msg: types.Message):
    if str(msg.from_user.id) == "YOUR_TELEGRAM_ID":
        for u in users:
            users[u]["daily_claimed"] = False
        save_users()
        await msg.answer("تم إعادة تعيين المكافأة اليومية للجميع.")

if __name__ == "__main__":
    executor.start_polling(dp)
