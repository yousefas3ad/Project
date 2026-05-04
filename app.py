### I debuged the full source code . Everything is fine.
import tkinter as tk
from tkinter import ttk, messagebox
import math

class NutritionCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutrition Calculator")
        self.root.geometry("560x780")
        self.root.resizable(False, False)

        # ── Palette ──────────────────────────────────────────────
        self.C = {
            "bg":        "#F5F2ED",   # warm off-white canvas
            "panel":     "#FFFFFF",
            "ink":       "#1A1714",   # near-black
            "muted":     "#7A746E",   # warm gray
            "rule":      "#DDD9D3",   # hairline separator
            "accent":    "#D4521C",   # terracotta
            "accent_lt": "#FAE8DF",   # tint
            "pill_bg":   "#EDE9E4",
            "pill_sel":  "#1A1714",
            "pill_fg":   "#7A746E",
            "pill_sfg":  "#FFFFFF",
        }

        self.root.configure(bg=self.C["bg"])
        self._build()

    # ─────────────────────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────────────────────
    def _build(self):
        outer = tk.Frame(self.root, bg=self.C["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Header ───────────────────────────────────────────────
        hdr = tk.Frame(outer, bg=self.C["bg"])
        hdr.pack(fill="x", pady=(0, 18))

        tk.Label(hdr, text="NUTRITION", font=("Georgia", 24, "bold"),
                 bg=self.C["bg"], fg=self.C["ink"]).pack(side="left")
        tk.Label(hdr, text=" PLAN", font=("Georgia", 24),
                 bg=self.C["bg"], fg=self.C["accent"]).pack(side="left")

        tk.Frame(outer, bg=self.C["rule"], height=1).pack(fill="x", pady=(0, 20))

        # ── Form card ────────────────────────────────────────────
        card = tk.Frame(outer, bg=self.C["panel"],
                        highlightbackground=self.C["rule"],
                        highlightthickness=1)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=self.C["panel"])
        inner.pack(fill="x", padx=20, pady=18)

        # biometrics row
        self._section_label(inner, "BIOMETRICS")
        bio = tk.Frame(inner, bg=self.C["panel"])
        bio.pack(fill="x", pady=(4, 0))
        bio.columnconfigure((0,1,2), weight=1, uniform="col")

        self.age_var    = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self._field(bio, "Age", "yrs", self.age_var,    col=0)
        self._field(bio, "Weight", "kg", self.weight_var, col=1)
        self._field(bio, "Height", "cm", self.height_var, col=2)

        tk.Frame(inner, bg=self.C["rule"], height=1).pack(fill="x", pady=14)

        # gender
        self._section_label(inner, "GENDER")
        self.gender_var = tk.StringVar(value="male")
        gf = tk.Frame(inner, bg=self.C["panel"])
        gf.pack(fill="x", pady=(4, 0))
        self._pill_group(gf, self.gender_var,
                         [("Male","male"), ("Female","female")])

        tk.Frame(inner, bg=self.C["rule"], height=1).pack(fill="x", pady=14)

        # activity
        self._section_label(inner, "ACTIVITY LEVEL")
        self.activity_var = tk.StringVar(value="moderate")
        af = tk.Frame(inner, bg=self.C["panel"])
        af.pack(fill="x", pady=(4, 0))
        self._pill_group(af, self.activity_var,
                         [("Light","light"),
                          ("Moderate","moderate"),
                          ("Very Active","very")])

        tk.Frame(inner, bg=self.C["rule"], height=1).pack(fill="x", pady=14)

        # goal
        self._section_label(inner, "GOAL")
        self.goal_var = tk.StringVar(value="maintain")
        gof = tk.Frame(inner, bg=self.C["panel"])
        gof.pack(fill="x", pady=(4, 0))
        self._pill_group(gof, self.goal_var,
                         [("Maintain","maintain"),
                          ("Lose Weight","lose"),
                          ("Gain Muscle","gain")])

        tk.Frame(inner, bg=self.C["panel"], height=6).pack()

        # ── CTA ──────────────────────────────────────────────────
        btn = tk.Button(outer, text="CALCULATE  →",
                        font=("Georgia", 12, "bold"),
                        bg=self.C["accent"], fg="#FFFFFF",
                        activebackground="#B84418",
                        activeforeground="#FFFFFF",
                        bd=0, padx=0, pady=14,
                        cursor="hand2",
                        command=self.calculate)
        btn.pack(fill="x", pady=18)

        # ── Results card ─────────────────────────────────────────
        self.res_card = tk.Frame(outer, bg=self.C["panel"],
                                 highlightbackground=self.C["rule"],
                                 highlightthickness=1)
        self.res_card.pack(fill="x")
        self.res_card.pack_forget()   # hidden until calculated

        ri = tk.Frame(self.res_card, bg=self.C["panel"])
        ri.pack(fill="x", padx=20, pady=18)

        self._section_label(ri, "YOUR PLAN")
        tk.Frame(ri, bg=self.C["rule"], height=1).pack(fill="x", pady=(6, 14))

        # metric tiles
        tiles = tk.Frame(ri, bg=self.C["panel"])
        tiles.pack(fill="x")
        tiles.columnconfigure((0,1,2,3), weight=1, uniform="tile")

        self.t_cal  = self._tile(tiles, "CALORIES", "kcal", col=0)
        self.t_pro  = self._tile(tiles, "PROTEIN",  "g",    col=1)
        self.t_carb = self._tile(tiles, "CARBS",    "g",    col=2)
        self.t_fat  = self._tile(tiles, "FAT",      "g",    col=3)

        tk.Frame(ri, bg=self.C["rule"], height=1).pack(fill="x", pady=14)

        # secondary row
        sec = tk.Frame(ri, bg=self.C["panel"])
        sec.pack(fill="x")
        sec.columnconfigure((0,1), weight=1, uniform="s")

        self.t_bmi   = self._tile(sec, "BMI", "",  col=0, wide=True)
        self.t_water = self._tile(sec, "WATER", "ml", col=1, wide=True)

        # tip
        self.tip_lbl = tk.Label(ri, text="", font=("Georgia", 9, "italic"),
                                bg=self.C["accent_lt"], fg=self.C["accent"],
                                wraplength=480, justify="left",
                                pady=8, padx=10)
        self.tip_lbl.pack(fill="x", pady=(14, 0))
        self.tip_lbl.pack_forget()

    # ─────────────────────────────────────────────────────────────
    # WIDGET HELPERS
    # ─────────────────────────────────────────────────────────────
    def _section_label(self, parent, text):
        tk.Label(parent, text=text,
                 font=("Courier", 8, "bold"),
                 bg=parent["bg"], fg=self.C["muted"],
                 anchor="w").pack(fill="x")

    def _field(self, parent, label, unit, var, col):
        f = tk.Frame(parent, bg=self.C["panel"])
        f.grid(row=0, column=col, sticky="ew", padx=(0, 8 if col < 2 else 0))

        tk.Label(f, text=label, font=("Courier", 8),
                 bg=self.C["panel"], fg=self.C["muted"]).pack(anchor="w")

        row = tk.Frame(f, bg=self.C["panel"])
        row.pack(fill="x")

        e = tk.Entry(row, textvariable=var, width=7,
                     font=("Georgia", 15),
                     bg=self.C["bg"], fg=self.C["ink"],
                     insertbackground=self.C["accent"],
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=self.C["rule"],
                     highlightcolor=self.C["accent"])
        e.pack(side="left", ipady=6, ipadx=4, fill="x", expand=True)

        tk.Label(row, text=unit, font=("Courier", 8),
                 bg=self.C["panel"], fg=self.C["muted"],
                 padx=4).pack(side="left")

    def _pill_group(self, parent, var, options):
        """Toggle pills — no radiobutton diamonds."""
        self._pill_btns = getattr(self, "_pill_btns", {})
        group_btns = []

        for label, value in options:
            btn = tk.Label(parent, text=label,
                           font=("Courier", 9, "bold"),
                           bg=self.C["pill_bg"],
                           fg=self.C["pill_fg"],
                           padx=12, pady=5, cursor="hand2")
            btn.pack(side="left", padx=(0, 6), pady=(0, 4))
            group_btns.append((btn, value))

            def on_click(v=value, grp=group_btns, sv=var):
                sv.set(v)
                for b, bv in grp:
                    if bv == v:
                        b.config(bg=self.C["pill_sel"], fg=self.C["pill_sfg"])
                    else:
                        b.config(bg=self.C["pill_bg"], fg=self.C["pill_fg"])

            btn.bind("<Button-1>", lambda e, fn=on_click: fn())

        # set initial state
        cur = var.get()
        for b, bv in group_btns:
            if bv == cur:
                b.config(bg=self.C["pill_sel"], fg=self.C["pill_sfg"])

    def _tile(self, parent, label, unit, col, wide=False):
        """Returns (value_label, sub_label) tuple."""
        f = tk.Frame(parent, bg=self.C["accent_lt"],
                     highlightbackground=self.C["rule"],
                     highlightthickness=1)
        f.grid(row=0, column=col, sticky="ew",
               padx=(0, 8 if col == 0 else 0), pady=(0, 4),
               ipadx=8, ipady=8)

        tk.Label(f, text=label, font=("Courier", 7, "bold"),
                 bg=self.C["accent_lt"], fg=self.C["muted"]).pack()

        val = tk.Label(f, text="—",
                       font=("Georgia", 20, "bold"),
                       bg=self.C["accent_lt"], fg=self.C["ink"])
        val.pack()

        sub = tk.Label(f, text=unit, font=("Courier", 8),
                       bg=self.C["accent_lt"], fg=self.C["muted"])
        sub.pack()
        return val, sub

    # ─────────────────────────────────────────────────────────────
    # CALCULATION
    # ─────────────────────────────────────────────────────────────
    def _bmr(self, age, w, h, g):
        base = 10*w + 6.25*h - 5*age
        return base + 5 if g == "male" else base - 161

    def _macros(self, cals, w, goal):
        prot  = w * (2.2 if goal=="gain" else 2.0 if goal=="lose" else 1.8)
        fat   = (cals * 0.25) / 9
        carbs = (cals - prot*4 - fat*9) / 4
        return int(prot), int(fat), int(carbs)

    def _bmi(self, w, h):
        b = w / (h/100)**2
        cat = ("Underweight" if b < 18.5 else
               "Normal"      if b < 25   else
               "Overweight"  if b < 30   else "Obese")
        return round(b, 1), cat

    def calculate(self):
        try:
            age    = int(self.age_var.get())
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
        except ValueError:
            messagebox.showerror("Input error",
                                 "Enter numbers in all three fields.")
            return

        if not (1 <= age <= 120):
            messagebox.showerror("Input error", "Age must be 1–120."); return
        if not (20 <= weight <= 300):
            messagebox.showerror("Input error", "Weight must be 20–300 kg."); return
        if not (100 <= height <= 250):
            messagebox.showerror("Input error", "Height must be 100–250 cm."); return

        mult  = {"light":1.375,"moderate":1.55,"very":1.725}[self.activity_var.get()]
        tdee  = self._bmr(age, weight, height, self.gender_var.get()) * mult
        goal  = self.goal_var.get()
        cals  = tdee + (-500 if goal=="lose" else 300 if goal=="gain" else 0)
        prot, fat, carbs = self._macros(cals, weight, goal)
        bmi, bmi_cat     = self._bmi(weight, height)
        water_ml         = int(weight * 35)

        # Update tiles
        self.t_cal[0].config(text=f"{int(cals):,}")
        self.t_cal[1].config(text="kcal / day")
        self.t_pro[0].config(text=str(prot))
        self.t_pro[1].config(text="g protein")
        self.t_carb[0].config(text=str(carbs))
        self.t_carb[1].config(text="g carbs")
        self.t_fat[0].config(text=str(fat))
        self.t_fat[1].config(text="g fat")
        self.t_bmi[0].config(text=f"{bmi}")
        self.t_bmi[1].config(text=bmi_cat)
        self.t_water[0].config(text=f"{water_ml:,}")
        self.t_water[1].config(text=f"ml · {round(water_ml/240)} glasses")

        tips = {
            "lose":     "Tip — Prioritise protein to preserve muscle while in a deficit.",
            "gain":     "Tip — Eat at consistent intervals; target a calorie surplus around workouts.",
            "maintain": "Tip — Track weekly averages rather than single-day totals for best accuracy.",
        }
        self.tip_lbl.config(text=tips[goal])
        self.tip_lbl.pack(fill="x", pady=(14, 0))
        self.res_card.pack(fill="x")


def main():
    root = tk.Tk()
    app = NutritionCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
