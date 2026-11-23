import uiautomator2 as u2
import requests
import time
import sys
import os

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا للتجربة
EMAIL = "ssda73410@gmail.com"
PASSWORD = "fawazfawaz123@"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي (محاكي Google الرسمي)...")
    
    try:
        d = u2.connect("127.0.0.1:5555")
        send_msg("✅ تم الاتصال بالهاتف بنجاح.")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # 1. فتح متجر بلاي
    send_msg("🛒 جاري فتح متجر بلاي...")
    d.app_start("com.android.vending")
    time.sleep(10)

    # 2. الضغط على SIGN IN
    if d(text="SIGN IN").exists:
        send_msg("🔑 تم العثور على زر تسجيل الدخول. جاري الضغط...")
        d(text="SIGN IN").click()
        time.sleep(5)
    else:
        send_msg("⚠️ لم يتم العثور على زر SIGN IN. قد يكون المتجر مفتوحاً بالفعل.")
        d.screenshot("/tmp/store.png")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open("/tmp/store.png", "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})
        return

    # 3. إدخال الإيميل (نحتاج لمعرفة الواجهة التي ستظهر)
    # هذه الخطوات تعتمد على واجهة جوجل، قد نحتاج لتعديلها
    send_msg("📧 جاري إدخال الإيميل...")
    # ... (سنضيف كود الإدخال هنا بعد أن نرى الصورة التالية)
    
    # أخذ صورة للنتيجة
    d.screenshot("/tmp/login.png")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/login.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    send_msg("🎉 انتهت التجربة. جاري الانتظار للخطوة التالية.")
    
if __name__ == "__main__":
    main()
