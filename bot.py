import uiautomator2 as u2
import requests
import time
import sys
import urllib.parse
import http.server
import socketserver
import threading
import os

BOT_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652"

CLIENT_ID = "469058699729-6bh3d12qsj1775uni0tj7gtu7uld61iv.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/games"

EMAIL = "nvhjgvjj49@gmail.com"
PASSWORD = "fawazfawaz1234@#" # ضع كلمة المرور هنا

auth_code = None

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

def login_to_google(d):
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

        if d(text="Tap Yes").exists or d(text="Tap Yes on your phone or tablet").exists:
            send_msg("📲 وصلت لشاشة التحقق. جاري الضغط على Tap Yes...")
            if d(text="Tap Yes").exists: d(text="Tap Yes").click()
            else: d(text="Tap Yes on your phone or tablet").click()
            send_msg("⚠️ **افتح هاتفك الآن واضغط على إشعار جوجل.** (لديك 45 ثانية)...")
            time.sleep(45)

def main():
    global auth_code
    send_msg("🚀 بدء تشغيل الهاتف الوهمي لاستخراج التوكن...")
    
    # 1. تشغيل السيرفر المحلي على المنفذ 8080
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # 2. ربط منفذ الهاتف بمنفذ السيرفر
    os.system("adb reverse tcp:8080 tcp:8080")
    send_msg("🔗 تم ربط السيرفر المحلي بالهاتف الوهمي.")

    try:
        d = u2.connect("127.0.0.1:5555")
    except Exception as e:
        send_msg(f"❌ فشل الاتصال بالهاتف: {str(e)}")
        sys.exit(1)

    # 3. فتح المتصفح
    d.app_start("com.android.chrome")
    time.sleep(5)
    if d(text="Accept & continue").exists:
        d(text="Accept & continue").click()
        time.sleep(3)
    if d(text="No thanks").exists:
        d(text="No thanks").click()
        time.sleep(3)

    # 4. فتح رابط الصلاحيات
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

    # 5. تسجيل الدخول (إذا لزم)
    login_to_google(d)

    # 6. اختيار الحساب
    if d(textContains="@gmail.com").exists:
        send_msg("👤 جاري اختيار الحساب...")
        d(textContains="@gmail.com").click()
        time.sleep(5)

    # 7. الموافقة على الصلاحيات
    if d(text="Continue").exists:
        send_msg("✅ جاري الضغط على Continue...")
        d(text="Continue").click()
        time.sleep(5)
    elif d(text="Allow").exists:
        send_msg("✅ جاري الضغط على Allow...")
        d(text="Allow").click()
        time.sleep(5)
    
    take_screenshot(d, "بعد الموافقة")

    # 8. انتظار التقاط الكود بواسطة السيرفر
    send_msg("⏳ في انتظار التقاط الكود تلقائياً من السيرفر...")
    for _ in range(15): # انتظار 15 ثانية
        if auth_code:
            break
        time.sleep(1)

    # 9. تحويل الكود إلى Refresh Token
    if auth_code:
        send_msg(f"🎉 تم التقاط الكود بنجاح!\nجاري تحويله...")
        
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
