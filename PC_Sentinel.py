# Scripted by @Emir Karadağ [2025-2026]
# GitHub: @Scriptionz [https://github.com/Scriptionz] 
# LinkedIn: @Emir Karadağ [https://www.linkedin.com/in/emir-karadağ-617a013a2/]

# !! Licensed under the MIT License. !!

# {LATEST} v1.0.1 - Modular Delta Edition - 9 January 2026
# {OLD} v1.0.0 - System Sentinel Core - 9 January 2026

# ----------------- SYSTEM ARCHITECTURE (HOW IT WORKS) ----------------- #
# 1. HARDWARE INTERFACE: 
#    Uses 'psutil' to communicate with Windows/Linux kernel to fetch 
#    CPU, RAM, and Battery metrics.
#
# 2. TREND TRACKING: 
#    Stores the last measurement to show real-time increase/decrease.
#
# 3. MODULAR CONFIG: 
#    All system limits and UI toggles are managed from a single block.
# ----------------------------------------------------------------------- #

import os
import sys
import time
import subprocess

def install_dependencies():
    """Checks and installs required libraries for system monitoring."""
    required = {'psutil', 'colorama', 'plyer'}
    try:
        import psutil
        from colorama import Fore, Style, init
        from plyer import notification
    except ImportError:
        print("SENTINEL: Installing core telemetry modules...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
        os.execl(sys.executable, sys.executable, *sys.argv)

install_dependencies()

import psutil
from colorama import Fore, Style, init
from plyer import notification

# Initialize Colorama for Windows terminal
init(autoreset=True)

# --------------- MODULAR CONFIGURATION ----------------- #

SETTINGS = {
    "show_delta": True,           # Show increase/decrease (+/-)
    "enable_notifications": True,  # Critical alerts
    "update_interval": 1,         # Refresh rate
}

THRESHOLDS = {
    "cpu_danger": 85.0,
    "ram_danger": 90.0,
    "battery_low": 20
}

# Trend History
history = {"cpu": 0.0, "ram": 0.0}

# --------------- CORE ENGINE ----------------- #

def clear_screen():
    """Clears terminal and prevents stacking."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_status_color(value, limit):
    """Returns color based on usage intensity."""
    if value < limit * 0.6: return Fore.GREEN
    if value < limit: return Fore.YELLOW
    return Fore.RED

def get_trend_str(current, previous):
    """Calculates the difference from the last second."""
    diff = current - previous
    if diff > 0.1: return f"{Fore.RED}▲ +{diff:.1f}%"
    if diff < -0.1: return f"{Fore.GREEN}▼ {diff:.1f}%"
    return f"{Fore.WHITE}•  0.0%"

def send_alert(title, message):
    if SETTINGS["enable_notifications"]:
        notification.notify(
            title=f"⚠️ SYSTEM ALERT: {title}",
            message=message,
            app_name="System Sentinel",
            timeout=5
        )

print(f"{Fore.CYAN}System Sentinel v1.0.1")
time.sleep(2)

try:
    while True:
        # --- Data Acquisition ---
        cpu_usage = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        disk = psutil.disk_usage('/')

        # --- Dashboard UI ---
        clear_screen()
        print(f"{Fore.BLUE}="*45)
        print(f"{Fore.WHITE}   System Sentinel - Live Telemetry Dashboard")
        print(f"{Fore.BLUE}="*45)

        # CPU Section
        cpu_color = get_status_color(cpu_usage, THRESHOLDS["cpu_danger"])
        cpu_trend = get_trend_str(cpu_usage, history["cpu"]) if SETTINGS["show_delta"] else ""
        print(f" CPU USAGE:   {cpu_color}[{cpu_usage}%] {cpu_trend}")
        
        # RAM Section
        ram_color = get_status_color(ram.percent, THRESHOLDS["ram_danger"])
        ram_trend = get_trend_str(ram.percent, history["ram"]) if SETTINGS["show_delta"] else ""
        print(f" RAM USAGE:   {ram_color}[{ram.percent}%] {ram_trend} ({ram.used // (1024**2)}MB)")

        # Disk Section
        print(f" DISK SPACE:  {Fore.CYAN}[{disk.percent}%] Free: {disk.free // (1024**3)}GB")

        # Battery Section
        if battery:
            bat_color = Fore.GREEN if battery.percent > THRESHOLDS["battery_low"] else Fore.RED
            status = "Charging" if battery.power_plugged else "Discharging"
            print(f" BATTERY:    {bat_color}[{battery.percent}%] Status: {status}")

        print(f"{Fore.BLUE}="*45)
        print(f"{Fore.WHITE} Status: MONITORING | CTRL+C to stop.")

        # --- Logic: Trend Update & Alerts ---
        history["cpu"] = cpu_usage
        history["ram"] = ram.percent

        if cpu_usage > THRESHOLDS["cpu_danger"]:
            send_alert("HIGH CPU USAGE", f"CPU is at {cpu_usage}%!")
        
        if ram.percent > THRESHOLDS["ram_danger"]:
            send_alert("LOW MEMORY", "System RAM is almost full!")

        time.sleep(SETTINGS["update_interval"])

except KeyboardInterrupt:
    print(f"\n{Fore.YELLOW}SENTINEL: Shield deactivated. System safe.")
    sys.exit()
