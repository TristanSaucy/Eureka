import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rebellious Calculator")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Theory box
        theory_frame = ttk.LabelFrame(main_frame, text="How It Works", padding="5")
        theory_frame.grid(row=0, column=0, pady=10, sticky=(tk.W, tk.E))
        
        theory_text = """This is a rebellious calculator that follows two phases:

1. First 5 Presses (Orderly Phase):
   • Odd presses: Add 1
   • Even presses: Subtract 1

2. After 5 Presses (Chaos Phase):
   • Randomly chooses between: +1, -1, +2, -2
   • Each operation has equal probability

The graph shows how the total changes over time, revealing the transition 
from orderly behavior to chaos."""
        
        ttk.Label(theory_frame, text=theory_text, justify=tk.LEFT, wraplength=500).grid(row=0, column=0)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, pady=10)
        
        # Number of presses input
        ttk.Label(input_frame, text="Number of Presses:").grid(row=0, column=0, padx=5)
        self.presses_var = tk.StringVar(value="500")
        self.presses_entry = ttk.Entry(input_frame, textvariable=self.presses_var, width=10)
        self.presses_entry.grid(row=0, column=1, padx=5)
        
        # Run button
        ttk.Button(input_frame, text="Run Simulation", command=self.run_simulation).grid(row=0, column=2, padx=5)
        
        # Output text
        self.output_text = tk.Text(main_frame, height=10, width=50)
        self.output_text.grid(row=2, column=0, pady=10)
        
        # Create figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, pady=10)

    def run_simulation(self):
        try:
            total_presses = int(self.presses_var.get())
            if total_presses <= 0:
                raise ValueError("Number of presses must be positive")
            
            # Clear previous output
            self.output_text.delete(1.0, tk.END)
            self.ax.clear()
            
            # Run simulation
            total = 0
            presses = 0
            log = []
            totals = []

            self.output_text.insert(tk.END, "Starting total: 0\n")

            for _ in range(total_presses):
                presses += 1

                if presses <= 5:
                    if presses % 2 == 1:
                        total += 1
                        log.append("+1")
                    else:
                        total -= 1
                        log.append("-1")
                else:
                    operation = random.choice(["+1", "-1", "+2", "-2"])
                    if operation == "+1":
                        total += 1
                    elif operation == "-1":
                        total -= 1
                    elif operation == "+2":
                        total += 2
                    else:
                        total -= 2
                    log.append(operation)

                totals.append(total)

                if presses % 50 == 0:
                    self.output_text.insert(tk.END, f"Press {presses}: Total = {total}\n")

            self.output_text.insert(tk.END, "\n=== Final Results ===\n")
            self.output_text.insert(tk.END, f"Final total: {total}\n")
            self.output_text.insert(tk.END, f"Most chaotic sequence (last 10 presses): {log[-10:]}\n")

            # Update plot
            self.ax.plot(range(total_presses), totals)
            self.ax.set_xlabel("Presses")
            self.ax.set_ylabel("Total")
            self.ax.set_title("Calculator Rebellion: Total Over Time")
            self.ax.grid(True)
            self.canvas.draw()

        except ValueError as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 