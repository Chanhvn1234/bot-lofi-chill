from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Đài phát thanh Thế Giới Ngầm Reborn đang hoạt động 24/7!"

def run():
    # Khởi chạy web server ở port 8080
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Chạy web server trên một luồng riêng biệt để không chặn code của bot
    t = Thread(target=run)
    t.start()