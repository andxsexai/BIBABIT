import os
# Глушим предупреждение macOS (должно быть ДО импорта customtkinter)
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import customtkinter as ctk
import subprocess
import threading
import sys

# Настройка стабильной темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GangApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GANGPYTHON CONTROL PANEL v1.0")
        self.geometry("600x520")
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Интерфейс
        self.label = ctk.CTkLabel(self, text="GANGPYTHON INTERFACE", font=("Arial", 24, "bold"), text_color="#A855F7")
        self.label.pack(pady=20)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Вставь ссылку Splice...", width=400)
        self.url_entry.pack(pady=10)

        self.grab_btn = ctk.CTkButton(self, text="ЗАХВАТИТЬ СЭМПЛ", command=self.start_grab, fg_color="#9333EA")
        self.grab_btn.pack(pady=10)

        self.log_box = ctk.CTkTextbox(self, width=500, height=200)
        self.log_box.pack(pady=20)
        self.log(">>> СИСТЕМА ГОТОВА")

    def log(self, message):
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")

    def start_grab(self):
        url = self.url_entry.get()
        if not url: return self.log("!!! ВВЕДИТЕ URL")
        self.log(f"[*] ЗАПУСК...")
        # Запуск в отдельном потоке, чтобы GUI не завис
        threading.Thread(target=self.run_grab, args=(url,), daemon=True).start()

    def run_grab(self, url):
        try:
            # Запускаем твой рабочий скрипт
            process = subprocess.Popen(["python3", "grabber_v1.py", url], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout: self.log(stdout)
            if stderr: self.log(f"ОШИБКА: {stderr}")
        except Exception as e:
            self.log(f"СБОЙ: {str(e)}")

if __name__ == "__main__":
    app = GangApp()
    app.mainloop()