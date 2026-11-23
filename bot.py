import uiautomator2 as u2
import requests
import time
import sys
import os

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي (أندرويد 11)...")
    
    try:
        d = u2.connect("127.0.0.1:5555")
        send_msg("✅ تم الاتصال بالهاتف بنجاح.")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # 1. تحميل وتثبيت متجر بلاي
    send_msg("⏳ جاري تحميل وتثبيت متجر Google Play...")
    apk_url = "https://github.com/Team-Kujang/PlayStore/raw/main/PlayStore.apk"
    apk_path = "/tmp/playstore.apk"
    
    try:
        r = requests.get(apk_url)
        with open(apk_path, 'wb') as f:
            f.write(r.content)
        
        # تثبيت APK باستخدام ADB
        os.system(f"adb install {apk_path}")
        send_msg("✅ تم تثبيت متجر بلاي بنجاح.")
    except Exception as e:
        send_msg(f"❌ فشل تثبيت متجر بلاي: {str(e)}")

    # 2. فتح متجر بلاي
    send_msg("🛒 جاري فتح متجر بلاي...")
    d.app_start("com.android.vending")
    time.sleep(10)
    
    # 3. أخذ صورة وإرسالها
    d.screenshot("/tmp/playstore_final.png")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/playstore_final.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    send_msg("🎉 انتهت التجربة. متجر بلاي يجب أن يكون مفتوحاً الآن.")
    
if __name__ == "__main__":
    main()
