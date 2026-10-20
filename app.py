import os
import threading
import pygame
import customtkinter as ctk
from pynput import keyboard, mouse

# ----------------- AUDIO ENGINE SETUP -----------------
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.mixer.set_num_channels(24)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sound") if os.path.isdir(os.path.join(BASE_DIR, "sound")) else os.path.join(BASE_DIR, "sounds")

def load_sound(filename):
    path = os.path.join(SOUND_DIR, filename)
    if os.path.exists(path):
        s = pygame.mixer.Sound(path)
        s.set_volume(0.8)
        return s
    else:
        print(f"⚠️ Warning: {filename} not found in {SOUND_DIR}")
        return None

sounds = {
    "typing": load_sound("typing.wav"),
    "cat": load_sound("meow.wav"),
    "cat_long": load_sound("angry.wav"),
    "dog": load_sound("Bark.wav"),
    "dog_long": load_sound("howl.wav"),
    "goat": load_sound("Goat.wav"),
}

SOUND_PACKS = {
    "1": {"id": "1", "name": "⌨️ Typing", "tap": "typing", "long": None},
    "2": {"id": "2", "name": "🐱 Cat", "tap": "cat", "long": "cat_long"},
    "3": {"id": "3", "name": "🐶 Dog", "tap": "dog", "long": "dog_long"},
    "4": {"id": "4", "name": "🐐 Goat", "tap": "goat", "long": None},
}

# ----------------- APP STATE -----------------
current_pack_id = "1"
current_volume = 0.8
long_press_threshold = 0.35  # seconds
enable_mouse_clicks = True
active_modifiers = set()
held_keys = {}

def update_master_volume(val):
    global current_volume
    current_volume = float(val)
    for s in sounds.values():
        if s:
            s.set_volume(current_volume)

def trigger_long_press(key_id):
    pack = SOUND_PACKS[current_pack_id]
    long_key = pack["long"]
    if long_key and sounds[long_key]:
        sounds[long_key].play()
        if key_id in held_keys:
            held_keys[key_id]['long_triggered'] = True

def get_key_id(key):
    try:
        return key.char if key.char is not None else str(key)
    except AttributeError:
        return str(key)

# ----------------- FRONT-END GUI (CustomTkinter) -----------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Speakey 🔊")
app.geometry("480x520")
app.resizable(False, False)

# Title & Status Header
header_frame = ctk.CTkFrame(app, corner_radius=12)
header_frame.pack(fill="x", padx=20, pady=(20, 10))

