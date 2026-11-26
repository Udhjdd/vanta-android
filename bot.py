import uiautomator2 as u2
import requests
import time
import sys
import urllib.parse
import http.server
import socketserver
import threading
import os
import json

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

CLIENT_ID = "469058699729-6bh3d12qsj1775uni0tj7gtu7uld61iv.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/games"

auth_code = None
EMAIL = None
PASSWORD = None

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def take_screenshot(d, caption):
    path = f"/tmp/{int(time.time())}_{caption.replace(' ', '_')}.png"
    try:
        d.screenshot(path)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID, "caption": f"📸 {caption}"}, files={"photo": f})
    except Exception:
        pass

def get_credentials_from_telegram():
    """جلب الإيميل والباسورد من تيليجرام قبل بدء العملية"""
    global EMAIL, PASSWORD
    send_msg("🤖 مرحباً سيدي. يرجى إرسال الإيميل في سطر، وكلمة المرور في السطر الذي يليه.")
    
    offset = None
    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"timeout": 30, "offset": offset}
        try:
            res = requests.get(url, params=params, timeout=35).json()
            if "result" in res and len(res["result"]) > 0:
                for update in res["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        chat_id = str(update["message"]["chat"]["id"])
                        if chat_id == CHAT_ID:
                            text = update["message"]["text"].strip()
                            lines = text.split('\n')
                            if len(lines) >= 2:
                                EMAIL = lines[0].strip()
                                PASSWORD = lines[1].strip()
                                send_msg(f"✅ تم استلام البيانات للحساب: {EMAIL}\nجاري البدء...")
                                return True
                            else:
                                send_msg("⚠️ يرجى إرسال الإيميل في سطر، والباسورد في السطر التالي.")
        except Exception as e:
            print(f"Polling error: {e}")
        time.sleep(2)

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Success!</h1><p>Token captured. You can close this.</p>")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Waiting...</h1>")

def start_server():
    with socketserver.TCPServer(("", 8080), OAuthHandler) as httpd:
        httpd.serve_forever()

def safe_input(d, text_to_type, chat_id, step_name):
    """دالة آمنة للكتابة تتجنب انهيار الشاشة وتلتقط الصور"""
    for attempt in range(3):
        try:
            field = d(className="android.widget.EditText")
            if field.wait(timeout=10):
                field.click()
                time.sleep(1)
                field.set_text(text_to_type)
                time.sleep(1)
                take_screenshot(d, step_name)
                return True
        except Exception as e:
            print(f"Retry {attempt+1}: {e}")
            time.sleep(2)
    return False

def login_to_google(d):
    time.sleep(3)
    take_screenshot(d, "التحقق من شاشة الدخول")
    
    if d(text="Sign in").exists or d(className="android.widget.EditText").exists:
        send_msg("🔑 جاري إدخال الإيميل...")
        if safe_input(d, EMAIL, CHAT_ID, "بعد إدخال الإيميل"):
            if d(text="Next").exists: d(text="Next").click()
            else: d.press("enter")
            time.sleep(5)
            take_screenshot(d, "بعد الضغط على Next (الإيميل)")
        else:
            send_msg("⚠️ فشل إدخال الإيميل.")
            return

        send_msg("🔑 جاري إدخال كلمة المرور...")
        if safe_input(d, PASSWORD, CHAT_ID, "بعد إدخال الباسورد"):
            if d(text="Next").exists: d(text="Next").click()
            else: d.press("enter")
            time.sleep(8)
            take_screenshot(d, "بعد الضغط على Next (الباسورد)")
        else:
            send_msg("⚠️ فشل إدخال كلمة المرور.")
            return

        # التعامل مع 2FA
        take_screenshot(d, "التحقق من 2FA")
        if d(text="Tap Yes").exists or d(text="Tap Yes on your phone or tablet").exists:
            send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على Tap Yes...")
            if d(text="Tap Yes").exists: d(text="Tap Yes").click()
            else: d(text="Tap Yes on your phone or tablet").click()
            take_screenshot(d, "تم الضغط على Tap Yes")
            send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل.** (لديك 45 ثانية)...")
            time.sleep(45)
            take_screenshot(d, "بعد انتظار 2FA")

def main():
    global auth_code
    # 1. جلب البيانات من تيليجرام
    get_credentials_from_telegram()
    
    send_msg("🚀 بدء تشغيل الهاتف الوهمي...")
    
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    os.system("adb reverse tcp:8080 tcp:8080")
    send_msg("🔗 تم ربط السيرفر المحلي بالهاتف الوهمي.")

    try:
        d = u2.connect("127.0.0.1:5555")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    d.app_start("com.android.chrome")
    time.sleep(5)
    if d(text="Accept & continue").exists:
        d(text="Accept & continue").click()
        time.sleep(3)
    if d(text="No thanks").exists:
        d(text="No thanks").click()
        time.sleep(3)
    take_screenshot(d, "تم فتح المتصفح")

    send_msg("🌐 جاري فتح رابط الصلاحيات...")
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
    take_screenshot(d, "صفحة الصلاحيات")

    login_to_google(d)

    # اختيار الحساب
    take_screenshot(d, "التحقق من شاشة اختيار الحساب")
    if d(textContains="@gmail.com").exists:
        send_msg("👤 جاري اختيار الحساب...")
        d(textContains="@gmail.com").click()
        time.sleep(5)
        take_screenshot(d, "بعد اختيار الحساب")

    # الموافقة
    take_screenshot(d, "التحقق من شاشة الموافقة")
    if d(text="Continue").exists:
        send_msg("✅ جاري الضغط على Continue...")
        d(text="Continue").click()
        time.sleep(5)
        take_screenshot(d, "بعد الضغط على Continue")
    elif d(text="Allow").exists:
        send_msg("✅ جاري الضغط على Allow...")
        d(text="Allow").click()
        time.sleep(5)
        take_screenshot(d, "بعد الضغط على Allow")
    
    take_screenshot(d, "النتيجة النهائية (قبل التقاط الكود)")

    send_msg("⏳ في انتظار التقاط الكود تلقائياً...")
    for _ in range(15):
        if auth_code:
            break
        time.sleep(1)

    if auth_code:
        send_msg(f"🎉 تم التقاط الكود!\nجاري تحويله...")
        
        token_url = "https://oauth2.googleapis.com/token"
        res = requests.post(token_url, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
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
        send_msg("❌ فشل التقاط الكود (انتهت المهلة).")
        take_screenshot(d, "error_no_code")

if __name__ == "__main__":
    main()
