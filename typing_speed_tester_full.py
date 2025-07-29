import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import time
import random
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import threading
import platform

# For sound effects
if platform.system() == "Windows":
    import winsound
else:
    import pygame
    pygame.mixer.init()

word_list = [
    "python", "programming", "keyboard", "monitor", "mouse", "developer", "logic", "string",
    "function", "variable", "condition", "loop", "error", "typing", "interface", "project",
    "application", "learning", "performance", "input", "output", "window", "frame", "button",
    "data", "file", "system", "speed", "accuracy", "result", "score", "practice", "computer",
    "random", "sentence", "text", "timer", "graph", "theme", "level", "easy", "medium", "hard"
]

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.username = None
        self.start_time = 0
        self.time_left = 60

        self.sound_enabled = True  # Toggle sound on/off if you want

        self.login_screen()

    def login_screen(self):
        self.clear_root()

        tk.Label(self.root, text="Welcome! Please enter your username:", font=("Helvetica", 14)).pack(pady=20)
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.focus()

        tk.Button(self.root, text="Login", font=("Helvetica", 14), command=self.handle_login).pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return
        self.username = username
        self.create_main_ui()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_ui(self):
        self.clear_root()

        self.create_menu()

        tk.Label(self.root, text=f"Hello, {self.username}!", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Difficulty selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()
        tk.Label(difficulty_frame, text="Select Difficulty: ", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.OptionMenu(difficulty_frame, self.difficulty_var, "Easy", "Medium", "Hard").pack(side=tk.LEFT)

        self.sentence_label = tk.Label(self.root, text="", font=("Helvetica", 13), wraplength=720, justify="left")
        self.sentence_label.pack(pady=10)

        self.entry = tk.Text(self.root, height=7, width=90, font=("Courier", 12))
        self.entry.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="blue")
        self.result_label.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start Test", font=("Helvetica", 12), command=self.start_test)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(button_frame, text="Submit", font=("Helvetica", 12), command=self.end_test)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.theme = "light"
        self.apply_theme()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Start Test", command=self.start_test)
        file_menu.add_command(label="View Graph", command=self.show_graph)
        file_menu.add_command(label="Export Report (PDF)", command=self.export_pdf_report)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        view_menu.add_command(label="Toggle Sound Effects", command=self.toggle_sound)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def generate_sentence(self, word_count):
        return " ".join(random.choices(word_list, k=word_count)).capitalize() + "."

    def start_test(self):
        self.entry.delete('1.0', tk.END)
        self.result_label.config(text="")
        level = self.difficulty_var.get()

        if level == "Easy":
            word_count = 20
        elif level == "Hard":
            word_count = 60
        else:
            word_count = 40

        self.text_to_type = self.generate_sentence(word_count)
        self.sentence_label.config(text=self.text_to_type)
        self.time_left = 60
        self.start_time = time.time()
        self.update_timer()

    def play_beep(self):
        if not self.sound_enabled:
            return
        try:
            if platform.system() == "Windows":
                winsound.Beep(1000, 150)
            else:
                # Using pygame beep
                freq = 1000
                duration_ms = 150
                sample_rate = 44100
                n_samples = int(round(duration_ms * sample_rate / 1000))
                buf = pygame.sndarray.make_sound(
                    (4096 * pygame.sndarray.array([[int(4096 * (0.5 * (i / n_samples))) for i in range(n_samples)]]).T).astype('int16'))
                buf.play()
        except Exception as e:
            print("Beep error:", e)

    def update_timer(self):
        if self.time_left > 0:
            self.root.title(f"Typing Speed Tester - Time Left: {self.time_left}s")
            if self.time_left <= 5:  # beep in last 5 seconds
                threading.Thread(target=self.play_beep).start()
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.end_test()

    def end_test(self):
        end_time = time.time()
        typed_text = self.entry.get("1.0", tk.END).strip()
        time_taken = round(end_time - self.start_time, 2)

        word_count = len(typed_text.split())
        speed = round((word_count / time_taken) * 60, 2) if time_taken > 0 else 0
        accuracy = self.calculate_accuracy(typed_text, self.text_to_type)
        score = self.calculate_score(speed)

        self.save_score(speed, accuracy, score)

        result = (
            f"Time Taken: {time_taken} sec\n"
            f"Speed: {speed} WPM\n"
            f"Accuracy: {accuracy}%\n"
            f"Score: {score}/100"
        )
        self.result_label.config(text=result)
        self.root.title("Typing Speed Tester")

    def calculate_accuracy(self, typed, reference):
        typed_words = typed.split()
        reference_words = reference.split()
        correct = sum(1 for tw, rw in zip(typed_words, reference_words) if tw == rw)
        total = len(reference_words)
        return round((correct / total) * 100, 2) if total > 0 else 0

    def calculate_score(self, speed):
        if speed >= 60:
            return 100
        elif speed >= 40:
            return 80
        elif speed >= 20:
            return 60
        else:
            return 40

    def save_score(self, speed, accuracy, score):
        filename = f"{self.username}_scores.csv"
        try:
            with open(filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), speed, accuracy, score])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save score: {e}")

    def show_graph(self):
        filename = f"{self.username}_scores.csv"
        try:
            df = pd.read_csv(filename, header=None)
            speeds = df[1].tail(10)
            times = df[0].tail(10)

            plt.figure(figsize=(8, 4))
            plt.plot(times, speeds, marker='o', linestyle='-', color='darkgreen')
            plt.title(f"{self.username}'s Typing Speed Over Time (WPM)")
            plt.xlabel("Time")
            plt.ylabel("Speed (WPM)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read score data.\n{e}")

    def export_pdf_report(self):
        filename = f"{self.username}_scores.csv"
        pdf_filename = f"{self.username}_typing_report.pdf"
        try:
            df = pd.read_csv(filename, header=None)
        except Exception as e:
            messagebox.showerror("Error", f"No data to export or failed to read data.\n{e}")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(0, 10, f"Typing Speed Report for {self.username}", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)

        # Add table header
        pdf.cell(60, 10, "Date & Time", 1)
        pdf.cell(40, 10, "Speed (WPM)", 1)
        pdf.cell(40, 10, "Accuracy (%)", 1)
        pdf.cell(40, 10, "Score", 1)
        pdf.ln()

        # Add data rows
        for index, row in df.iterrows():
            pdf.cell(60, 10, str(row[0]), 1)
            pdf.cell(40, 10, str(row[1]), 1)
            pdf.cell(40, 10, str(row[2]), 1)
            pdf.cell(40, 10, str(row[3]), 1)
            pdf.ln()

        try:
            pdf.output(pdf_filename)
            messagebox.showinfo("Success", f"PDF report saved as {pdf_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF.\n{e}")

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "dark":
            self.root.config(bg="black")
            self.sentence_label.config(bg="black", fg="white")
            self.entry.config(bg="gray10", fg="white", insertbackground="white")
            self.result_label.config(bg="black", fg="lightgreen")
        else:
            self.root.config(bg="SystemButtonFace")
            self.sentence_label.config(bg="SystemButtonFace", fg="black")
            self.entry.config(bg="white", fg="black", insertbackground="black")
            self.result_label.config(bg="SystemButtonFace", fg="blue")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        status = "enabled" if self.sound_enabled else "disabled"
        messagebox.showinfo("Sound Effects", f"Sound effects {status}.")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.username = None
            self.login_screen()

    def show_about(self):
        messagebox.showinfo("About",
                            "Typing Speed Tester\n"
                            "Created with Python Tkinter\n"
                            "Features:\n"
                            "- User login\n"
                            "- Difficulty levels\n"
                            "- Saves history per user\n"
                            "- Export history as PDF\n"
                            "- Sound effects and countdown beeps\n"
                            "- Speed graph\n"
                            "- Light/Dark theme toggle")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTester(root)
    root.mainloop()
