import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import keyboard
import time

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rebellious Calculator")
        
        # Make window resizable
        self.root.resizable(True, True)
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Initialize chaos_enabled before using it
        self.chaos_enabled = tk.BooleanVar(value=True)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)

        # Help button
        help_button = ttk.Button(main_frame, text="How It Works", command=self.show_help)
        help_button.grid(row=0, column=0, pady=5, sticky=tk.W)

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Number of presses input
        self.presses_label = ttk.Label(input_frame, text="Number of Presses:")
        self.presses_label.grid(row=0, column=0, padx=5)
        self.presses_var = tk.StringVar(value="500")
        self.presses_entry = ttk.Entry(input_frame, textvariable=self.presses_var, width=10)
        self.presses_entry.grid(row=0, column=1, padx=5)
        
        # Run button
        self.run_button = ttk.Button(input_frame, text="Start Simulation", 
                                   command=self.toggle_simulation)
        self.run_button.grid(row=0, column=2, padx=5)
        
        # Combined control frame for speed and chaos
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Controls", padding="5")
        control_frame.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        control_frame.grid_columnconfigure(1, weight=1)  # Make slider expand

        # Speed slider with minimal labels
        ttk.Label(control_frame, text="Fast").grid(row=0, column=0, padx=5, pady=5)
        self.speed_var = tk.DoubleVar(value=100.0)  # Default to middle speed
        self.speed_slider = ttk.Scale(
            control_frame,
            from_=1,     # Super fast (1ms delay)
            to=400,      # Very slow (400ms delay)
            orient='horizontal',
            variable=self.speed_var
        )
        self.speed_slider.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Label(control_frame, text="Slow").grid(row=0, column=2, padx=5)

        # Chaos toggle in the same frame
        self.chaos_enabled = tk.BooleanVar(value=True)
        self.chaos_toggle = ttk.Checkbutton(
            control_frame,
            text="Enable Chaos",
            variable=self.chaos_enabled,
            command=self.update_chaos_display
        )
        self.chaos_toggle.grid(row=0, column=4, padx=15)

        # Output text
        self.output_text = tk.Text(main_frame, height=10, width=50)
        self.output_text.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Create figure frame with weight
        figure_frame = ttk.Frame(main_frame)
        figure_frame.grid(row=4, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        figure_frame.grid_columnconfigure(0, weight=1)
        figure_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)

        # Create figure with dynamic size
        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=figure_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Custom control buttons frame
        button_frame = ttk.Frame(figure_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Add placeholder buttons (you can customize these later)
        ttk.Button(button_frame, text="Reset View").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Save Plot").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Clear Data").pack(side=tk.LEFT, padx=2)

        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        self.fig.canvas.draw()
        
        # Set minimum window size
        self.root.minsize(400, 600)
        
        # Add chaos toggle and explanation
        self.chaos_frame = ttk.LabelFrame(main_frame, text="Chaos Control", padding="5")
        self.chaos_frame.grid(row=5, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Chaos level display
        self.chaos_level = 0
        self.chaos_bar = ttk.Progressbar(self.chaos_frame, length=200, mode='determinate')
        self.chaos_bar.grid(row=1, column=0, padx=5, pady=5)
        self.chaos_label = ttk.Label(self.chaos_frame, text="0%")
        self.chaos_label.grid(row=1, column=1, padx=5)
        
        # Initialize variables for interactive mode
        self.running = False
        self.total = 0
        self.press_count = 0
        self.totals = []
        
        # Add simulation control variables
        self.simulation_running = False
        self.auto_running = False
        
        # Bind window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def calculate_next_value(self):
        """Calculate the next value based on press count and chaos level"""
        # Calculate chaos level if enabled
        if self.chaos_enabled.get() and self.press_count > 100:
            self.chaos_level = min(1, (self.press_count - 100) / 400)
        else:
            self.chaos_level = 0
        
        # Update chaos bar
        chaos_percent = int(self.chaos_level * 100)
        self.chaos_bar['value'] = chaos_percent
        self.chaos_label['text'] = f"{chaos_percent}%"
        
        # First 5 presses: strict rules
        if self.press_count <= 5:
            return 1 if self.press_count % 2 == 1 else -1
            
        # After 5 presses: chaos influenced operations
        if random.random() < self.chaos_level:
            # High chaos: more extreme operations
            return random.choice([3, -3])
        else:
            # Low chaos: normal operations
            return random.choice([1, -1, 2, -2])

    def update_plot(self):
        """Update the plot with current data"""
        try:
            self.ax.clear()
            if self.totals:  # Only plot if we have data
                self.ax.plot(range(len(self.totals)), self.totals)
                self.ax.set_xlabel("Presses")
                self.ax.set_ylabel("Total")
                self.ax.set_title("Calculator Rebellion: Total Over Time")
                self.ax.grid(True)
                
                # Adjust layout to prevent cutoff
                self.fig.tight_layout()
                
            self.canvas.draw()
        except Exception as e:
            print(f"Plot update error: {e}")

    def on_closing(self):
        """Handle cleanup when window is closed"""
        try:
            self.auto_running = False
        except Exception as e:
            print(f"Cleanup error: {e}")
        finally:
            self.root.destroy()
            self.root.quit()

    def toggle_simulation(self):
        """Toggle the simulation on/off"""
        if self.auto_running:
            # Stop the simulation
            self.auto_running = False
            self.run_button.config(text="Start Simulation")
        else:
            # Start the simulation
            try:
                total_presses = int(self.presses_var.get())
                if total_presses <= 0:
                    raise ValueError("Number of presses must be positive")
                
                self.auto_running = True
                self.run_button.config(text="Stop Simulation")
                
                self.press_count = 0
                self.total = 0
                self.totals = []
                self.output_text.delete(1.0, tk.END)
                self.ax.clear()
                self.run_simulation_step()
                
            except ValueError as e:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Error: {str(e)}")

    def update_speed_label(self, *args):
        """Update the speed label when slider changes"""
        delay = self.speed_var.get()
        updates_per_sec = int(1000 / delay)
        self.speed_label.config(text=f"Speed: {updates_per_sec} updates/sec")

    def run_simulation_step(self):
        """Run one step of the simulation"""
        if not self.auto_running:
            return
            
        try:
            total_presses = int(self.presses_var.get())
            
            if self.press_count < total_presses:
                self.press_count += 1
                change = self.calculate_next_value()
                self.total += change
                self.totals.append(self.total)
                
                # Limit updates to prevent overwhelming the GUI
                if len(self.totals) % max(1, int(self.press_count / 2000)) == 0:
                    if self.press_count % 50 == 0:
                        self.output_text.insert(tk.END, 
                            f"Press {self.press_count}: Total = {self.total}\n")
                        self.output_text.see(tk.END)
                    
                    # Update plot in real-time
                    self.update_plot()
                
                # Calculate delay with a minimum threshold
                delay = int(self.speed_var.get())
                delay = max(1, int(delay ** 1.5 / 40))  # More aggressive scaling, minimum 1ms delay
                
                # Schedule next update if still running
                if self.auto_running:
                    self.root.after(delay, self.run_simulation_step)
            else:
                # Simulation complete
                self.auto_running = False
                self.run_button.config(text="Start Simulation")
                self.output_text.insert(tk.END, "\n=== Final Results ===\n")
                self.output_text.insert(tk.END, f"Final total: {self.total}\n")
                self.update_plot()  # Final plot update
                
        except Exception as e:
            print(f"Simulation error: {e}")  # Debug output
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
            self.auto_running = False
            self.run_button.config(text="Start Simulation")

    def update_chaos_display(self):
        """Update chaos display based on toggle state"""
        if not self.chaos_enabled.get():
            self.chaos_bar['value'] = 0
            self.chaos_label['text'] = "0%"
            self.chaos_level = 0

    def on_resize(self, event):
        """Handle window resize"""
        if event.widget == self.root:
            # Update figure size
            try:
                # Get frame size
                width = event.width - 40  # Adjust for padding
                height = int(width * 0.6)  # Maintain aspect ratio
                
                # Update figure size
                self.fig.set_size_inches(width/100, height/100)
                
                # Redraw plot
                self.update_plot()
            except Exception as e:
                print(f"Resize error: {e}")

    def show_technical_details(self, parent_dialog):
        """Show deeper analysis in a new modal"""
        analysis_dialog = tk.Toplevel(parent_dialog)
        analysis_dialog.title("Mathematical & Philosophical Analysis")
        analysis_dialog.geometry("600x500")
        
        # Make dialog modal
        analysis_dialog.transient(parent_dialog)
        analysis_dialog.grab_set()
        
        # Add content frame
        content_frame = ttk.Frame(analysis_dialog, padding="20")
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        analysis_dialog.grid_columnconfigure(0, weight=1)
        analysis_dialog.grid_rowconfigure(0, weight=1)

        # Analysis text
        analysis_text = """The Mathematics and Philosophy of Chaos

MATHEMATICAL FOUNDATIONS:

1. Random Walk Properties
   • The system begins as a simple alternating sequence
   • Transitions into a modified random walk
   • Final phase introduces weighted probability distributions
   • Creates a unique form of controlled randomness

2. Statistical Behavior
   • Early Phase: Zero mean, minimal variance
   • Middle Phase: Slight positive bias in expected value
   • Chaos Phase: Increasing variance with time
   • Emergence of complex patterns through simple rules

3. Chaos Theory Connections
   • Demonstrates sensitive dependence on initial conditions
   • Shows emergence of complexity from simple rules
   • Exhibits phase transitions between order and chaos
   • Parallels with butterfly effect in chaotic systems

PHILOSOPHICAL IMPLICATIONS:

1. Order vs. Chaos
   • Initial order represents rigid, deterministic systems
   • Transition phase mirrors real-world complexity
   • Final chaos reflects natural entropy increase
   • Questions determinism vs. randomness in nature

2. Emergence and Complexity
   • Simple rules create complex behaviors
   • Local interactions lead to global patterns
   • Parallels with natural system evolution
   • Demonstrates emergence in mathematical systems

3. Predictability and Control
   • Early phase: Complete predictability
   • Middle phase: Statistical predictability
   • Chaos phase: Fundamental unpredictability
   • Reflects limits of knowledge and control

4. Metaphysical Questions
   • Nature of randomness vs. determinism
   • Role of initial conditions in system evolution
   • Relationship between simplicity and complexity
   • Boundaries between order and chaos

5. Real-World Parallels
   • Financial market fluctuations
   • Population dynamics in ecology
   • Social system evolution
   • Weather pattern development

6. Philosophical Questions Raised
   • Is true randomness possible?
   • Can chaos be controlled?
   • Does complexity require chaos?
   • Is order emergent from chaos, or vice versa?"""

        # Add scrollable text widget
        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=60, height=20)
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insert analysis text
        text_widget.insert('1.0', analysis_text)
        text_widget.configure(state='disabled')  # Make text read-only
        
        # Close button
        close_button = ttk.Button(content_frame, text="Close", command=analysis_dialog.destroy)
        close_button.grid(row=1, column=0, columnspan=2, pady=(20,0))
        
        # Configure content frame grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Center the dialog
        analysis_dialog.update_idletasks()
        x = parent_dialog.winfo_x() + (parent_dialog.winfo_width() - analysis_dialog.winfo_width()) // 2
        y = parent_dialog.winfo_y() + (parent_dialog.winfo_height() - analysis_dialog.winfo_height()) // 2
        analysis_dialog.geometry(f"+{x}+{y}")

    def show_help(self):
        """Show the help dialog"""
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title("How It Works")
        help_dialog.geometry("500x400")
        
        # Make dialog modal
        help_dialog.transient(self.root)
        help_dialog.grab_set()
        
        # Add content frame
        content_frame = ttk.Frame(help_dialog, padding="20")
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        help_dialog.grid_columnconfigure(0, weight=1)
        help_dialog.grid_rowconfigure(0, weight=1)

        # Help text
        help_text = """The Rebellious Calculator: A Journey from Order to Chaos

PHASES OF REBELLION:

1. Orderly Phase (First 5 Presses)
   • Odd presses: Add 1
   • Even presses: Subtract 1
   • Perfectly predictable behavior

2. Standard Chaos (Presses 6-100)
   • Randomly chooses between: +1, -1, +2, -2
   • Each operation has equal probability
   • Introduces unpredictability

3. Growing Chaos (After Press 100)
   • Chaos level gradually increases
   • Higher chaos introduces extreme operations (+3, -3)
   • Probability of extreme operations increases with chaos
   • Maximum chaos reached at press 500

CONTROLS:
• Speed Slider: Adjust simulation speed
• Chaos Toggle: Enable/disable growing chaos
• Start/Stop: Control simulation progress

The graph shows the total value over time, revealing the 
transition from orderly behavior to chaos."""

        # Add scrollable text widget
        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=50, height=15)
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insert help text
        text_widget.insert('1.0', help_text)
        text_widget.configure(state='disabled')  # Make text read-only
        
        # Button frame
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(20,0))
        
        # Change button text to match new content
        analysis_button = ttk.Button(button_frame, text="Deep Analysis", 
                               command=lambda: self.show_technical_details(help_dialog))
        analysis_button.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_button = ttk.Button(button_frame, text="Close", command=help_dialog.destroy)
        close_button.pack(side=tk.LEFT, padx=5)
        
        # Configure content frame grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Center the dialog
        help_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - help_dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - help_dialog.winfo_height()) // 2
        help_dialog.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
