import tkinter as tk
from tkinter import ttk
import random
import time

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.configure(bg="#ACE1AF")  
        self.root.label = tk.Label(self.root, text="Typing Speed Tester",font=("Times New Roman",17,"bold"),fg="black",bg="#ACE1AF")  
        self.root.label.pack()
        self.sentences = {
            "Easy": [
                "The only limit to our realization of tomorrow will be our doubts of today."
                "Hello, World! This is a typing speed test."
                "The quick brown fox jumps over the lazy dog.",
                "In the beginning God created the heavens and the earth.",
                "Practice makes perfect.", 
            ],
            "Medium": [
                "The quick brown fox jumps over the lazy dog. Programming is fun and rewarding.",
                "Practice makes perfect. Hello, World! This is a typing speed test."
            ],
            "Hard": [
                "The quick brown fox jumps over the lazy dog.",
                "Programming is fun and rewarding. Practice makes perfect.",
                "Hello, World! This is a typing speed test. Choose the passage type to practice."
                "In the beginning God created the heavens and the earth.To be or not to be, that is the question.",
                "All that glitters is not gold.It was the best of times, it was the worst of times.",         
            ]
        }

        self.current_difficulty = tk.StringVar()
        self.current_difficulty.set("Easy")
        self.current_sentence_type = tk.StringVar()
        self.current_sentence_type.set("Lines") 
        self.current_sentence = tk.StringVar()
        self.current_sentence.set(self.get_random_sentence())
        self.start_time = None
        self.scores = []
        self.create_widgets()

    def create_widgets(self):
        self.label_sentence_type = tk.Label(self.root, text="Input:", font=("Arial", 15,"bold"),fg="brown", bg="#ACE1AF")
        self.label_sentence_type.pack(pady=5)

        self.dropdown_sentence_type = ttk.Combobox(self.root, values=["Lines", "Passages"], style="Custom.TCombobox")
        self.dropdown_sentence_type.set("Lines")  
        self.dropdown_sentence_type.pack(pady=10)
        self.dropdown_sentence_type.bind("<<ComboboxSelected>>", self.change_sentence_type)
        
        self.label_difficulty = tk.Label(self.root, text="Level:", font=("arial", 15,"bold"),fg="brown",bg="#ACE1AF")
        self.label_difficulty.pack(pady=5)
        
        self.dropdown_difficulty = ttk.Combobox(self.root, values=["Easy", "Medium", "Hard"], style="Custom.TCombobox")
        self.dropdown_difficulty.set("Easy")
        self.dropdown_difficulty.pack(pady=10)
        self.dropdown_difficulty.bind("<<ComboboxSelected>>", self.change_difficulty)


        self.label_sentence = tk.Label(self.root, textvariable=self.current_sentence, font=("Arial", 14), bg="#ACE1AF")
        self.label_sentence.pack(pady=20)

        self.entry_typing = tk.Entry(self.root, font=("Arial", 12), bg="#FFFFFF")  
        self.entry_typing.pack(pady=10)

        self.button_start = tk.Button(self.root, text="Start Test", command=self.start_test, bg="green", fg="black", font=("Arial", 12))
        self.button_start.pack(pady=10)

        self.button_stop = tk.Button(self.root, text="Stop", command=self.stop_test, bg="#006D5B", fg="black", font=("Arial", 12))
        self.button_stop.pack(pady=10)
        self.button_stop["state"] = "disabled"

        self.button_restart = tk.Button(self.root, text="Restart", command=self.restart_test, bg="#05472A", fg="black", font=("Arial", 12))
        self.button_restart.pack(pady=10)
        self.button_restart["state"] = "disabled"

        self.label_timer = tk.Label(self.root, text="Time: 0s", font=("Arial", 16,"bold"),fg="#BA850D", bg="#ACE1AF")
        self.label_timer.pack(pady=10)

        self.label_result = tk.Label(self.root, text="", font=("Arial", 12),bg="#ACE1AF")
        self.label_result.pack(pady=10)

        self.label_scores = tk.Label(self.root, text="Scores:", font=("Arial", 19,"bold"),fg="#6D0012", bg="#ACE1AF")
        self.label_scores.pack(pady=10)

        style = ttk.Style()
        style.configure("Custom.TCombobox", padding=(5, 5, 5, 5), background="#FFFFFF")

    def change_difficulty(self, event):
        self.current_difficulty.set(self.dropdown_difficulty.get())
        self.current_sentence.set(self.get_random_sentence())

    def change_sentence_type(self, event):
        self.current_sentence_type.set(self.dropdown_sentence_type.get())
        self.current_sentence.set(self.get_random_sentence())

    def get_random_sentence(self):
        return random.choice(self.sentences[self.current_difficulty.get()])

    def start_test(self):
        self.current_sentence.set(self.get_random_sentence())
        self.entry_typing.delete(0, 'end') 
        self.start_time = time.time()
        self.update_timer()
        self.button_start["state"] = "disabled"
        self.button_stop["state"] = "normal"
        self.button_restart["state"] = "normal"
        self.root.bind("<Return>", self.check_result)

    def stop_test(self):
        self.root.after_cancel(self.update_timer)
        self.button_start["state"] = "normal"
        self.button_stop["state"] = "disabled"
        self.button_restart["state"] = "normal"
        self.root.unbind("<Return>")

    def restart_test(self):
        self.stop_test()
        self.label_result.config(text="")
        self.start_test()

    def update_timer(self):
        if self.start_time is not None:  
            elapsed_time = time.time() - self.start_time
            self.label_timer.config(text=f"Time: {int(elapsed_time)}s")
            self.root.after(1000, self.update_timer)

    def check_result(self, event):
        user_input = self.entry_typing.get()
        original_sentence = self.current_sentence.get()

        if user_input == original_sentence:
            elapsed_time = time.time() - self.start_time
            points = len(original_sentence.split())  
            accuracy = 100
        else:
            points = 0
            accuracy = round((len(set(original_sentence.split()) & set(user_input.split())) / len(original_sentence.split())) * 100, 2)

        result_text = f"Your score: {points} points\nAccuracy: {accuracy}%"
        self.label_result.config(text=result_text)
        self.scores.append({"Points": points, "Accuracy": accuracy})
        self.update_scores_label()
        self.button_start["state"] = "normal"
        self.button_stop["state"] = "disabled"
        self.button_restart["state"] = "normal"
        self.root.unbind("<Return>")

    def update_scores_label(self):
        scores_text = "Scores:\n"
        for i, score in enumerate(self.scores, start=1):
            scores_text += f"{i}. Points: {score['Points']}, Accuracy: {score['Accuracy']}%\n"
        self.label_scores.config(text=scores_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTester(root)
    root.mainloop()
