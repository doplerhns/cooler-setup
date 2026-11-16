import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
import sys

# ---------- Главное окно установщика ----------
root = tk.Tk()
root.title("Cooler Setup 2.1.4")
root.geometry("520x380")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Иконка-заглушка (стандартная)
try:
    root.iconbitmap(default="fan.ico")
except:
    pass

# ---------- Заголовок ----------
header = tk.Frame(root, bg="#0078d7", height=70)
header.pack(fill="x")
tk.Label(header, text="Cooler Setup", font=("Segoe UI", 18, "bold"),
         fg="white", bg="#0078d7").pack(side="left", padx=20, pady=15)
tk.Label(header, text="Версия 2.1.4", font=("Segoe UI", 10),
         fg="white", bg="#0078d7").pack(side="right", padx=20)

# ---------- Основной контент ----------
content = tk.Frame(root, bg="#f0f0f0")
content.pack(fill="both", expand=True, padx=20, pady=15)

status_var = tk.StringVar(value="Добро пожаловать в мастер установки Cooler.")
status_label = tk.Label(content, textvariable=status_var, font=("Segoe UI", 10),
                        bg="#f0f0f0", anchor="w", justify="left")
status_label.pack(fill="x", pady=(0, 10))

progress = ttk.Progressbar(content, mode="determinate", maximum=100)
progress.pack(fill="x", pady=10)

log_box = tk.Text(content, height=8, font=("Consolas", 9), state="disabled",
                  bg="white", relief="solid", bd=1)
log_box.pack(fill="both", expand=True)

def log(msg):
    log_box.config(state="normal")
    log_box.insert("end", msg + "\n")
    log_box.see("end")
    log_box.config(state="disabled")
    root.update()

# ---------- Кнопки ----------
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(fill="x", padx=20, pady=10)

install_btn = tk.Button(btn_frame, text="Установить", width=14,
                        font=("Segoe UI", 10), bg="#0078d7", fg="white",
                        activebackground="#005a9e")
install_btn.pack(side="right", padx=5)

cancel_btn = tk.Button(btn_frame, text="Отмена", width=10, font=("Segoe UI", 10))
cancel_btn.pack(side="right", padx=5)

# ---------- Логика установки ----------
STAGES = [
    (5,   "Проверка системных требований..."),
    (12,  "Поиск установленных версий Cooler..."),
    (20,  "Распаковка CoolerCore.dll..."),
    (28,  "Регистрация драйвера PWM-контроллера..."),
    (36,  "Копирование CoolerTray.exe..."),
    (45,  "Настройка автозапуска..."),
    (55,  "Калибровка датчиков температуры..."),
    (65,  "Синхронизация с CoolerMaster XY-9000..."),
    (75,  "Оптимизация кривых вентиляторов..."),
    (85,  "Применение профиля 'Silent Max'..."),
    (93,  "Финальная проверка..."),
    (99,  "Почти готово..."),
]

def fake_install():
    install_btn.config(state="disabled")
    cancel_btn.config(state="disabled")

    for pct, msg in STAGES:
        # плавно доезжаем до нужного процента
        current = progress["value"]
        while current < pct:
            current += 1
            progress["value"] = current
            status_var.set(msg)
            time.sleep(0.03)
            root.update()
        log(f"[OK] {msg}")

    # ---------- ТРОЛЛИНГ ----------
    time.sleep(0.5)
    status_var.set("Установка завершена успешно!")
    log("[OK] Установка завершена.")
    time.sleep(1)

    # "Ой, что-то пошло не так"
    status_var.set("ОШИБКА: перегрев кулера!")
    log("[!!] ВНИМАНИЕ: Кулер не отвечает!")
    log("[!!] Температура ЦП: 118°C")
    log("[!!] Обороты: 0 RPM")
    time.sleep(1.2)

    messagebox.showerror("Cooler — Критическая ошибка",
        "Не удалось запустить кулер!\n\n"
        "Температура процессора: 118°C\n"
        "Вентилятор: не отвечает\n\n"
        "Рекомендуется немедленно выключить ПК!")

    # Анимация "перегрева"
    for i in range(30):
        root.configure(bg="#ff0000" if i % 2 == 0 else "#ff8800")
        header.configure(bg="#ff0000" if i % 2 == 0 else "#ff8800")
        log(f"🔥 ПЕРЕГРЕВ! Температура: {118 + i}°C")
        root.update()
        time.sleep(0.08)

    # ---------- ПАНЧЛАЙН ----------
    root.configure(bg="#f0f0f0")
    header.configure(bg="#0078d7")
    status_var.set("...")

    messagebox.showinfo("Cooler",
        "Шутка 😄\n\n"
        "Твой ПК в полном порядке.\n"
        "Ничего не установлено, ничего не сломано.\n\n"
        "Просто расслабься и проверь, не пыльный ли у тебя кулер :)")

    progress["value"] = 0
    status_var.set("Шутка завершена. Программу можно закрыть.")
    install_btn.config(state="normal", text="Ещё раз 😄")
    cancel_btn.config(state="normal")

def start_install():
    threading.Thread(target=fake_install, daemon=True).start()

install_btn.config(command=start_install)
cancel_btn.config(command=root.destroy)

root.mainloop()
