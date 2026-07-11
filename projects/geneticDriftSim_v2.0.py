import random
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Person:

    def __init__(self, parm, parf, af1):
        self._parm = parm
        self._parf = parf
        self._gender = random.randint(0, 1)
        self._age = 0
        if parm is None and parf is None:
            self._allele1 = "A" if random.random() < af1 else "a"
            self._allele2 = "A" if random.random() < af1 else "a"
        else:
            self._allele1 = parm.get_allele()
            self._allele2 = parf.get_allele()

    def get_allele(self):
        return random.choice([self._allele1, self._allele2])


class SimulationApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Population Genetics Simulator")
        self.root.geometry("1100x700")

        # Configure Main Layout Grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left Panel - Input Controls
        control_frame = ttk.LabelFrame(root, text=" Parameters ", padding=15)
        control_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Input variables
        self.pop_var = tk.StringVar(value="100")
        self.af1_var = tk.StringVar(value="0.5")
        self.gen_var = tk.StringVar(value="50")
        self.numsim_var = tk.StringVar(value="5")
        self.lif_var = tk.StringVar(value="4.0")
        self.kid_var = tk.StringVar(value="2.1")
        self.cc_var = tk.StringVar(value="200")
        self.fc_var = tk.StringVar(value="1.0")

        # Render input fields dynamically
        fields = [
            ("Initial Population Size:", self.pop_var),
            ("Allele 'A' Frequency (0-1):", self.af1_var),
            ("Number of Generations:", self.gen_var),
            ("Simulation Runs (Trials):", self.numsim_var),
            ("Avg Life Expectancy (Gen):", self.lif_var),
            ("Avg Kids per Female:", self.kid_var),
            ("Carrying Capacity:", self.cc_var),
            ("Fitness Coefficient of 'aa' (0-1):", self.fc_var),
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
        self.ax.set_title("Allele A Frequency Over Time")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Frequency")
        self.ax.set_ylim(0, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_simulation(self):
        """Validates inputs and triggers background calculation thread."""
        try:
            pop = int(self.pop_var.get())
            af1 = float(self.af1_var.get())
            gen = int(self.gen_var.get())
            numsim = int(self.numsim_var.get())
            lif = float(self.lif_var.get())
            kid = float(self.kid_var.get())
            cc = int(self.cc_var.get())
            fc = float(self.fc_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric fields.")
            return

        if not (0 < af1 < 1):
            messagebox.showerror(
                "Input Error", "Allele frequency must be strictly between 0 and 1."
            )
            return

        if (
            pop <= 0
            or gen <= 0
            or numsim <= 0
            or cc <= 0
            or lif <= 0
            or kid < 0
            or fc < 0
        ):
            messagebox.showerror(
                "Input Error", "Numeric values must be greater than or equal to 0."
            )
            return

        # Disable button to prevent overlapping simulation tasks
        self.run_btn.config(state="disabled")
        self.status_lbl.config(text="Status: Simulating... please wait.")

        # --- FIX: Added 'fc' to the tuple below ---
        sim_args = (pop, af1, gen, numsim, lif, kid, cc, fc)
        threading.Thread(
            target=self.run_simulation_logic, args=sim_args, daemon=True
        ).start()

    def run_simulation_logic(self, pop, af1, gen, numsim, lif, kid, cc, fc):
        """Processes simulation mathematical computations."""
        self.ax.clear()
        self.ax.set_title("Allele A Frequency Over Time")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Frequency")
        self.ax.set_ylim(0, 1)
        self.ax.set_xlim(0, gen)

        for g in range(numsim):
            population = []
            history = [af1]  # Track starting point at gen 0

            # Generate baseline population
            for _ in range(pop):
                population.append(Person(None, None, af1))

            for i in range(gen):
                homd = homr = het = 0
                new_population = []
                males = [p for p in population if p._gender == 1]

                # Process lifespans and reproduction cycles
                for j in population:
                    j._age += 1
                    rand1 = random.uniform(lif - 1, lif + 1)
                    if rand1 >= j._age:
                        new_population.append(j)

                    # Females breed exactly at generation index age 2 if males exist
                    if j._gender == 0 and j._age == 2 and males:
                        guy = random.choice(males)
                        if j._allele1 == "a" and j._allele2 == "a":
                            rand2 = random.uniform(0, kid * 2 * fc)
                        else:
                            rand2 = random.uniform(0, kid * 2)
                        for _ in range(round(rand2)):
                            new_population.append(Person(guy, j, af1))
                # Handle Environmental Carrying Capacity Cap
                if len(new_population) > cc:
                    new_population = new_population[-cc:]

                population = new_population

                # If population crashes completely, track final state and stop calculation
                if not population:
                    history.append(0)
                    continue

                # Count genotypes present inside generation group
                for l in population:
                    if l._allele1 == "A" and l._allele2 == "A":
                        homd += 1
                    elif l._allele1 == "a" and l._allele2 == "a":
                        homr += 1
                    else:
                        het += 1

                total_alleles = 2 * (homd + het + homr)
                freq_A = (homd * 2 + het) / total_alleles if total_alleles > 0 else 0
                history.append(freq_A)
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