title_label = ctk.CTkLabel(header_frame, text="Speakey", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(side="left", padx=20, pady=12)

status_badge = ctk.CTkLabel(header_frame, text="● ACTIVE", text_color="#2ECC71", font=ctk.CTkFont(size=12, weight="bold"))
status_badge.pack(side="right", padx=20, pady=12)

# Soundpack Selection
pack_label = ctk.CTkLabel(app, text="SELECT SOUND PACK", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray")
pack_label.pack(anchor="w", padx=25, pady=(10, 5))

def on_pack_selected(choice):
    global current_pack_id
    for pid, pdata in SOUND_PACKS.items():
        if pdata["name"] == choice:
            current_pack_id = pid
            tap_sound = sounds[pdata["tap"]]
            if tap_sound:
                tap_sound.play()
            break

pack_options = [p["name"] for p in SOUND_PACKS.values()]
pack_segment = ctk.CTkSegmentedButton(app, values=pack_options, command=on_pack_selected, height=38, font=ctk.CTkFont(size=14))
pack_segment.set(SOUND_PACKS["1"]["name"])
pack_segment.pack(fill="x", padx=20, pady=(0, 15))

# Controls Frame (Sliders & Toggles)
controls_frame = ctk.CTkFrame(app, corner_radius=12)
controls_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Volume Slider
vol_header = ctk.CTkFrame(controls_frame, fg_color="transparent")
vol_header.pack(fill="x", padx=15, pady=(15, 0))
ctk.CTkLabel(vol_header, text="Volume", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
vol_val_label = ctk.CTkLabel(vol_header, text="80%", font=ctk.CTkFont(size=12), text_color="gray")
vol_val_label.pack(side="right")

def on_volume_slider(val):
    vol_val_label.configure(text=f"{int(val * 100)}%")
    update_master_volume(val)

vol_slider = ctk.CTkSlider(controls_frame, from_=0.0, to=1.0, command=on_volume_slider)
vol_slider.set(0.8)
vol_slider.pack(fill="x", padx=15, pady=(5, 15))

# Long-Press Sensitivity Slider
hold_header = ctk.CTkFrame(controls_frame, fg_color="transparent")
hold_header.pack(fill="x", padx=15, pady=(5, 0))
ctk.CTkLabel(hold_header, text="Long-Press Sensitivity", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
hold_val_label = ctk.CTkLabel(hold_header, text="350 ms", font=ctk.CTkFont(size=12), text_color="gray")
hold_val_label.pack(side="right")

def on_hold_slider(val):
    global long_press_threshold
    long_press_threshold = round(val, 2)
    hold_val_label.configure(text=f"{int(long_press_threshold * 1000)} ms")

hold_slider = ctk.CTkSlider(controls_frame, from_=0.15, to=0.8, command=on_hold_slider)
hold_slider.set(0.35)
hold_slider.pack(fill="x", padx=15, pady=(5, 15))

# Mouse Click Toggle Switch
def on_mouse_toggle():
    global enable_mouse_clicks
    enable_mouse_clicks = mouse_switch.get()

mouse_switch = ctk.CTkSwitch(controls_frame, text="Enable Mouse Click Sounds", command=on_mouse_toggle, font=ctk.CTkFont(size=13))
mouse_switch.select()
mouse_switch.pack(anchor="w", padx=15, pady=(10, 10))

# Live Key Indicator
footer_frame = ctk.CTkFrame(app, corner_radius=10, fg_color="#1E1E1E")
footer_frame.pack(fill="x", padx=20, pady=(5, 20))

ctk.CTkLabel(footer_frame, text="Last Key: ", font=ctk.CTkFont(size=12), text_color="gray").pack(side="left", padx=(15, 5), pady=10)
live_key_badge = ctk.CTkLabel(footer_frame, text="None", font=ctk.CTkFont(size=13, weight="bold"), text_color="#3498DB")
live_key_badge.pack(side="left", pady=10)

def update_live_key_ui(key_name):
    # Safely schedule GUI text update onto the main Tkinter thread
    app.after(0, lambda: live_key_badge.configure(text=key_name))

def sync_pack_ui(pack_id):
    app.after(0, lambda: pack_segment.set(SOUND_PACKS[pack_id]["name"]))

# ----------------- BACKGROUND LISTENERS -----------------
def on_press(key):
    global current_pack_id
    key_id = get_key_id(key)
    update_live_key_ui(str(key_id).replace("Key.", ""))

    # Track Cmd / Ctrl
    if key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
        active_modifiers.add('cmd')
        return
    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        active_modifiers.add('ctrl')
        return

    # Check for shortcut: Cmd + Ctrl + [1-4]
    if 'cmd' in active_modifiers and 'ctrl' in active_modifiers:
        if str(key_id) in SOUND_PACKS:
            current_pack_id = str(key_id)
            sync_pack_ui(current_pack_id)
            tap_sound = sounds[SOUND_PACKS[current_pack_id]["tap"]]
            if tap_sound:
                tap_sound.play()
            return

    # Ignore OS repeat if key is already held
    if key_id in held_keys:
        return

    # 1. Play immediate tap sound
    pack = SOUND_PACKS[current_pack_id]
    tap_sound = sounds[pack["tap"]]
    if tap_sound:
        tap_sound.play()

    # 2. Start long-press timer if pack supports it
    if pack["long"]:
        timer = threading.Timer(long_press_threshold, trigger_long_press, args=[key_id])
        timer.daemon = True
        timer.start()
        held_keys[key_id] = {'timer': timer, 'long_triggered': False}
    else:
        held_keys[key_id] = {'timer': None, 'long_triggered': False}

def on_release(key):
    key_id = get_key_id(key)
    if key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
        active_modifiers.discard('cmd')
    elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        active_modifiers.discard('ctrl')

    if key_id in held_keys:
        timer_info = held_keys.pop(key_id)
        if timer_info['timer'] and not timer_info['long_triggered']:
            timer_info['timer'].cancel()

def on_click(x, y, button, pressed):
    if pressed and enable_mouse_clicks:
        update_live_key_ui("Mouse Click")
        pack = SOUND_PACKS[current_pack_id]
        tap_sound = sounds[pack["tap"]]
        if tap_sound:
            tap_sound.play()

# Start background listeners
key_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
key_listener.daemon = True
key_listener.start()

mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.daemon = True
mouse_listener.start()

def on_close():
    key_listener.stop()
    mouse_listener.stop()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()