import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا
EMAIL = "YOUR_EMAIL_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def take_screenshot(d, caption):
    path = f"/tmp/{caption.replace(' ', '_')}.png"
    d.screenshot(path)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": f})

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي...")
    
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
    take_screenshot(d, "1. فتح متجر بلاي")

    # 2. الضغط على SIGN IN
    if d(text="SIGN IN").exists:
        d(text="SIGN IN").click()
        time.sleep(10)
        take_screenshot(d, "2. شاشة تسجيل الدخول")
    else:
        send_msg("⚠️ لم يتم العثور على زر SIGN IN.")
        return

    # 3. إدخال الإيميل
    send_msg("📧 جاري إدخال الإيميل...")
    if d(className="android.widget.EditText").exists(timeout=30):
        d(className="android.widget.EditText").set_text(EMAIL)
        time.sleep(2)
        take_screenshot(d, "3. بعد إدخال الإيميل")
        
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
            
        time.sleep(10)
    else:
        send_msg("⚠️ لم تظهر خانة الإيميل.")
        return

    # 4. إدخال كلمة المرور
    send_msg("🔑 جاري إدخال كلمة المرور...")
    if d(className="android.widget.EditText").exists(timeout=10):
        d(className="android.widget.EditText").set_text(PASSWORD)
        time.sleep(2)
        take_screenshot(d, "4. بعد إدخال الباسورد")
        
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
            
        time.sleep(15)
    else:
        send_msg("⚠️ لم تظهر خانة كلمة المرور.")
        return

    # 5. التعامل مع 2FA
    if d(text="Tap Yes on your phone or tablet").exists or d(text="Tap Yes").exists:
        send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على (Tap Yes)...")
        if d(text="Tap Yes on your phone or tablet").exists:
            d(text="Tap Yes on your phone or tablet").click()
        else:
            d(text="Tap Yes").click()
            
        take_screenshot(d, "5. شاشة التحقق (2FA)")
        send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل لتأكيد الدخول.** (لديك 30 ثانية)...")
        time.sleep(30)
        
        # صورة بعد التأكيد
        take_screenshot(d, "6. بعد تأكيد 2FA")
        
    else:
        send_msg("⚠️ لم تظهر شاشة Tap Yes. قد يكون الدخول تم مباشرة أو هناك خطأ.")

    # التقاط صورة نهائية
    take_screenshot(d, "7. النتيجة النهائية بعد الدخول")
    send_msg("🎉 انتهت عملية تسجيل الدخول. راجع الصور سيدي.")
    
if __name__ == "__main__":
    main()
