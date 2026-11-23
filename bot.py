import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا
EMAIL = "ssda73410@gmail.com"
PASSWORD = "fawazfawaz123@"

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

    # 2. الضغط على SIGN IN
    if d(text="SIGN IN").exists:
        d(text="SIGN IN").click()
        send_msg("⏳ جاري الانتظار حتى تظهر خانة الإيميل...")
    else:
        send_msg("⚠️ لم يتم العثور على زر SIGN IN.")
        return

    # 3. إدخال الإيميل (انتظار ذكي)
    email_field = d(className="android.widget.EditText")
    if email_field.wait(timeout=30): # ينتظر حتى 30 ثانية حتى يظهر الحقل
        time.sleep(2) # انتظار إضافي بسيط لضمان جاهزية لوحة المفاتيح
        send_msg("📧 تم العثور على خانة الإيميل. جاري الكتابة...")
        email_field.click()
        time.sleep(1)
        email_field.clear_text()
        email_field.set_text(EMAIL)
        time.sleep(2)
        take_screenshot(d, "2. بعد إدخال الإيميل")
        
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
            
    else:
        send_msg("⚠️ لم تظهر خانة الإيميل بعد 30 ثانية.")
        take_screenshot(d, "خطأ - لم تظهر خانة الإيميل")
        return

    # 4. إدخال كلمة المرور (انتظار ذكي)
    send_msg("🔑 جاري الانتظار حتى تظهر خانة كلمة المرور...")
    password_field = d(className="android.widget.EditText")
    if password_field.wait(timeout=30):
        time.sleep(2) # انتظار لضمان جاهزية الشاشة
        send_msg("🔑 تم العثور على خانة الباسورد. جاري الكتابة...")
        password_field.click()
        time.sleep(1)
        password_field.clear_text()
        password_field.set_text(PASSWORD)
        time.sleep(2)
        take_screenshot(d, "3. بعد إدخال الباسورد")
        
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
            
        time.sleep(15)
    else:
        send_msg("⚠️ لم تظهر خانة كلمة المرور بعد 30 ثانية.")
        take_screenshot(d, "خطأ - لم تظهر خانة كلمة المرور")
        return

    # 5. التعامل مع 2FA
    if d(text="Tap Yes on your phone or tablet").exists or d(text="Tap Yes").exists:
        send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على (Tap Yes)...")
        if d(text="Tap Yes on your phone or tablet").exists:
            d(text="Tap Yes on your phone or tablet").click()
        else:
            d(text="Tap Yes").click()
            
        take_screenshot(d, "4. شاشة التحقق (2FA)")
        send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل لتأكيد الدخول.** (لديك 30 ثانية)...")
        time.sleep(30)
        take_screenshot(d, "5. بعد تأكيد 2FA")
    else:
        send_msg("⚠️ لم تظهر شاشة Tap Yes. قد يكون الدخول تم مباشرة أو هناك خطأ.")

    take_screenshot(d, "6. النتيجة النهائية بعد الدخول")
    send_msg("🎉 انتهت عملية تسجيل الدخول. راجع الصور سيدي.")
    
if __name__ == "__main__":
    main()
