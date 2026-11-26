import uiautomator2 as u2
import requests
import time
import sys
import urllib.parse

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

CLIENT_ID = "469058699729-6bh3d12qsj1775uni0tj7gtu7uld61iv.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/games"

EMAIL = "nvhjgvjj49@gmail.com"
PASSWORD = "fawazfawaz1234@#" # ضع كلمة المرور هنا

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

def login_to_google(d):
    """دالة مساعدة لتسجيل الدخول (تستخدم في الصفحة الأولى أو صفحة الصلاحيات)"""
    time.sleep(3)
    if d(text="Sign in").exists or d(className="android.widget.EditText").exists:
        send_msg("🔑 جاري تسجيل الدخول...")
        email_field = d(className="android.widget.EditText")
        if email_field.exists:
            email_field.click()
            time.sleep(1)
            email_field.set_text(EMAIL)
            time.sleep(1)
            if d(text="Next").exists: d(text="Next").click()
            else: d.press("enter")
            time.sleep(5)

        password_field = d(className="android.widget.EditText")
        if password_field.exists:
            password_field.click()
            time.sleep(1)
            password_field.set_text(PASSWORD)
            time.sleep(1)
            if d(text="Next").exists: d(text="Next").click()
            else: d.press("enter")
            time.sleep(8)

        # التحقق بخطوتين (إذا ظهرت)
        if d(text="Tap Yes").exists or d(text="Tap Yes on your phone or tablet").exists:
            send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على Tap Yes...")
            if d(text="Tap Yes").exists: d(text="Tap Yes").click()
            else: d(text="Tap Yes on your phone or tablet").click()
            send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل.** (لديك 45 ثانية)...")
            time.sleep(45)

def main():
    send_msg("🚀 بدء تشغيل الهاتف الوهمي لاستخراج التوكن...")
    
    try:
        d = u2.connect("127.0.0.1:5555")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # 1. فتح المتصفح
    d.app_start("com.android.chrome")
    time.sleep(5)
    if d(text="Accept & continue").exists:
        d(text="Accept & continue").click()
        time.sleep(3)
    if d(text="No thanks").exists:
        d(text="No thanks").click()
        time.sleep(3)

    # 2. فتح رابط الصلاحيات مباشرة
    send_msg("🔗 جاري فتح رابط الصلاحيات...")
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    })
    
    d.open_url(auth_url)
    time.sleep(8)
    take_screenshot(d, "1. صفحة الصلاحيات")

    # 3. تسجيل الدخول إذا طلب (لأن الجلسة لم تنتقل)
    login_to_google(d)
    take_screenshot(d, "2. بعد تسجيل الدخول")

    # 4. اختيار الحساب إذا ظهر
    if d(textContains="@gmail.com").exists:
        send_msg("👤 جاري اختيار الحساب...")
        d(textContains="@gmail.com").click()
        time.sleep(5)

    # 5. الضغط على Continue أو Allow
    if d(text="Continue").exists:
        send_msg("✅ جاري الضغط على Continue...")
        d(text="Continue").click()
        time.sleep(5)
    elif d(text="Allow").exists:
        send_msg("✅ جاري الضغط على Allow...")
        d(text="Allow").click()
        time.sleep(5)
    
    take_screenshot(d, "3. بعد الموافقة")

    # 6. استخراج الكود من شريط العنوان
    send_msg("🔍 جاري استخراج الكود...")
    current_url = ""
    
    # محاولة قراءة الرابط
    for _ in range(15):
        try:
            # فتح شريط العنوان
            d(className="android.widget.EditText", packageName="com.android.chrome").click()
            time.sleep(1)
            current_url = d(className="android.widget.EditText", packageName="com.android.chrome").get_text()
            if "code=" in current_url:
                break
            # إغلاق الكيبورد
            d.press("back")
            time.sleep(1)
        except:
            pass
        time.sleep(2)

    if "code=" in current_url:
        code = current_url.split("code=")[1].split("&")[0]
        send_msg(f"🎉 تم التقاط الكود!\nجاري تحويله إلى Refresh Token...")
        
        token_url = "https://oauth2.googleapis.com/token"
        res = requests.post(token_url, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        })
        token_data = res.json()
        
        if 'refresh_token' in token_data:
            rt = token_data['refresh_token']
            send_msg(f"✅ **نجاح ساحق!**\nهذا هو الـ Refresh Token:\n`{rt}`\n\nانسخه.")
        else:
            send_msg(f"⚠️ لم أجد refresh_token. الرد: {token_data}")
    else:
        send_msg(f"❌ فشل التقاط الكود. الرابط الحالي: {current_url}")
        take_screenshot(d, "error_no_code")

if __name__ == "__main__":
    main()
