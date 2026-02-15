import telebot, requests, os

# توكن مصلح
bot = telebot.TeleBot("7684676625:AAEl4kHBZ9zs3zfR7Xd1QCi-slZb6hMslO0")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "هلا مصلح! جاري تجربة المحرك الجديد.. أرسل رابط تيك توك.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "انتظر يا مصلح، جاري تجربة طريق بديل... 🚀")
        try:
            # محرك جديد (Cobalt) - أسرع وأحياناً يتخطى قيود المواقع المجانية
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            data = {"url": url, "vQuality": "720"}
            
            res = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers).json()
            
            if "url" in res:
                video_url = res['url']
                video_data = requests.get(video_url).content
                with open("v.mp4", "wb") as f: f.write(video_data)
                with open("v.mp4", "rb") as v: bot.send_video(message.chat.id, v)
                os.remove("v.mp4")
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ الموقع مقيد حالياً، جرب رابط تيك توك (غالباً أسهل).", message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ يا مصلح، السيرفر المجاني يمنع الاتصال بالمصدر. جرب رابطاً مختلفاً.", message.chat.id, msg.message_id)

bot.polling()
