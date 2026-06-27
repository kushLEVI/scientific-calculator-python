import tkinter as tk
import math
import re

# ---------------- SETTINGS ---------------- #
mode = "DEG"

# ---------------- FUNCTIONS ---------------- #
def insert(value):
    entry.insert(tk.END, value)

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def toggle_mode():
    global mode
    mode = "RAD" if mode == "DEG" else "DEG"
    mode_btn.config(text=mode)

# ✅ Proper trig handling (fixes your error)
def fix_trig(expr):
    if mode == "DEG":
        expr = re.sub(r"sin\((.*?)\)", r"math.sin(math.radians(\1))", expr)
        expr = re.sub(r"cos\((.*?)\)", r"math.cos(math.radians(\1))", expr)
        expr = re.sub(r"tan\((.*?)\)", r"math.tan(math.radians(\1))", expr)
    else:
        expr = re.sub(r"sin\((.*?)\)", r"math.sin(\1)", expr)
        expr = re.sub(r"cos\((.*?)\)", r"math.cos(\1)", expr)
        expr = re.sub(r"tan\((.*?)\)", r"math.tan(\1)", expr)
    return expr

def evaluate(expr):
    try:
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('e', str(math.e))
        expr = expr.replace('^', '**')

        expr = fix_trig(expr)

        expr = re.sub(r"√\((.*?)\)", r"math.sqrt(\1)", expr)
        expr = re.sub(r"log\((.*?)\)", r"math.log10(\1)", expr)
        expr = re.sub(r"ln\((.*?)\)", r"math.log(\1)", expr)

        result = eval(expr)
        return result

    except:
        return "Error"

def calculate():
    result = evaluate(entry.get())
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(result))

# ---------------- KEYBOARD SUPPORT ---------------- #
def key_handler(event):
    key = event.char

    if key in "0123456789+-*/().":
        insert(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        backspace()

# ---------------- UI ---------------- #
root = tk.Tk()
root.title("scietific calculator 🧮")  # as requested
root.geometry("420x650")
root.configure(bg="#2b2b2b")

for i in range(8):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

entry = tk.Entry(root, font=("Consolas", 22),
                 bg="#1c1c1c", fg="#00ff9c",
                 bd=0, justify="right")
entry.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

# Mode + Delete
mode_btn = tk.Button(root, text=mode, command=toggle_mode,
                     bg="#ff9500", fg="white")
mode_btn.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

del_btn = tk.Button(root, text="DEL", command=backspace,
                    bg="#607d8b", fg="white")
del_btn.grid(row=1, column=2, columnspan=3, sticky="nsew", padx=5, pady=5)

# ---------------- BUTTON CREATOR ---------------- #
def btn(text, r, c):
    if text == "=":
        cmd = calculate
        color = "#4CAF50"
    elif text == "C":
        cmd = clear
        color = "#f44336"
    elif text == "x²":
        cmd = lambda: insert("**2")
        color = "#3c3f41"
    elif text == "xʸ":
        cmd = lambda: insert("**")
        color = "#3c3f41"
    else:
        cmd = lambda: insert(text)
        color = "#3c3f41"

    tk.Button(root, text=text, command=cmd,
              font=("Segoe UI", 13),
              bg=color, fg="white", bd=0)\
        .grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

# ---------------- LAYOUT ---------------- #
layout = [
    ['7','8','9','/','C'],
    ['4','5','6','*','('],
    ['1','2','3','-',
')'],
    ['0','.','=','+','^'],
    ['sin(','cos(','tan(','√(','π'],
    ['log(','ln(','e','x²','xʸ']
]

for r, row in enumerate(layout, start=2):
    for c, val in enumerate(row):
        btn(val, r, c)

# Bind keyboard
root.bind("<Key>", key_handler)

root.mainloop()