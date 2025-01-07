import pyautogui as pa
import time
import pyperclip

pa.PAUSE = 1

# Esse serviço vai entrar no youtube pelo seu computador 

pa.press('win')
pa.write("chrome")
pa.press('ENTER')
pa.write("youtube.com")
pa.press("ENTER")
time.sleep(4)
pa.click(x=613, y=99)
pyperclip.copy("Naruto AMV")
pa.hotkey("ctrl", "v")
pa.press("ENTER")