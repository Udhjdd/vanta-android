import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا للتجربة
EMAIL = "ssda73410@gmail.com"
PASSWORD = "fawazfawaz123@"

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

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
        send_msg("🔑 جاري الضغط على تسجيل الدخول...")
        d(text="SIGN IN").click()
        time.sleep(5)
    else:
        send_msg("⚠️ لم يتم العثور على زر SIGN IN.")

    # 3. الانتظار حتى تظهر خانة الإيميل
    send_msg("⏳ في انتظار ظهور خانة الإيميل (قد تستغرق بعض الوقت)...")
    
    # محاولة البحث عن خانة الإيميل (قد يكون اسمها Identifier أو Email)
    email_field = d(className="android.widget.EditText")
    if email_field.exists(timeout=30):
        send_msg("📧 تم العثور على خانة الإيميل. جاري الكتابة...")
        email_field.set_text(EMAIL)
        time.sleep(2)
        
        # الضغط على Next
        if d(text="Next").exists:
            d(text="Next").click()
        else:
            d.press("enter")
            
        time.sleep(10)
        send_msg("🔑 جاري إدخال كلمة المرور...")
        
        # إدخال كلمة المرور
        password_field = d(className="android.widget.EditText")
        if password_field.exists(timeout=10):
            password_field.set_text(PASSWORD)
            time.sleep(2)
            if d(text="Next").exists:
                d(text="Next").click()
            else:
                d.press("enter")
                
            time.sleep(15)
            send_msg("✅ تمت محاولة تسجيل الدخول. جاري التقاط الصورة النهائية.")
        else:
            send_msg("⚠️ لم يتم العثور على خانة كلمة المرور.")
    else:
        send_msg("⚠️ لم تظهر خانة الإيميل. قد يكون الحساب محظوراً أو الشبكة بطيئة.")

    # أخذ صورة للنتيجة
    d.screenshot("/tmp/login_result.png")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/login_result.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    send_msg("🎉 انتهت التجربة. راجع الصورة لمعرفة النتيجة.")
    
if __name__ == "__main__":
    main()
