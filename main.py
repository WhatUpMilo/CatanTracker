import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict

theoretical_probs = {
    2: 1 / 36, 3: 2 / 36, 4: 3 / 36, 5: 4 / 36,
    6: 5 / 36, 7: 6 / 36, 8: 5 / 36, 9: 4 / 36,
    10: 3 / 36, 11: 2 / 36, 12: 1 / 36
}

DEVIATION_THRESHOLD = 0.05


class DiceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Catan Dice Tracker")
        self.sum_counts = defaultdict(int)
        self.total_rolls = 0
        self.current_player = 1
        self.num_players = 0

        self.setup_widgets()

    def setup_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid()

        # Player count
        ttk.Label(self.main_frame, text="Number of Players:").grid(column=0, row=0)
        self.players_entry = ttk.Entry(self.main_frame, width=5)
        self.players_entry.grid(column=1, row=0)

        # Mode selection
        ttk.Label(self.main_frame, text="Mode:").grid(column=0, row=1)
        self.mode_var = tk.StringVar(value="manual")
        ttk.Radiobutton(self.main_frame, text="Manual", variable=self.mode_var, value="manual").grid(column=1, row=1)
        ttk.Radiobutton(self.main_frame, text="Automatic", variable=self.mode_var, value="automatic").grid(column=2,
                                                                                                           row=1)

        # Start button
        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.start_game)
        self.start_button.grid(column=0, row=2, columnspan=3, pady=10)

        # Output area
        self.output_text = tk.Text(self.root, width=80, height=25, wrap=tk.WORD)
        self.output_text.grid(padx=10, pady=10)

        # Manual entry area
        self.manual_entry = ttk.Entry(self.root, width=10)
        self.manual_button = ttk.Button(self.root, text="Enter Roll", command=self.manual_roll)

    def start_game(self):
        try:
            self.num_players = int(self.players_entry.get())
            if self.num_players <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of players.")
            return

        self.sum_counts.clear()
        self.total_rolls = 0
        self.current_player = 1
        self.output_text.delete("1.0", tk.END)

        if self.mode_var.get() == "automatic":
            self.run_automatic_mode()
        else:
            self.run_manual_mode()

    def run_automatic_mode(self):
        rounds = random.randint(15, 17)
        for round_num in range(1, rounds + 1):
            self.output_text.insert(tk.END, f"--- Round {round_num} ---\n")
            for player in range(1, self.num_players + 1):
                roll = random.randint(1, 6) + random.randint(1, 6)
                self.sum_counts[roll] += 1
                self.total_rolls += 1
                self.output_text.insert(tk.END, f"Player {player} rolled a {roll}\n")
            self.output_text.insert(tk.END, "\n")

        self.display_results()

    def run_manual_mode(self):
        self.manual_entry.grid()
        self.manual_button.grid()
        self.output_text.insert(tk.END, f"Manual Mode: Player {self.current_player}, enter your roll (2-12).\n")

    def manual_roll(self):
        try:
            roll = int(self.manual_entry.get())
            if 2 <= roll <= 12:
                self.sum_counts[roll] += 1
                self.total_rolls += 1
                self.output_text.insert(tk.END, f"Player {self.current_player} entered {roll}\n")
                self.current_player += 1
                if self.current_player > self.num_players:
                    self.current_player = 1
                    if self.total_rolls >= self.num_players * 3:
                        self.display_results()
                self.output_text.insert(tk.END, f"Next: Player {self.current_player}, enter your roll.\n")
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Roll", "Enter a valid sum between 2 and 12.")
        finally:
            self.manual_entry.delete(0, tk.END)

    def display_results(self):
        self.output_text.insert(tk.END, "\n--- Empirical Probability Table ---\n")
        for s in range(2, 13):
            freq = self.sum_counts[s]
            prob = freq / self.total_rolls if self.total_rolls else 0
            self.output_text.insert(tk.END, f"Sum {s}: Count = {freq}, Probability = {prob:.4f}\n")

        self.output_text.insert(tk.END, "\n--- Deviation from Theoretical Probabilities ---\n")
        lucky = []
        for s in range(2, 13):
            theo = theoretical_probs[s]
            emp = self.sum_counts[s] / self.total_rolls if self.total_rolls else 0
            dev = abs(emp - theo)
            self.output_text.insert(tk.END, f"Sum {s}: Theo = {theo:.4f}, Emp = {emp:.4f}, Dev = {dev:.4f}\n")
            if dev >= DEVIATION_THRESHOLD:
                if emp > theo:
                    lucky.append(f"{s} is unusually lucky!")
                else:
                    lucky.append(f"{s} is surprisingly rare!")

        self.output_text.insert(tk.END, "\n--- Interpretation ---\n")
        if lucky:
            for msg in lucky:
                self.output_text.insert(tk.END, msg + "\n")
        else:
            self.output_text.insert(tk.END, "No lucky or unlucky numbers yet.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiceTrackerGUI(root)
    root.mainloop()
