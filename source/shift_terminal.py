import csv
import time
import os
import random
from datetime import datetime
import sys
from collections import Counter

# Enable ANSI colors for Windows terminal support
if sys.platform == "win32":
    os.system("")

# SUPER PATH LOGIC: Stops data appearing on desktop xD
# This finds the EXACT folder where the .exe or .py is sitting
if getattr(sys, 'frozen', False):
    # If the app is running as an .exe (PyInstaller)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # If the app is running as a normal .py script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_NAME = os.path.join(DATA_DIR, "shifts.csv")

OPERATORS = {
    "Connect": "CN-2041",
    "Express": "EX-7781",
    "Metro": "MT-5503",
    "Airlink": "AL-9901",
    "Waterline": "WL-3320"
}

HEADER = [
    "OPERATOR", "DATE", "SHIFT_START", "ROUTE", "TRAIN_MODEL",
    "SERVICE_NUMBER", "PASSENGERS", "ARRIVAL_TIME", "ETA", "DELAY"
]

# Aesthetics
GREEN = "\033[92m"
BLACK = "\033[40m"
RESET = "\033[0m"

def style(text=""):
    print(f"{GREEN}{BLACK}{text}{RESET}")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(GREEN + "\nPress Enter to continue..." + RESET)

def flicker():
    for _ in range(3):
        print("\033[2m", end="", flush=True)
        time.sleep(random.uniform(0.03, 0.08))
        print("\033[22m", end="", flush=True)
        time.sleep(random.uniform(0.03, 0.08))

def calculate_delay(arrival, eta):
    fmt = "%H:%M:%S"
    try:
        a = datetime.strptime(arrival, fmt)
        e = datetime.strptime(eta, fmt)
        diff = (a - e).total_seconds() / 60
        return "on time" if diff <= 0 else f"{int(diff)} min delay"
    except ValueError:
        return "N/A"

def init_file():
    # This specifically creates the 'data' folder in the BASE_DIR
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            csv.writer(f).writerow(HEADER)

def load_all_rows():
    init_file()
    try:
        with open(FILE_NAME, "r", newline="") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return [HEADER]

def save_all_rows(rows):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        
#Boot up sequence
def boot():
    clear()
    style("╔══════════════════════╗")
    style("║   SCR TERMINAL v1.5  ║")
    style("║ SHIFT CONTROL SYSTEM ║")
    style("╚══════════════════════╝\n")
    flicker()
    style("BOOTING SYSTEM...")
    time.sleep(0.8)
    style("LOADING OPERATOR MODULES...")
    time.sleep(0.8)
    style("ACCESS RESTRICTED\n")
    time.sleep(0.5)

def choose_operator():
    style("AVAILABLE OPERATORS:\n")
    ops = list(OPERATORS.keys())
    for i, op in enumerate(ops, 1):
        style(f"{i}) {op}")
    style("")
    choice = input(GREEN + "Select operator: " + RESET)
    try:
        return ops[int(choice) - 1]
    except:
        return None

def login():
    for _ in range(3):
        op = choose_operator()
        if not op:
            style("INVALID SELECTION.\n")
            continue
        code = input(GREEN + f"ENTER CODE FOR {op}: " + RESET)
        if OPERATORS[op] == code:
            style(f"\nACCESS GRANTED — {op} OPERATOR\n")
            flicker()
            time.sleep(0.5)
            return op
        else:
            style("INVALID CODE\n")
            flicker()
    style("ACCESS DENIED")
    return None

def add_shift(operator):
    clear()
    flicker()
    style("=== REGISTER NEW SHIFT ===\n")
    today = datetime.now().strftime("%d.%m.%Y")
    date = input(f"Date (DD.MM.YYYY) [Enter = {today}]: ").strip() or today
    start = input(GREEN + "Shift start (HH:MM:SS): " + RESET)
    route = input(GREEN + "Route: " + RESET)
    model = input(GREEN + "Train model: " + RESET)
    service = input(GREEN + "Service number: " + RESET)
    passengers = str(random.randint(20, 120))
    style(f"Passengers: {passengers}")
    eta = input(GREEN + "ETA (HH:MM:SS): " + RESET)
    arrival = input(GREEN + "Arrival time (HH:MM:SS): " + RESET)
    delay = calculate_delay(arrival, eta)
    with open(FILE_NAME, "a", newline="") as f:
        csv.writer(f).writerow([operator, date, start, route, model, service, passengers, arrival, eta, delay])
    style("\nSHIFT SAVED.")
    flicker()
    pause()

