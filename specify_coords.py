import cv2
import numpy as np
import pyautogui


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")


# Specify the title of your game window
game_window_title = "Heartwood Online"

# Get the game window
game_window = pyautogui.getWindowsWithTitle(game_window_title)

if game_window:
    print(f"Found game window: {game_window[0].title}")
    game_window[0].activate()

    # Capture the screenshot of the game window
    screenshot = pyautogui.screenshot(
        region=(game_window[0].left, game_window[0].top, game_window[0].width, game_window[0].height))

    # Convert the screenshot to a NumPy array (OpenCV format)
    screenshot_np = np.array(screenshot)

    # Create a window and set the callback function
    cv2.namedWindow('Select Region')
    cv2.setMouseCallback('Select Region', on_mouse)

    # Display the screenshot
    cv2.imshow('Select Region', screenshot_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Game window not found")
