import requests
import threading
import time

# цель захардкожена на localhost — это учебный стенд, свой же сайт
URL = "http://127.0.0.1:5000/register"
DATA = {"username": "test", "password": "123"}

THREADS = 1000         # сколько параллельных "атакующих"
running = True
sent = 0
failed = 0
lock = threading.Lock()


def worker():
    global sent, failed
    while running:
        try:
            requests.post(URL, data=DATA, timeout=2)
            with lock:
                sent += 1
        except Exception:
            with lock:
                failed += 1


# запускаем кучу потоков
for _ in range(THREADS):
    threading.Thread(target=worker, daemon=True).start()

print(f"Долбим {URL} в {THREADS} потоков. Ctrl+C чтобы остановить.")

try:
    while True:
        time.sleep(1)
        print(f"Отправлено: {sent} | Ошибок (сайт не ответил): {failed}")
except KeyboardInterrupt:
    running = False
    print(f"\nСтоп. Всего отправлено: {sent}, ошибок: {failed}")