def view_shifts(operator):
    clear()
    flicker()
    style(f"=== SHIFT LOG — {operator} ===\n")
    rows = load_all_rows()
    if len(rows) <= 1:
        style("NO DATA FOUND.")
    else:
        style(" | ".join(HEADER))
        style("-" * 110)
        for row in rows[1:]:
            if row[0] == operator:
                style(" | ".join(row))
    pause()

def edit_shift(operator):
    clear()
    flicker()
    style("=== EDIT SHIFT ===\n")
    all_rows = load_all_rows()
    user_shifts = [(i, r) for i, r in enumerate(all_rows) if r[0] == operator]
    if not user_shifts:
        style("NO SHIFTS TO EDIT.")
        pause(); return
    for i, (idx, row) in enumerate(user_shifts, 1):
        style(f"{i}) {row[1]} | {row[3]} | {row[9]}")
    choice = input(GREEN + "\nSelect shift number to edit: " + RESET)
    try:
        selection_idx = int(choice) - 1
        orig_idx, target_row = user_shifts[selection_idx]
        new_row = list(target_row)
        for i, field in enumerate(HEADER):
            if field == "OPERATOR": continue
            val = input(f"{field} [{target_row[i]}]: ").strip()
            if val: new_row[i] = val
        new_row[9] = calculate_delay(new_row[7], new_row[8])
        all_rows[orig_idx] = new_row
        save_all_rows(all_rows)
        style("\nSHIFT UPDATED.")
    except:
        style("INVALID SELECTION.")
    pause()

def delete_shift(operator):
    clear()
    flicker()
    style("=== DELETE SHIFT ===\n")
    all_rows = load_all_rows()
    user_shifts = [(i, r) for i, r in enumerate(all_rows) if r[0] == operator]
    if not user_shifts:
        style("NO SHIFTS TO DELETE.")
        pause(); return
    for i, (idx, row) in enumerate(user_shifts, 1):
        style(f"{i}) {row[1]} | {row[3]} | {row[9]}")
    choice = input(GREEN + "\nSelect shift number to delete: " + RESET)
    try:
        selection_idx = int(choice) - 1
        orig_idx, target_row = user_shifts[selection_idx]
        confirm = input(GREEN + "TYPE 'YES' TO CONFIRM DELETE: " + RESET)
        if confirm == "YES":
            all_rows.pop(orig_idx)
            save_all_rows(all_rows)
            style("\nSHIFT DELETED.")
        else:
            style("CANCELLED.")
    except:
        style("INVALID SELECTION.")
    pause()

def stats_screen(operator):
    clear()
    flicker()
    style(f"=== OPERATOR STATS — {operator} ===\n")
    rows = load_all_rows()
    delays, routes, total = [], [], 0
    for row in rows[1:]:
        if row[0] == operator:
            total += 1
            routes.append(row[3])
            if "min delay" in row[9]:
                delays.append(int(row[9].split()[0]))
    avg = sum(delays) // len(delays) if delays else 0
    maxd = max(delays) if delays else 0
    common_route = Counter(routes).most_common(1)[0][0] if routes else "N/A"
    style(f"Total shifts logged: {total}")
    style(f"Average delay time:  {avg} min")
    style(f"Maximum delay recorded: {maxd} min")
    style(f"Most frequent route: {common_route}")
    pause()
    
#Operator menu
def menu(operator):
    while True:
        clear()
        flicker()
        rows = load_all_rows()
        today = datetime.now().strftime("%d.%m.%Y")
        count = sum(1 for r in rows[1:] if r[0] == operator and r[1] == today)
        style(f"TODAY {today} — Shifts Completed: {count}")
        style(f"""
==============================
  SCR SHIFT TERMINAL v1.5
  OPERATOR: {operator}
==============================
1) Register new shift
2) View shift log
3) Edit a shift
4) Delete a shift
5) Operator stats
6) Exit
==============================
""")
        choice = input(GREEN + "Select option: " + RESET)
        if choice == "1": add_shift(operator)
        elif choice == "2": view_shifts(operator)
        elif choice == "3": edit_shift(operator)
        elif choice == "4": delete_shift(operator)
        elif choice == "5": stats_screen(operator)
        elif choice == "6": break
        else: pause()

if __name__ == "__main__":
    init_file()
    boot()
    op = login()
    if op:
        menu(op)

