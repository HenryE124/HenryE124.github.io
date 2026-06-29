import random
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Person:

    def __init__(self, sirstatus, lifestatus):
        if sirstatus == None:
            self._sirstatus = 'S'
        else:
            self._sirstatus = sirstatus
        self._lifestatus = 'L'

    def get_lifestatus(self):
        return self._lifestatus

    def set_lifestatus(self, lifestatus):
        self._lifestatus = lifestatus

    def get_sirstatus(self):
        return self._sirstatus

    def set_sirstatus(self, sirstatus):
        self._sirstatus = sirstatus


class SimulationApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Epidemiology Dashboard")
        self.root.geometry("1100x700")
        
        # Configure Main Layout Grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left Panel - Input Controls
        control_frame = ttk.LabelFrame(root, text=" Parameters ", padding=15)
        control_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.i_var = tk.StringVar("5")
        self.r_var = tk.StringVar("0")
        self.s_var = tk.StringVar("95")
        self.beta_var = tk.StringVar("0.1")
        self.gamma_var = tk.StringVar("0.05")
        self.numsim_var = tk.StingVar("5")

        
        fields = [
            ("Infected Population:", self.i_var),
            ("Recovered Population:", self.r_var),
            ("Sick Population:", self.s_var),
            ("Chance of Infection:", self.beta_var)
            ("Chance of Recovery:", self.gamma_var)
            ("Number of Simulations:", self.numsim_var)
        ]

        for idx, (label_text, var) in enumerate(fields):
            lbl = ttk.Label(control_frame, text=label_text)
            lbl.grid(row=idx * 2, column=0, sticky="w", pady=(5, 0))
            entry = ttk.Entry(control_frame, textvariable=var, width=25)
            entry.grid(row=idx * 2 + 1, column=0, sticky="ew", pady=(0, 10))

    
        # Run Button
        self.run_btn = ttk.Button(
            control_frame, text="Run Simulation", command=self.start_simulation
        )
        self.run_btn.grid(row=17, column=0, pady=(15, 5), sticky="ew")

        # Status text element
        self.status_lbl = ttk.Label(
            control_frame, text="Status: Ready", font=("Helvetica", 9, "italic")
        )
        self.status_lbl.grid(row=16, column=0, pady=5, sticky="w")

        # Right Panel - Matplotlib Plot
        self.plot_frame = ttk.Frame(root, padding=15)
        self.plot_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # Setup initial Matplotlib figure embedded into Tkinter
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.ax.set_title("Tracking Infection Across Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Infected Population")
        self.ax.set_ylim(0, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_simulation(self):
        try:
            i = int(self.i_var.get())
            r = int(self.r_var.get())
            s = int(self.s_var.get())
            beta = float(self.beta_var.get())
            gamma = float(self.gamma_var.get())
            numsim = int(self.numsim_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric fields.")
            return
        if not (0 < beta < 1):
            messagebox.showerror("Input Error", "Please enter valid numeric fields.")
            return
        if not (0 < gamma < 1):
            messagebox.showerror("Input Error", "Please enter valid numeric fields.")
            return

        self.run_btn.config(state="disabled")
        self.status_lb1.config(text="Status: Simulating")

        sim_args = (i, r, s, beta, gamma)
        threading.Thread(
            target=self.run_simulation_logic, args=sim_args, daemon=True
        ).start()

    def run_simulation_logic(self, i, r, s, beta, gamma, numsim):
        self.ax.clear()
        self.ax.set_title("Tracking Infection Accross Time")
        self.ax.set_xlabel("Week")
        self.ax.set_ylabel("Infected Population (%)")

        for a in range(numsim):
            population = []
            history = [(i/(i + r + s))]
            week = 0
            
            for _ in range(s):
                population.append(Person('S', 'L'))
            for _ in range(r):
                population.append(Person('R', 'L'))
            for _ in range(i):
                population.append(Person('I', 'L'))
                
            while s >= 1:
                spop = [q for q in population if q._sirstatus == 'S']
                rpop = [q for q in population if q._sirstatus == 'R']
                ipop = [q for q in population if q._sirstatus == 'I']

                ds = -(beta * s * r)/(s + r + i)
                di = (beta * s * r)/(s + r + i) - gamma * i
                dr = gamma * i
                if round(ds) == 0:
                    continue
                else:
                    for _ in range(round(ds)):
                        q = random.choice(spop)
                        q.set_sirstatus('I')
                if round(dr) == 0:
                    continue
                else:
                    for _ in range(round(dr)):
                        q = random.choice(ipop)
                        q.set_sirstatus('R')

                history.append(i/(i+r+s))
                week += 1
                
            # Map calculated lineage pathway safely to chart line
            self.ax.plot(history, label=f"Trial {g+1}")

        # Update plotting asset directly on Main App Screen safely
        self.root.after(0, self.update_ui_complete)
        
    def update_ui_complete(self):
        """Refreshes canvas view layout assets safely on completion."""
        self.canvas.draw()
        self.run_btn.config(state="normal")
        self.status_lbl.config(text="Status: Done!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
