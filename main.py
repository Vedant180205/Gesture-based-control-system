# main.py

import cv2
from detection.hand_tracking import HandTracker
from control.mouse_control import MouseController
from utils.smoothing import SmoothFilter


def main():
    cap = cv2.VideoCapture(0)

    # Optional: reduce resolution for stability
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    tracker = HandTracker()
    mouse = MouseController()
    smoother = SmoothFilter(0.35)

    margin = 100  # control area margin

    while True:
        success, frame = cap.read()

        if not success:
            break

        # Fix mirror
        frame = cv2.flip(frame, 1)

        results = tracker.process_frame(frame)
        landmarks = tracker.get_landmarks(frame, results)

        h, w, _ = frame.shape

        # Draw control box (visual feedback)
        cv2.rectangle(
            frame,
            (margin, margin),
            (w - margin, h - margin),
            (255, 0, 255),
            2
        )

        if landmarks:
            hand = landmarks[0]
            _, x, y = hand[8]

            # Clamp inside box
            x = max(margin, min(x, w - margin))
            y = max(margin, min(y, h - margin))

            # Normalize to reduced area
            x = x - margin
            y = y - margin

            reduced_w = w - 2 * margin
            reduced_h = h - 2 * margin

            # Apply smoothing
            x, y = smoother.apply(x, y)

            mouse.move_cursor(x, y, reduced_w, reduced_h)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()