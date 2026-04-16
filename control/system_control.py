# control/system_control.py

import pyautogui

pyautogui.FAILSAFE = False


class SystemController:
    def execute(self, action):
        if action == "OPEN":
            # Open palm held → new tab
            pyautogui.hotkey('ctrl', 't')

        elif action == "TWO_FINGERS":
            # Peace sign held → close tab
            pyautogui.hotkey('ctrl', 'w')

        elif action == "SCROLL_UP":
            # Fist moved up → scroll up
            pyautogui.scroll(4)

        elif action == "SCROLL_DOWN":
            # Fist moved down → scroll down
            pyautogui.scroll(-4)