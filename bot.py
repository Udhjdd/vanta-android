import uiautomator2 as u2
import requests
import time
import sys
import os

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا للتجربة
EMAIL = "YOUR_EMAIL_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي على GitHub Actions...")
    
    try:
        d = u2.connect("127.0.0.1:5555")
        send_msg("✅ تم الاتصال بالهاتف بنجاح.")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # 1. فتح متجر بلاي
    send_msg("🛒 جاري فتح متجر بلاي...")
    d.app_start("com.android.vending")
    time.sleep(5)
    
    # ملاحظة: الخطوات التالية (تسجيل الدخول، الـ VPN، تفعيل النقاط)
    # سنقوم بإضافتها لاحقاً بعد التأكد من أن الهاتف يعمل.
    
    send_msg("🎉 انتهت التجربة الأولية.")
    d.screenshot("/tmp/result.png")
    
    # إرسال الصورة لك على تيليجرام
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/result.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

if __name__ == "__main__":
    main()
