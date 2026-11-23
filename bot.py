import uiautomator2 as u2
import requests
import time
import sys

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

# ضع الإيميل والباسورد هنا (نفس الحساب الذي وصل لشاشة 2FA)
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
    d.app_start("com.android.vending")
    time.sleep(10)

    # 2. تسجيل الدخول (محاكاة الخطوات السابقة)
    if d(text="SIGN IN").exists:
        d(text="SIGN IN").click()
        time.sleep(5)
    
    if d(className="android.widget.EditText").exists(timeout=30):
        d(className="android.widget.EditText").set_text(EMAIL)
        time.sleep(2)
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
        
        time.sleep(10)
        d(className="android.widget.EditText").set_text(PASSWORD)
        time.sleep(2)
        if d(text="Next").exists: d(text="Next").click()
        else: d.press("enter")
        time.sleep(15)

    # 3. التعامل مع 2FA
    if d(text="Tap Yes on your phone or tablet").exists:
        send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على (Tap Yes)...")
        d(text="Tap Yes on your phone or tablet").click()
        send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل لتأكيد الدخول.** (لديك 30 ثانية)...")
        time.sleep(30)
        
        # التقاط صورة بعد الانتظار
        d.screenshot("/tmp/after_2fa.png")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open("/tmp/after_2fa.png", "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

        # 4. التوجه لصفحة النقاط
        send_msg("💎 جاري التوجه لصفحة Play Points...")
        d.app_start("com.android.vending")
        time.sleep(5)
        # فتح رابط النقاط عبر المتصفح أو المتجر (سنستخدم المتصفح لسهولة التنقل)
        d.app_start("com.android.chrome")
        time.sleep(5)
        # تخطي شاشة الترحيب إذا ظهرت
        if d(text="Accept & continue").exists:
            d(text="Accept & continue").click()
            time.sleep(3)
        if d(text="No thanks").exists:
            d(text="No thanks").click()
            time.sleep(3)
            
        d.open_url("https://play.google.com/store/points?hl=en")
        time.sleep(15)
        
        # محاولة الضغط على Join
        if d(text="Join").exists:
            send_msg("✅ تم العثور على زر Join. جاري الضغط...")
            d(text="Join").click()
            time.sleep(5)
        else:
            send_msg("⚠️ لم يتم العثور على زر Join (قد يكون الحساب مؤهلاً بالفعل أو الـ IP غير مدعوم).")

    else:
        send_msg("⚠️ لم تظهر شاشة Tap Yes. قد يكون الدخول تم مباشرة أو هناك خطأ.")

    # أخذ صورة نهائية
    d.screenshot("/tmp/final_result.png")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("/tmp/final_result.png", "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    send_msg("🎉 انتهت العملية بالكامل سيدي.")
    
if __name__ == "__main__":
    main()
