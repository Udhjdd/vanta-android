import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

EMAIL = "ssda73410@gmail.com"
PASSWORD = "fawazfawaz123@" # ضع كلمة المرور هنا

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def take_screenshot(d, caption):
    path = f"/tmp/{caption.replace(' ', '_')}.png"
    try:
        d.screenshot(path)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": f})
    except Exception:
        pass

def safe_click(d, text, timeout=15):
    for _ in range(3):
        try:
            if d(text=text).exists(timeout=timeout):
                d(text=text).click()
                time.sleep(2)
                return True
            else:
                return False
        except Exception:
            time.sleep(2)
    return False

def safe_set_text(d, text, timeout=15):
    for _ in range(3):
        try:
            field = d(className="android.widget.EditText")
            if field.exists(timeout=timeout):
                field.click()
                time.sleep(1)
                field.clear_text()
                field.set_text(text)
                time.sleep(1)
                return True
        except Exception:
            time.sleep(2)
    return False

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
    if safe_click(d, "SIGN IN"):
        send_msg("⏳ جاري الانتظار حتى تظهر خانة الإيميل...")
    else:
        send_msg("⚠️ لم يتم العثور على زر SIGN IN.")
        return

    # 3. إدخال الإيميل
    if safe_set_text(d, EMAIL, timeout=30):
        send_msg("📧 تم إدخال الإيميل. جاري الضغط على Next...")
        take_screenshot(d, "2. بعد إدخال الإيميل")
        if not safe_click(d, "Next"):
            try: d.press("enter")
            except: pass
        time.sleep(10)
    else:
        send_msg("⚠️ فشل إدخال الإيميل.")
        return

    # 4. إدخال كلمة المرور
    if safe_set_text(d, PASSWORD, timeout=30):
        send_msg("🔑 تم إدخال الباسورد. جاري الضغط على Next...")
        take_screenshot(d, "3. بعد إدخال الباسورد")
        if not safe_click(d, "Next"):
            try: d.press("enter")
            except: pass
        time.sleep(15)
    else:
        send_msg("⚠️ فشل إدخال كلمة المرور.")
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
        send_msg("⚠️ لم تظهر شاشة Tap Yes.")

    # 6. الضغط على "I agree"
    send_msg("📜 جاري البحث عن زر (I agree)...")
    if safe_click(d, "I agree"):
        send_msg("✅ تم الضغط على I agree. جاري الانتظار...")
        time.sleep(5)
        take_screenshot(d, "6. بعد I agree")
        
        # 7. الضغط على "ACCEPT" لشاشة خدمات جوجل
        send_msg("📜 جاري البحث عن زر (ACCEPT)...")
        if safe_click(d, "ACCEPT"):
            send_msg("✅ تم الضغط على ACCEPT. جاري إنهاء الإعداد...")
            
            # التقاط 3 صور متتالية للتحقق من العودة للمتجر
            time.sleep(3)
            take_screenshot(d, "7. بعد ACCEPT - صورة 1")
            time.sleep(2)
            take_screenshot(d, "8. بعد ACCEPT - صورة 2")
            time.sleep(2)
            take_screenshot(d, "9. بعد ACCEPT - صورة 3 (النهائية)")
        else:
            send_msg("⚠️ لم يتم العثور على زر ACCEPT.")
            take_screenshot(d, "النتيجة النهائية")
    else:
        send_msg("⚠️ لم يتم العثور على زر I agree.")

    send_msg("🎉 انتهت عملية تسجيل الدخول بالكامل سيدي.")
    
if __name__ == "__main__":
    main()
