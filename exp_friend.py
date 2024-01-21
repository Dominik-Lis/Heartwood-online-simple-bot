import time
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui

print("expFriend by Domo started")

# Global variables to track if the player has been attacked recently and last attack time
were_attacked = False
last_attack_time = time.time()

# Global variables to track the last time each healing ability was used
last_heal_1_time = 0
last_heal_2_time = 0
last_heal_3_time = 0


# Function to calculate health percentage based on average color
def calculate_health_percentage(average_color, full_health, critical_health):
    percentage_health = 100 - (np.linalg.norm(np.array(full_health) - np.array(average_color)) / np.linalg.norm(
        np.array(full_health) - np.array(critical_health)) * 100)
    return max(0, min(100, percentage_health))


# Function to handle healing based on cooldowns
def handle_healing():
    global last_heal_1_time, last_heal_2_time, last_heal_3_time

    current_time = time.time()

    # Check if "3" can be used
    if current_time - last_heal_3_time > 11.3:
        pyautogui.press("3")
        last_heal_3_time = current_time
        return

    # Check if "1" can be used
    if current_time - last_heal_1_time > 11.3:
        pyautogui.press("1")
        last_heal_1_time = current_time
        return

    # Check if "2" can be used (after "1" has been used)
    if current_time - last_heal_1_time < 11.3 < current_time - last_heal_2_time:
        pyautogui.press("2")
        last_heal_2_time = current_time


# Function to detect the health bar and perform key presses
def detect_health_bar(image, previous_health):
    global were_attacked, last_attack_time

    frame = np.array(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    x1, y1, x2, y2 = 18, 166, 181, 169
    roi = hsv[y1:y2, x1:x2]
    average_color = np.mean(roi, axis=(0, 1)).astype(np.uint8)

    full_health = [120, 241, 226]
    critical_health = [0, 0, 49]

    percentage_health = calculate_health_percentage(average_color, full_health, critical_health)

    # Check if the health is decreasing
    if percentage_health < previous_health:
        were_attacked = True
        last_attack_time = time.time()

    # Stop attacking if health hasn't decreased for the last 3 seconds
    elif were_attacked and time.time() - last_attack_time > 3:
        were_attacked = False
        pyautogui.keyUp("space")

    # Press and hold space key if we were attacked recently
    if were_attacked:
        pyautogui.keyDown("space")

    # Handle healing based on cooldowns
    if percentage_health <= 60:
        handle_healing()

    if percentage_health < 99 and not were_attacked:
        pyautogui.press("1")

    return percentage_health


if __name__ == "__main__":
    game_window_title = "Heartwood Online"
    game_window_found = False
    previous_health = 100

    while True:
        game_window = gw.getWindowsWithTitle(game_window_title)

        if game_window:
            if not game_window_found:
                print(f"Found game window: {game_window[0].title}")
                game_window_found = True

            game_window[0].activate()
            screenshot = pyautogui.screenshot(
                region=(game_window[0].left, game_window[0].top, game_window[0].width, game_window[0].height))

            previous_health = detect_health_bar(screenshot, previous_health)

        else:
            if game_window_found:
                print("Game window not found")
                game_window_found = False

        time.sleep(0.1)  # Delay for health monitoring (adjust as needed)

        # Delay for healing function (adjust as needed)
        time.sleep(1)
