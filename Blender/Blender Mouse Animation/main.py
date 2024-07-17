import pyautogui
import time

aralik = 1/60

def record_positions():
    current_second = 0
    with open('mouse_positions.txt', 'w') as file:
        file.write('saniye,x,y\n')
    while current_second < 11:
        x, y = pyautogui.position()
        current_second += aralik
        with open('mouse_positions.txt', 'a') as file:
            file.write(f'{current_second},{x},{y}\n')
        time.sleep(aralik)
        if current_second >= 11:
            break


record_positions()



