import tkinter as tk
from tkinter import messagebox
from core import GameCore, Timer

class TypingGame:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Typing and Scramble Game")
        self.win.geometry("600x400")
        self.win.configure(bg="pink")
        self.game = GameCore()
        self.timer = Timer()
        self.sentence = ""
        self.scramble = {}
        self.make_menu()

    def clear(self):
        for w in self.win.winfo_children():
            w.destroy()

    def styled_button(self, **kwargs):
        return tk.Button(
            self.win,
            bg="#FFFFCC",
            fg="black",
            relief="raised",
            bd=3,
            **kwargs
        )

    def styled_label(self, **kwargs):
        return tk.Label(
            self.win,
            bg="#FFFFCC",
            **kwargs
        )

    def make_menu(self):
        self.clear()
        self.styled_label(text="Typing and Scramble Game", font=("Arial", 20)).pack(pady=30)
        self.styled_button(text="Typing Test", width=25, command=self.typing_test).pack(pady=10)
        self.styled_button(text="Word Scramble", width=25, command=self.scramble_game).pack(pady=10)
        self.styled_button(text="Exit", width=25, command=self.win.quit).pack(pady=10)
        self.styled_label(
            text="Made by MAHDI, TAMJEED, SAKIB",
            font=("Arial", 12, "italic"),
            fg="gray"
        ).pack(side="bottom", pady=10)

    def typing_test(self):
        self.clear()
        self.sentence = self.game.get_random_typing_sentence()
        self.styled_label(text="Typing Test", font=("Arial", 16)).pack(pady=10)
        self.styled_label(text="Type this sentence:").pack()
        self.styled_label(text=self.sentence, wraplength=500, fg="blue").pack(pady=10)

        input_box = tk.Text(self.win, height=3, width=60)
        input_box.pack(pady=10)
        input_box.focus()
        input_box.bind('<KeyPress>', lambda e: self.timer.start() if not self.timer.is_running else None)

        def submit():
            time_taken = self.timer.stop()
            user = input_box.get('1.0', 'end-1c')
            if not user.strip():
                messagebox.showinfo("Type!", "You must type something.")
                return
            wpm = self.game.calculate_wpm(self.sentence, time_taken)
            acc = self.game.calculate_accuracy(self.sentence, user)
            msg = f"Time: {time_taken:.2f}s\nWPM: {wpm}\nAccuracy: {acc}%"
            messagebox.showinfo("Result", msg)
            self.timer.reset()
            self.make_menu()

        self.styled_button(text="Submit", command=submit).pack(pady=10)
        self.styled_button(text="Back", command=self.make_menu).pack(pady=5)

    def scramble_game(self):
        self.clear()
        self.scramble = self.game.get_random_scramble_word()
        scrambled_word = self.game.scramble_word(self.scramble['word'])

        self.styled_label(text="Word Scramble", font=("Arial", 16)).pack(pady=10)
        self.styled_label(text=f"Unscramble: {scrambled_word.upper()}", font=("Arial", 14), fg="green").pack(pady=10)

        entry = tk.Entry(self.win, font=("Arial", 14), width=20)
        entry.pack(pady=10)
        entry.focus()

        def check():
            ans = entry.get().strip().lower()
            if ans == self.scramble['word'].lower():
                messagebox.showinfo("Correct", f"Nice! The answer is '{self.scramble['word']}'")
            else:
                messagebox.showinfo("Incorrect", f"Nope! The answer was '{self.scramble['word']}'")
            self.scramble_game()

        self.styled_button(text="Check", command=check).pack(pady=10)
        self.styled_button(text="Hint", command=lambda: messagebox.showinfo("Hint", self.scramble.get('hint', 'No hint.'))).pack(pady=5)
        self.styled_button(text="Back", command=self.make_menu).pack(pady=5)

    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
    TypingGame().run()
