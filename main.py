# main.py

import cv2
import ctypes
from detection.hand_tracking import HandTracker
from gestures.gesture_logic import detect_gesture
from control.system_control import SystemController

# ── Toggle verbose console output ─────────────────────────────────────────────
DEBUG = False


def make_window_passive(title):
    """Mark the OpenCV window as WS_EX_NOACTIVATE so it never steals focus."""
    GWL_EXSTYLE      = -20
    WS_EX_NOACTIVATE = 0x08000000
    WS_EX_TOPMOST    = 0x00000008

    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd:
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd, GWL_EXSTYLE,
            style | WS_EX_NOACTIVATE | WS_EX_TOPMOST
        )
        print(f"[SETUP] Passive window ready (hwnd={hwnd})")
    else:
        print("[SETUP] WARNING: Could not find gesture window handle")


def main():
    WIN_TITLE = "Gesture Control"

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("[ERROR] Camera not accessible")
        return

    tracker    = HandTracker()
    controller = SystemController()

    # ── Thresholds ─────────────────────────────────────────────────────────────
    HOLD_THRESHOLD        = 12   # frames OPEN/TWO_FINGERS must be held before firing
    FIST_BUFFER_SIZE      = 6    # sliding window length for scroll detection
    FIST_SCROLL_THRESHOLD = 20   # min pixel movement across window to trigger scroll
    SCROLL_COOLDOWN       = 8    # frames to wait between scroll events

    # ── Runtime state ──────────────────────────────────────────────────────────
    prev_gesture  = None
    hold_counter  = 0
    current_label = "No Hand"
    fist_y_buffer = []
    scroll_cd     = 0
    frame_count   = 0
    window_setup  = False

    print("[INFO] Gesture control started. Press ESC in the window to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame      = cv2.flip(frame, 1)
        results    = tracker.process_frame(frame)
        landmarks  = tracker.get_landmarks(frame, results)
        h, w, _    = frame.shape
        frame_count += 1

        if landmarks:
            hand    = landmarks[0]
            gesture = detect_gesture(hand)

            if DEBUG and frame_count % 15 == 0:
                print(f"[DEBUG] gesture={gesture}  hold={hold_counter}  scroll_buf={len(fist_y_buffer)}")

            # ── FIST → sliding-window scroll ───────────────────────────────────
            if gesture == "FIST":
                wrist_y = hand[0][2]
                fist_y_buffer.append(wrist_y)
                if len(fist_y_buffer) > FIST_BUFFER_SIZE:
                    fist_y_buffer.pop(0)

                if scroll_cd > 0:
                    scroll_cd -= 1

                if len(fist_y_buffer) == FIST_BUFFER_SIZE and scroll_cd == 0:
                    net_dy = fist_y_buffer[-1] - fist_y_buffer[0]

                    if net_dy < -FIST_SCROLL_THRESHOLD:
                        print(f"[ACTION] SCROLL UP  (dy={net_dy})")
                        controller.execute("SCROLL_UP")
                        current_label = "SCROLL UP ↑"
                        scroll_cd = SCROLL_COOLDOWN
                        fist_y_buffer.clear()

                    elif net_dy > FIST_SCROLL_THRESHOLD:
                        print(f"[ACTION] SCROLL DOWN  (dy={net_dy})")
                        controller.execute("SCROLL_DOWN")
                        current_label = "SCROLL DOWN ↓"
                        scroll_cd = SCROLL_COOLDOWN
                        fist_y_buffer.clear()

                    else:
                        current_label = f"FIST  dy={net_dy:+d}"
                else:
                    current_label = f"FIST  buf={len(fist_y_buffer)}/{FIST_BUFFER_SIZE}"

                prev_gesture = None
                hold_counter = 0

            # ── OPEN / TWO_FINGERS → hold-timer ───────────────────────────────
            else:
                fist_y_buffer.clear()
                scroll_cd = 0

                if gesture is None:
                    prev_gesture  = None
                    hold_counter  = 0
                    current_label = "---"

                elif gesture != prev_gesture:
                    hold_counter  = 1
                    prev_gesture  = gesture
                    current_label = f"{gesture}  1/{HOLD_THRESHOLD}"

                else:
                    hold_counter += 1
                    current_label = f"{gesture}  {hold_counter}/{HOLD_THRESHOLD}"

                if gesture in ("OPEN", "TWO_FINGERS") and hold_counter == HOLD_THRESHOLD:
                    print(f"[ACTION] Firing {gesture}")
                    controller.execute(gesture)
                    current_label = f">>> {gesture} FIRED!"

        else:
            prev_gesture  = None
            hold_counter  = 0
            fist_y_buffer.clear()
            scroll_cd     = 0
            current_label = "No Hand"
            if DEBUG and frame_count % 30 == 0:
                print("[DEBUG] No hand detected")

        # ── HUD overlay ────────────────────────────────────────────────────────
        cv2.rectangle(frame, (5, h - 55), (420, h - 5), (0, 0, 0), -1)
        cv2.putText(frame, current_label, (10, h - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)

        cv2.imshow(WIN_TITLE, frame)

        # Make window passive on first frame (after HWND is available)
        if not window_setup:
            cv2.waitKey(100)
            make_window_passive(WIN_TITLE)
            window_setup = True

        if cv2.waitKey(1) & 0xFF == 27:   # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()