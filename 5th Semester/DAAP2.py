# please run "pip install matplotlib" before running the python file

import random, math, tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def brute_force(points):
    min_d = float('inf')
    closest_pair_points = None
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            d = dist(points[i], points[j])
            if d < min_d:
                min_d = d
                closest_pair_points = (points[i], points[j])
    return min_d, closest_pair_points

def strip_closest(strip, d):
    min_d = d
    closest_pair_points = None
    strip.sort(key=lambda x: x[1])
    for i in range(len(strip)):
        for j in range(i+1, len(strip)):
            if (strip[j][1] - strip[i][1]) >= min_d:
                break
            new_d = dist(strip[i], strip[j])
            if new_d < min_d:
                min_d = new_d
                closest_pair_points = (strip[i], strip[j])
    return min_d, closest_pair_points

def closest_pair(points):
    def recur(Px, Py):
        n = len(Px)
        if n <= 3:
            return brute_force(Px)
        mid = n // 2
        mid_x = Px[mid][0]
        Lx, Rx = Px[:mid], Px[mid:]
        Ly, Ry = [], []
        for p in Py:
            (Ly if p[0] <= mid_x else Ry).append(p)
        d1, p1 = recur(Lx, Ly)
        d2, p2 = recur(Rx, Ry)
        if d1 < d2:
            d, closest = d1, p1
        else:
            d, closest = d2, p2
        strip = [p for p in Py if abs(p[0] - mid_x) < d]
        d_strip, p_strip = strip_closest(strip, d)
        if d_strip < d:
            return d_strip, p_strip
        return d, closest
    Px, Py = sorted(points), sorted(points, key=lambda x: x[1])
    return recur(Px, Py)

def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    half = n // 2
    high1, low1 = divmod(x, 10**half)
    high2, low2 = divmod(y, 10**half)
    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)
    return (z2 * 10**(2*half)) + ((z1 - z2 - z0) * 10**half) + z0

def generate_inputs():
    try:
        for algo in ["points", "integers"]:
            for i in range(1, 11):
                with open(f"{algo}_{i}.txt", "w") as f:
                    n = random.randint(100, 200)
                    if algo == "points":
                        for _ in range(n):
                            f.write(f"{random.randint(0, 10000)} {random.randint(0, 10000)}\n")
                    else:
                        f.write(f"{random.randint(10**50, 10**100)} {random.randint(10**50, 10**100)}\n")
        messagebox.showinfo("Success", "Generated 20 input files successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate files: {str(e)}")

