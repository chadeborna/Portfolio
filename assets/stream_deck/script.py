import serial
import pyautogui
import subprocess
import time
import win32gui
import win32api

ser = serial.Serial('COM3', 9600)
time.sleep(2)

spotify_mode = False
WM_APPCOMMAND = 0x0319

def set_mode(mode):
    ser.write((mode + '\n').encode('utf-8'))

def send_spotify_key(key):
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
    if hwnd:
        win32api.SendMessage(hwnd, WM_APPCOMMAND, 0, key)
    else:
        print("Spotify window not found")

def open_spotify():
    global spotify_mode
    subprocess.Popen(r'C:\Users\Borne\AppData\Roaming\Spotify\Spotify.exe')
    spotify_mode = True
    set_mode("SPOTIFY")
    print("Spotify mode ON")

def skip_song():
    send_spotify_key(0xB0000)

def prev_song():
    send_spotify_key(0xC0000)

def exit_spotify_mode():
    global spotify_mode
    spotify_mode = False
    set_mode("NORMAL")
    print("Spotify mode OFF")

def open_brave():
    subprocess.Popen(r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe')

def open_steam():
    subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')

print("Stream Deck running...")

while True:
    if ser.in_waiting > 0:
        raw = ser.readline()
        print(f"Raw data: {raw}")
        button = raw.decode('utf-8').strip()
        print(f"Button {button} pressed")

        if button == '1':
            open_spotify()
        elif button == '2':
            if spotify_mode:
                skip_song()
            else:
                open_brave()
        elif button == '3':
            if spotify_mode:
                prev_song()
            else:
                open_steam()
        elif button == '4':
            exit_spotify_mode()