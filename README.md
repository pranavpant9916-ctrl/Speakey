# 🔊 Speakey

> **Give your keys a voice.** An ultra-low-latency desktop audio utility that provides dynamic acoustic feedback for keystrokes and mouse clicks through your headphones.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey.svg)]()

---

## The Problem
When wearing noise-cancelling headphones or in-ear monitors, you lose tactile acoustic feedback from your keyboard and mouse. Speakey intercepts hardware events globally across your operating system and routes crisp, instant sound effects directly into your headphones.

---

##  Features

* **Ultra-Low Latency:** Uses optimized audio buffer pools (~11ms response time) for zero perceptible lag.
* **4 Unique Sound Packs:**
  * ⌨️ **Typing:** Crisp mechanical switch feedback.
  * 🐱 **Cat:** Cute meows on tap — **hold any key for an angry cat growl!**
  * 🐶 **Dog:** Playful barks on tap — **hold any key for a wolf howl!** 🐺
  * 🐐 **Goat:** Satisfying goat bleats.
* **⏱️ Interactive Long-Press Mechanics:** Holding keys triggers unique secondary sound states using thread-safe state machines.
* **Modern Dark-Mode GUI:** Built with `customtkinter`, featuring:
  * Live master volume slider.
  * Long-press sensitivity tuning (150ms – 800ms).
  * Mouse click toggle.
  * Live keystroke visualizer pill.
* **⌨Global Shortcuts:** Switch soundpacks instantly from any active window:
  * `Cmd + Ctrl + 1` ➔ Typing
  * `Cmd + Ctrl + 2` ➔ Cat
  * `Cmd + Ctrl + 3` ➔ Dog
  * `Cmd + Ctrl + 4` ➔ Goat

---

## Tech Stack & Architecture

* **Event Capture:** `pynput` (macOS `CGEventTap` / Windows `SetWindowsHookEx`)
* **Audio Engine:** `pygame.mixer` (SDL2 audio with 24 pre-allocated polyphonic channels)
* **Frontend UI:** `customtkinter` (Thread-safe Tkinter wrapper)
* **Concurrency:** Python `threading` & `threading.Timer`

---

## Getting Started

### Prerequisites

* Python 3.10+
* On macOS: `python-tk` via Homebrew (`brew install python-tk`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pranavpant9916-ctrl/Speakey.git
   cd Speakey