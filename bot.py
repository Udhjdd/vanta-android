import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي (أندرويد 10)...")
    
    try:
        d = u2.connect("127.0.0.1:5555")
        send_msg("✅ تم الاتصال بالهاتف بنجاح.")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # فتح متجر بلاي
    send_msg("🛒 جاري فتح متجر بلاي...")
    try:
        d.app_start("com.android.vending")
        time.sleep(10)
    except:
        send_msg("⚠️ لم يتم العثور على متجر بلاي، سأفتح المتصفح.")
        d.app_start("com.android.chrome")
        time.sleep(5)

    # أخذ صورة وإرسالها
    d.screenshot("/tmp/result.png")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/result.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    send_msg("🎉 انتهت التجربة.")
    
if __name__ == "__main__":
    main()
