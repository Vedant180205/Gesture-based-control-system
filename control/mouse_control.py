# control/system_control.py
import pyautogui


class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def move_cursor(self, x, y, frame_width, frame_height):
        # Convert camera coords → screen coords
        screen_x = int((x / frame_width) * self.screen_width)
        screen_y = int((y / frame_height) * self.screen_height)

        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.FAILSAFE = False