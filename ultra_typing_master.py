import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

EASY = [
    "Typing is a valuable skill for everyone.",
    "Practice daily to improve your typing speed.",
    "Python makes programming fun and simple."
]

MEDIUM = [
    "Artificial intelligence is transforming the world rapidly.",
    "Consistency and hard work are essential for success.",
    "Technology keeps evolving with new innovations every year."
]

HARD = [
    "Machine learning models analyze vast datasets to build predictions.",
    "Cybersecurity is critical to prevent unauthorized digital access.",
    "Programming requires logical thinking and structured problem solving."
]


class UltraTypingMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultra-Pro Typing Master")
        self.root.geometry("950x600")
        self.root.config(bg="#101010")

        self.time_left = 60
        self.start_time = None
        self.test_running = False
        self.target_text = ""
        self.current_word_index = 0
        self.words_list = []

        # Heading
        title = tk.Label(root, text="Ultra-Pro Typing Master",
                         font=("Arial", 28, "bold"), fg="cyan", bg="#101010")
        title.pack(pady=10)

        # Difficulty selection
        mode_frame = tk.Frame(root, bg="#101010")
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Difficulty:", fg="white", bg="#101010",
                 font=("Arial", 14)).pack(side="left", padx=10)

        self.mode_box = ttk.Combobox(mode_frame, values=["Easy", "Medium", "Hard"], width=15)
        self.mode_box.current(1)
        self.mode_box.pack(side="left")

        # Time selection
        tk.Label(mode_frame, text="Time:", fg="white", bg="#101010",
                 font=("Arial", 14)).pack(side="left", padx=10)

        self.time_box = ttk.Combobox(mode_frame, values=["30", "60", "120"], width=10)
        self.time_box.current(1)
        self.time_box.pack(side="left")

        # Paragraph text display
        self.display_text = tk.Text(root, height=7, width=100, bg="#1e1e1e",
                                    fg="white", font=("Arial", 14), wrap="word")
        self.display_text.pack(pady=20)
        self.display_text.config(state="disabled")

        # Typing box
        self.typing_box = tk.Entry(root, font=("Arial", 16), width=80)
        self.typing_box.pack(pady=10)
        self.typing_box.bind("<KeyRelease>", self.check_typing)

        # Timer Label
        self.timer_label = tk.Label(root, text="Time Left: 60",
                                    font=("Arial", 16), fg="yellow", bg="#101010")
        self.timer_label.pack()

        # Stats
        self.stats_label = tk.Label(root, text="WPM: 0 | Accuracy: 0%",
                                    font=("Arial", 18), fg="lime", bg="#101010")
        self.stats_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#101010")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start Test", width=12, height=1, bg="green",
                  fg="white", font=("Arial", 14), command=self.start_test).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Restart", width=12, height=1, bg="orange",
                  fg="white", font=("Arial", 14), command=self.restart_test).pack(side="left", padx=10)

        # Highlight tags
        self.display_text.tag_config("correct", foreground="lime")
        self.display_text.tag_config("wrong", foreground="red")
        self.display_text.tag_config("active", background="#444")

    # Start Test
    def start_test(self):
        mode = self.mode_box.get()

        if mode == "Easy":
            self.target_text = random.choice(EASY)
        elif mode == "Medium":
            self.target_text = random.choice(MEDIUM)
        else:
            self.target_text = random.choice(HARD)

        self.words_list = self.target_text.split()
        self.current_word_index = 0
        self.time_left = int(self.time_box.get())
        self.timer_label.config(text=f"Time Left: {self.time_left}")
        self.stats_label.config(text="WPM: 0 | Accuracy: 0%")
        self.typing_box.delete(0, tk.END)

        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert(tk.END, self.target_text)
        self.display_text.config(state="disabled")

        self.start_time = time.time()
        self.test_running = True
        self.countdown()
        self.highlight_active_word()

    # Countdown
    def countdown(self):
        if self.test_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}")
            self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.test_running = False
            messagebox.showinfo("Time Up!", "Your typing test has ended.")
            self.typing_box.delete(0, tk.END)

    # Real-time typing check
    def check_typing(self, event):
        if not self.test_running:
            return

        typed = self.typing_box.get().strip()
        target_word = self.words_list[self.current_word_index]

        # Real-time color marking
        if target_word.startswith(typed):
            self.highlight_word("correct")
        else:
            self.highlight_word("wrong")

        # On space — move to next word
        if event.keysym == "space":
            if typed == target_word:
                self.current_word_index += 1
            self.typing_box.delete(0, tk.END)
            self.highlight_active_word()
            self.update_stats()

    # Highlight the active word
    def highlight_active_word(self):
        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)

        for i, word in enumerate(self.words_list):
            if i == self.current_word_index:
                self.display_text.insert(tk.END, word + " ", "active")
            else:
                self.display_text.insert(tk.END, word + " ")

        self.display_text.config(state="disabled")

    # Highlight correctness
    def highlight_word(self, tag):
        self.display_text.config(state="normal")
        self.highlight_active_word()

        # Get current word range
        start = "1.0"
        for i in range(self.current_word_index):
            start = self.display_text.search(self.words_list[i], start, stopindex=tk.END) + f"+{len(self.words_list[i])}c"

        end = start + f"+{len(self.words_list[self.current_word_index])}c"
        self.display_text.tag_add(tag, start, end)
        self.display_text.config(state="disabled")

    # Stats update
    def update_stats(self):
        elapsed = time.time() - self.start_time
        wpm = (self.current_word_index / elapsed) * 60

        total_chars = len(" ".join(self.words_list[:self.current_word_index]))
        accuracy = (total_chars / len(self.target_text)) * 100

        self.stats_label.config(text=f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

    # Restart test
    def restart_test(self):
        self.test_running = False
        self.target_text = ""
        self.typing_box.delete(0, tk.END)
        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.config(state="disabled")
        self.stats_label.config(text="WPM: 0 | Accuracy: 0%")


root = tk.Tk()
UltraTypingMaster(root)
root.mainloop()
