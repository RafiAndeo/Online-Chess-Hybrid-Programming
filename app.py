# app.py adalah file execute client untuk memainkan online chess

# import library PySimpleGUI untuk membuat GUI
# import library subprocess untuk menjalankan file lain

import PySimpleGUI as sg
import subprocess

# tema GUI yang digunakan

sg.theme('LightBlue')

# layout GUI yang digunakan

layout = [[sg.Text("Welcome to Online Chess developed with Python Hybrid Programming"), sg.Text(size=(10, 1), key="-OUTPUT-")],
          [sg.Text("===================================================")],
          [sg.Text("Change Log")],
          [sg.Text("1.0.0 - Initial Release (2022-12-08)")],
          [sg.Text("1.0.1 - (2022-12-14)")],
          [sg.Text("[ADDED] - Menu to start the game")],
          [sg.Text("[CHANGED] - Window size to 1920 x 1080")],
          [sg.Text("1.0.2 - (2022-12-26)")],
          [sg.Text("[ADDED] - Background Image for the game")],
          [sg.Text("[CHANGED] - Chess board image")],
          [sg.Text("1.0.3 - (2022-12-28)")],
          [sg.Text("[CHANGED] - Players' usernames will be set as random")],
          [sg.Text("[FIXED] - Duplicate player username")],
          [sg.Text("[CHANGED] - Font Type")],
          [sg.Text("1.0.4 - (2022-12-29)")],
          [sg.Text("[FEATURE] - Added Radmin VPN to the game")],
          [sg.Text("===================================================")],
          [sg.Text("Please click the button below to start the game")],
          [sg.Button("Start"), sg.Button("Exit")]]
window = sg.Window("Online Chess", layout)

# fungsi untuk menjalankan GUI


def start_game():
    while True:
        event, values = window.read()
        if event == "Start":
            subprocess.call(['python', 'window.py'])
        elif event == "Exit":
            break
        elif event == sg.WIN_CLOSED:
            break
    window.close()


if __name__ == '__main__':
    start_game()