# --- GUI Actions ---
def run_algorithm():
    file_path = filedialog.askopenfilename(
        title="Select Input File", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return
    try:
        with open(file_path) as f:
            lines = f.readlines()
            data = [list(map(int, line.split())) for line in lines if line.strip()]
        if not data:
            messagebox.showerror("Error", "File is empty.")
            return
        text_box.config(state=tk.NORMAL)
        text_box.delete('1.0', tk.END)
        for widget in plot_frame.winfo_children():
            widget.destroy()
        if "points" in file_path:
            display_closest_pair(data, file_path)
        else:
            display_karatsuba(data, file_path)
    except ValueError:
        messagebox.showerror("Error", "Invalid input format in file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_closest_pair(data, file_path):
    output = "ALGORITHM: Closest Pair of Points (Divide & Conquer)\n\n"
    output += f"File: {file_path}\n"
    output += f"Number of Points: {len(data)}\n\n"
    output += "Steps:\n"
    output += " • Divide points into halves\n"
    output += " • Recurse on each half\n"
    output += " • Check strip area\n"
    output += " • Return the minimum distance\n"
    output += " • Time Complexity: O(n log n)\n\n"
    text_box.insert(tk.END, output)
    text_box.update()
    start_time = time.time()
    min_distance, closest_points = closest_pair(data)
    end_time = time.time()
    execution_time = end_time - start_time
    output = f"\nRESULTS:\n"
    output += f" • Minimum Distance: {min_distance:.4f}\n"
    output += f" • Closest Pair: {closest_points}\n"
    output += f" • Execution Time: {execution_time*1000:.4f} ms\n"
    text_box.insert(tk.END, output)
    text_box.config(state=tk.DISABLED)
    plot_closest_pair(data, closest_points)

def display_karatsuba(data, file_path):
    output = "ALGORITHM: Karatsuba Integer Multiplication\n\n"
    output += f"File: {file_path}\n"
    output += f"Numbers:\nX = {data[0][0]}\nY = {data[0][1]}\n\n"
    output += "Steps:\n"
    output += " • Split numbers\n"
    output += " • Compute 3 recursive multiplications\n"
    output += " • Combine results\n"
    output += " • Time Complexity: O(n^1.585)\n\n"
    text_box.insert(tk.END, output)
    text_box.update()
    start_time = time.time()
    result = karatsuba(data[0][0], data[0][1])
    end_time = time.time()
    execution_time = end_time - start_time
    expected = data[0][0] * data[0][1]
    verification = "CORRECT" if result == expected else "INCORRECT"
    output = f"\nRESULTS:\n"
    output += f" • Product: {result}\n"
    output += f" • Verification: {verification}\n"
    output += f" • Execution Time: {execution_time*1000:.4f} ms\n"
    text_box.insert(tk.END, output)
    text_box.config(state=tk.DISABLED)

def plot_closest_pair(data, closest_points):
    fig, ax = plt.subplots(figsize=(6, 5), dpi=80)
    x_coords = [p[0] for p in data]
    y_coords = [p[1] for p in data]
    ax.scatter(x_coords, y_coords, c='#CFE1E0', s=30, alpha=0.8, label='Points')
    ax.scatter([closest_points[0][0], closest_points[1][0]], 
               [closest_points[0][1], closest_points[1][1]], 
               c='#4A707A', s=80, marker='o', label='Closest Pair')
    ax.plot([closest_points[0][0], closest_points[1][0]], 
            [closest_points[0][1], closest_points[1][1]], 
            color='#7CA982', linewidth=2, alpha=0.7)
    ax.set_xlabel('X Coordinate', color='#1D3557')
    ax.set_ylabel('Y Coordinate', color='#1D3557')
    ax.set_title('Closest Pair Visualization', color='#1D3557', fontsize=11, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- GUI Setup ---
root = tk.Tk()
root.title("Divide and Conquer Visualizer")
root.geometry("1000x750")
root.configure(bg="#E9F5F2")

main_frame = tk.Frame(root, bg="#E9F5F2")
main_frame.pack(fill=tk.BOTH, expand=True)

sidebar = tk.Frame(main_frame, bg="#DDEBE8", width=220)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

btn_style = {
    "width": 22,
    "font": ("Segoe UI", 10, "bold"),
    "bd": 1,
    "relief": tk.RIDGE,
    "fg": "#1B263B"
}

tk.Button(sidebar, text="Generate Input Files", command=generate_inputs,
          bg="#BFD7B5", activebackground="#A8C9A1", **btn_style).pack(pady=10)
tk.Button(sidebar, text="Select & Run Algorithm", command=run_algorithm,
          bg="#B3D0D8", activebackground="#9DC2C8", **btn_style).pack(pady=10)

content_frame = tk.Frame(main_frame, bg="#E9F5F2")
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

text_label = tk.Label(content_frame, text="Algorithm Output:", font=("Segoe UI", 10, "bold"), bg="#E9F5F2", fg="#1D3557")
text_label.pack(anchor=tk.W)

text_box = scrolledtext.ScrolledText(content_frame, width=50, height=25,
                                     font=("Consolas", 9), bg="#F9FAFB", fg="#2B2D42",
                                     insertbackground="#2B2D42")
text_box.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 5))

plot_label = tk.Label(content_frame, text="Visualization:", font=("Segoe UI", 10, "bold"), bg="#E9F5F2", fg="#1D3557")
plot_label.pack(anchor=tk.W)

plot_frame = tk.Frame(content_frame, bg="#F9FAFB", relief=tk.RIDGE, bd=2)
plot_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
