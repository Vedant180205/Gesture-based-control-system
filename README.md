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

# 🖐️ Gesture-Based Browser Control System

### _Open tabs. Close tabs. Scroll pages. No mouse. No keyboard. Just hands._

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-red?style=for-the-badge)](https://pyautogui.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](.)

<br/>

> 🧠 **Powered by Google's MediaPipe** | 👁️ **Real-time Computer Vision** | ⚡ **Focus-Safe Overlay Window**

<br/>

---

</div>

## 🌌 What is This?

A **real-time, webcam-based gesture control system** that maps hand shapes to browser (or any app) actions.

- Hold an **Open Palm** → opens a new tab (`Ctrl+T`)
- Hold a **Peace Sign** → closes the current tab (`Ctrl+W`)
- Move a **Fist** up or down → scrolls the page

The overlay window is rendered **passively** — it sits on top without ever stealing focus from your browser. Chrome stays active the entire time.

Built on Google's MediaPipe for 21-point hand landmark detection and OpenCV for live video — running **100% locally**, no cloud, no latency.

---

## ✨ Gestures

| Gesture | Action | How it triggers |
|---|---|---|
| 🖐️ **Open Palm** | New Tab (`Ctrl+T`) | Hold for 12 frames (~0.4s) |
| ✌️ **Peace Sign** | Close Tab (`Ctrl+W`) | Hold for 12 frames (~0.4s) |
| ✊ **Fist — Move Up** | Scroll Up | Wrist moves ≥20px upward in a 6-frame window |
| ✊ **Fist — Move Down** | Scroll Down | Wrist moves ≥20px downward in a 6-frame window |

> **Hold-timer prevents accidental triggers.** Transitional or ambiguous hand shapes are ignored entirely.

---

## 🧬 How It Works

```
📷 Webcam Feed (640×480)
       │
       ▼
┌──────────────┐
│  HandTracker │  ← MediaPipe: detects 21 landmarks per hand
└──────┬───────┘
       │ 21 (id, x, y) points
       ▼
┌──────────────┐
│ detect_      │  ← Classifies shape: OPEN / TWO_FINGERS / FIST / None
│ gesture()    │
└──────┬───────┘
       │ gesture label
       ▼
┌──────────────────────────────────┐
│           main.py loop           │
│                                  │
│  FIST  → sliding-window scroll   │  ← 6-frame Y buffer, cooldown guard
│  OTHER → hold-timer gate         │  ← must hold 12 frames to fire
└──────┬───────────────────────────┘
       │ confirmed action
       ▼
┌──────────────┐
│ SystemCtrl   │  ← pyautogui: Ctrl+T / Ctrl+W / scroll()
└──────────────┘
       │
       ▼
🌐 Browser responds
```

---

## 🗂️ Project Structure

```
gesture-control-system/
│
├── 📄 main.py                    ← Entry point & main loop
│
├── 👁️ detection/
│   └── hand_tracking.py          ← MediaPipe wrapper (process + landmark extraction)
│
├── 🤌 gestures/
│   └── gesture_logic.py          ← OPEN / TWO_FINGERS / FIST classifier
│
├── 🖱️ control/
│   └── system_control.py         ← pyautogui action executor
│
├── 📋 requirements.txt
├── 🙈 .gitignore
└── 📖 README.md
```

---

## 🔬 Technical Details

### 🖐️ Gesture Classification (`gesture_logic.py`)

Each finger is classified as **extended** if its tip is farther from the wrist than its PIP knuckle:

```python
def is_finger_extended(hand, tip_id, pip_id):
    wrist = hand[0][1:]
    tip   = hand[tip_id][1:]
    pip   = hand[pip_id][1:]
    return distance(tip, wrist) > distance(pip, wrist)
```

| Condition | Gesture |
|---|---|
| All 4 fingers extended | `OPEN` |
| 0 fingers extended | `FIST` |
| Index + Middle extended (but not all 4) | `TWO_FINGERS` |
| Anything else | `None` (transitional — ignored) |

---

### ⏱️ Hold-Timer (for OPEN / TWO_FINGERS)

Actions only fire after a gesture is held **continuously for 12 frames** (~0.4 seconds at 30fps). This eliminates false triggers from brief hand shape transitions.

```
Frame:     1   2   3  ...  12
Gesture:  OPEN OPEN OPEN ... OPEN  ← fires Ctrl+T on frame 12
              ↑ resets on any change
```

---

### 📊 Sliding-Window Scroll (for FIST)

Scroll is detected by tracking the wrist Y position over a 6-frame buffer:

```
buffer = [y0, y1, y2, y3, y4, y5]
net_dy = buffer[-1] - buffer[0]

if net_dy < -20 → SCROLL UP
if net_dy > +20 → SCROLL DOWN
```

An 8-frame cooldown prevents repeat-firing on a single movement.

---

### 🪟 Passive Window (no focus steal)

The preview window is marked `WS_EX_NOACTIVATE | WS_EX_TOPMOST` via the Windows API:

```python
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
    style | WS_EX_NOACTIVATE | WS_EX_TOPMOST)
```

The gesture window floats on top, but **Chrome (or any target app) retains keyboard focus** at all times.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.9+**
- A working **webcam**

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Vedant180205/Gesture-based-control-system.git
cd gesture-control-system

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

> A window titled **`Gesture Control`** will appear in the corner.  
> Keep your browser open behind it and use gestures.  
> Press **ESC** in the gesture window to quit.

---

## ⚙️ Configuration

All tunable values are at the top of `main.py`:

```python
DEBUG = False               # Set True to print per-frame gesture state

HOLD_THRESHOLD        = 12  # Frames to hold OPEN/TWO_FINGERS before firing
FIST_BUFFER_SIZE      = 6   # Sliding window size for scroll detection
FIST_SCROLL_THRESHOLD = 20  # Min pixel movement (across window) to scroll
SCROLL_COOLDOWN       = 8   # Frames between scroll events
```

Detection sensitivity can be tuned in `detection/hand_tracking.py`:

```python
HandTracker(
    max_hands=1,
    detection_conf=0.7,   # Lower = more permissive detection
    tracking_conf=0.7     # Lower = more permissive tracking
)
```

---

## 📋 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `opencv-python` | 4.9.0.80 | Camera capture & frame rendering |
| `mediapipe` | 0.10.9 | 21-point hand landmark detection |
| `numpy` | 1.26.4 | Array operations |
| `pyautogui` | 0.9.54 | Keyboard shortcuts & scroll |
| `pynput` | 1.7.6 | Low-level input (available for extension) |

---

## 🗺️ Roadmap

- [x] ✅ Real-time hand tracking (MediaPipe)
- [x] ✅ OPEN → new tab (`Ctrl+T`)
- [x] ✅ TWO_FINGERS → close tab (`Ctrl+W`)
- [x] ✅ FIST → scroll up / down (sliding window)
- [x] ✅ Hold-timer to prevent accidental triggers
- [x] ✅ Passive overlay window (no focus steal)
- [x] ✅ Debug toggle flag
- [ ] 🔄 Configurable gesture → action mappings
- [ ] 🔄 Tab switching gesture (swipe left/right)
- [ ] 🔄 System tray icon & hotkey to pause/resume
- [ ] 🔄 macOS / Linux support

---

## 🤝 Contributing

PRs welcome. For major changes open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m 'Add your-idea'`
4. Push: `git push origin feature/your-idea`
5. Open a pull request 🚀

---

## 📜 License

MIT — build whatever you want with it.

---

## 👨‍💻 Author

**Vedant** — building things that shouldn't exist yet.

[![GitHub](https://img.shields.io/badge/GitHub-Vedant180205-black?style=for-the-badge&logo=github)](https://github.com/Vedant180205)

---

<div align="center">

```
Your hands are the interface.
The camera is the keyboard.
The future is running at 30fps.
```

</div>
