<div align="center">

```
 ██████╗ ███████╗███████╗████████╗██╗   ██╗██████╗ ███████╗
██╔════╝ ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝
██║  ███╗█████╗  ███████╗   ██║   ██║   ██║██████╔╝█████╗  
██║   ██║██╔══╝  ╚════██║   ██║   ██║   ██║██╔══██╗██╔══╝  
╚██████╔╝███████╗███████║   ██║   ╚██████╔╝██║  ██║███████╗
 ╚═════╝ ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝

     C O N T R O L   S Y S T E M
```

# 🖐️ Gesture-Based Control System

### _Control your computer with nothing but your bare hands. No mouse. No keyboard. Just vibes._

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-red?style=for-the-badge)](https://pyautogui.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

<br/>

> 🧠 **Powered by Google's MediaPipe** | 👁️ **Real-time Computer Vision** | ⚡ **Sub-10ms Response Time**

<br/>

---

</div>

## 🌌 What is This Sorcery?

Imagine Tom Minority Report. Imagine Iron Man's holographic UI. Now imagine that — **but in Python, running on your webcam, right now.**

This project is a **real-time, camera-based gesture recognition system** that maps your hand movements to full cursor control on your screen. Index finger up? That's your mouse. Move it around. The computer follows.

Built with Google's MediaPipe for state-of-the-art hand landmark detection and OpenCV for live video processing — all running **locally on your machine**, no cloud, no latency, no compromise.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ **Air Mouse** | Move your cursor by raising your index finger and moving your hand |
| 🧠 **21-Point Hand Tracking** | Full skeletal landmark detection across all 5 fingers (21 nodes!) |
| 🔮 **Adaptive Smoothing** | Exponential moving average filter with dynamic alpha tuning |
| 🎯 **Dead Zone Engine** | Ignores micro-jitter — only registers intentional movement |
| 📦 **Control Box UI** | Visual on-screen boundary that maps camera space to screen space |
| 🪞 **Mirror Mode** | Webcam is flipped horizontally for natural, intuitive control |
| ⚡ **60 FPS Capable** | Lightweight pipeline — runs fast even on standard laptops |
| 🧩 **Modular Architecture** | Plug-and-play modules for detection, control, gestures, and utils |

---

## 🧬 How It Actually Works

```
   📷 Webcam Feed
        │
        ▼
   ┌─────────────┐
   │  OpenCV     │  ← Captures 640×480 frames at ~60fps
   │  VideoCapture│
   └─────┬───────┘
         │ BGR Frame
         ▼
   ┌─────────────┐
   │  Hand       │  ← Converts BGR→RGB, feeds into MediaPipe
   │  Tracker    │
   └─────┬───────┘
         │ 21 Landmarks (x, y per point)
         ▼
   ┌─────────────┐
   │  Landmark   │  ← Extracts Index Fingertip (point #8)
   │  Extractor  │
   └─────┬───────┘
         │ Raw (x, y) in camera space
         ▼
   ┌─────────────┐
   │  Smooth     │  ← Adaptive EMA filter + dead zone
   │  Filter     │     (alpha=0.35 normal, 0.8 for fast moves)
   └─────┬───────┘
         │ Smoothed (x, y)
         ▼
   ┌─────────────┐
   │  Mouse      │  ← Remaps camera coords → screen coords
   │  Controller │     pyautogui.moveTo(screen_x, screen_y)
   └─────────────┘
         │
         ▼
   🖥️ Your Cursor Moves!
```

---

## 🗂️ Project Structure

```
gesture-control-system/
│
├── 📄 main.py                    ← 🚀 Entry point — the grand orchestrator
│
├── 👁️ detection/
│   └── hand_tracking.py          ← MediaPipe hand landmark engine
│
├── 🖱️ control/
│   └── mouse_control.py          ← Camera-to-screen coordinate mapper
│
├── 🤌 gestures/
│   ├── gesture_logic.py          ← [WIP] Gesture classification logic
│   └── gesture_utils.py          ← [WIP] Gesture helper utilities
│
├── 🔧 utils/
│   └── smoothing.py              ← Adaptive EMA + dead zone filter
│
├── ⚙️ config/
│   └── settings.py               ← [WIP] Configurable system parameters
│
├── 📷 camera/
│   └── camera.py                 ← Camera abstraction layer
│
├── 📋 requirements.txt           ← Python dependencies
├── 🙈 .gitignore                 ← Git ignored files & venv
└── 📖 README.md                  ← You are here
```

---

## 🔬 Under The Hood — Key Technical Details

### 🖐️ Hand Landmark Map (MediaPipe 21-Point Model)

```
                    8   ← INDEX FINGERTIP (used for cursor)
                    |
              7     |
              |   12
         6    | 11  |
         |  4 | |  16
         |  | |10   |  20
    5  3 | 9 |  |  19
    |  | | | | 15  |
    |  2 | | |  |  18
    | |  | | 14   |
    1 |  | |  | 17
    | 0--+-+-13
    |    |
    WRIST (0)
```

> MediaPipe detects **21 key points** per hand. We track **landmark #8** (index fingertip) for cursor movement.

---

### 🔮 The Smoothing Algorithm

The `SmoothFilter` uses a **variable-alpha Exponential Moving Average**:

```python
# Dead zone — ignore micro-jitter below 5px
if abs(dx) < 5 and abs(dy) < 5:
    return prev_position   # Stay put

# Fast movement? Snap quickly (alpha=0.8)
if distance > 50:
    alpha = 0.8

# Slow movement? Smooth heavily (alpha=0.35)
smooth_x = alpha * x + (1 - alpha) * prev_x
```

This means:
- **Tiny trembles** → ignored completely (dead zone)  
- **Slow, precise movements** → heavily smoothed (natural feel)  
- **Fast swipes** → snap responsively (no lag on big moves)

---

### 📦 The Control Box

The system defines a **margin zone** (100px) around the camera frame. Your hand is only tracked **inside** this box, which then gets **remapped** to your full screen resolution.

```
 ┌──────────────────────┐  ← Full 640×480 frame
 │   ╔══════════════╗   │
 │   ║              ║   │  ← Control box (440×280)
 │   ║   MOVE HERE  ║   │    Everything inside = active zone
 │   ║              ║   │
 │   ╚══════════════╝   │
 └──────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.9+**
- A working **webcam**
- A brain (optional, but recommended)

---

### 📦 Installation

**1. Clone the repo**
```bash
git clone https://github.com/Vedant180205/Gesture-based-control-system.git
cd gesture-control-system
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run it**
```bash
python main.py
```

> 🎉 A window titled `"Gesture Control"` will pop up. Raise your **index finger** and move your hand. Your cursor follows.  
> Press **ESC** to exit.

---

## 📋 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `opencv-python` | 4.9.0.80 | Camera capture & frame rendering |
| `mediapipe` | 0.10.9 | Hand landmark detection (21 points) |
| `numpy` | 1.26.4 | Numerical operations |
| `pyautogui` | 0.9.54 | Cursor movement + screen interaction |
| `pynput` | 1.7.6 | Low-level keyboard/mouse input control |

---

## ⚙️ Configuration

You can tune key parameters directly in `main.py`:

```python
# Smoothing sensitivity (0.0 = frozen, 1.0 = no smoothing)
smoother = SmoothFilter(0.35)

# Camera resolution
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Control box margin (pixels from edge)
margin = 100
```

And in `detection/hand_tracking.py`:

```python
HandTracker(
    max_hands=1,           # Track 1 or 2 hands
    detection_conf=0.7,    # Minimum detection confidence
    tracking_conf=0.7      # Minimum tracking confidence
)
```

---

## 🗺️ Roadmap

- [x] ✅ Real-time hand tracking with MediaPipe
- [x] ✅ Index finger cursor movement
- [x] ✅ Adaptive smoothing with dead zone
- [x] ✅ Coordinate remapping (camera → screen)
- [ ] 🔄 Pinch gesture → left click
- [ ] 🔄 Fist gesture → drag mode
- [ ] 🔄 Peace sign → right click
- [ ] 🔄 Scroll support (two-finger swipe)
- [ ] 🔄 Multi-hand detection
- [ ] 🔄 Gesture sequence recognition
- [ ] 🔄 Config UI / settings panel
- [ ] 🔄 System tray integration
- [ ] 🔄 Gesture recording & playback

---

## 🧠 Tech Stack

<div align="center">

| Layer | Tech |  
|---|---|
| Language | Python 3.9+ |
| Computer Vision | OpenCV 4.9 |
| Hand Detection | Google MediaPipe |
| System Control | PyAutoGUI + pynput |
| Math/Utilities | NumPy |

</div>

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/pinch-click`
3. Commit your changes: `git commit -m 'Add pinch-to-click gesture'`
4. Push to the branch: `git push origin feature/pinch-click`
5. Open a pull request 🚀

---

## 📜 License

Distributed under the **MIT License**. Do whatever you want with it. Build something crazy.

---

## 👨‍💻 Author

**Vedant** — building things that shouldn't exist yet.

[![GitHub](https://img.shields.io/badge/GitHub-Vedant180205-black?style=for-the-badge&logo=github)](https://github.com/Vedant180205)

---

<div align="center">

### ⭐ If this project blew your mind, leave a star. It costs nothing and means everything.

```
Your hands are the keyboard.
Your fingers are the mouse.
The future is now, and it's running at 60fps.
```

</div>
