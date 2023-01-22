# import library os untuk membangun interaksi antara program dan sistem operasi
# import library time untuk mengatur waktu
# import library pygame untuk membuat game
# import library tkinter untuk membuat GUI
# import library random untuk mengacak angka
# import library client untuk mengimport class client
# import library piece untuk mengimport class piece

import os
import time
import pygame
import tkinter as tk
import random
from client import Client
from piece import get_piece

# mendefinisikan host dan port yang digunakan berdasarkan ip address dan port yang telah ditentukan dari Radmin VPN

host = "26.122.184.85"
port = 10000
address = (host, port)

# resolusi layar yang digunakan adalah fullscreen

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BOARD_LENGTH = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 1.3
TILE_LENGTH = BOARD_LENGTH / 8

# mendefinisikan judul dan font yang digunakan

CAPTION = "Online Chess"
FONT = "verdana"

# mendefinisikan warna yang digunakan

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PIECE_GREEN_BG = (0, 128, 128)

# mengimport gambar background dan mengubah ukurannya sesuai dengan resolusi layar

bg_img = pygame.image.load('assets/images/bg.jpg')
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# membuat function window utama user interface


def draw_start_menu(window: pygame.Surface, name: str, connection_lost: bool = False, connection_refused: bool = False) -> None:

    window.blit(bg_img, (0, 0))

    font = pygame.font.SysFont(FONT, SCREEN_HEIGHT // 10)
    text1 = font.render("Press space", True, WHITE)
    text2 = font.render("to start the game", True, WHITE)

    if connection_refused:
        conn_text = font.render("(connection refused)", True, RED)
        conn_text_rect = conn_text.get_rect()
        conn_text_rect.centerx = SCREEN_WIDTH / 2
        window.blit(conn_text, conn_text_rect)

    if connection_lost:
        conn_text = font.render("(connection lost)", True, RED)
        conn_text_rect = conn_text.get_rect()
        conn_text_rect.centerx = SCREEN_WIDTH / 2
        window.blit(conn_text, conn_text_rect)

    text1_rect = text1.get_rect()
    text1_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT /
                         2 - SCREEN_HEIGHT // 10)
    text2_rect = text2.get_rect()
    text2_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    window.blit(text1, text1_rect)
    window.blit(text2, text2_rect)

    pygame.display.update()

# membuat function window untuk menunggu player lain


def draw_waiting(window: pygame.Surface) -> None:

    window.blit(bg_img, (0, 0))

    font = pygame.font.SysFont(FONT, SCREEN_HEIGHT // 10)
    text = font.render("Waiting for player", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    window.blit(text, text_rect)
    pygame.display.update()

# membuat function window menu untuk memulai game dan keluar game


def menu_screen(window: pygame.Surface, name: str, connection_lost: bool = False) -> None:

    draw_start_menu(window, name, connection_lost)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    draw_waiting(window)
                    try:
                        client = Client(name, address)
                        chess_game(window, client)
                    except ConnectionRefusedError:
                        draw_start_menu(window, name, connection_refused=True)

# membuat function window untuk bermain


def chess_game(window: pygame.Surface, client: Client) -> None:

    window.blit(bg_img, (0, 0))

    board = client.board

    board.draw(window, client.name)
    pygame.display.update()

    while True:
        if board.winner is not None:
            time.sleep(5)
            menu_screen(window, client.name)

        if client.name != board.turn:
            try:
                command = client.receive(4096)
                command["window"] = window
                command["my_name"] = client.name
                board.command(command, window)
            except ConnectionResetError:
                menu_screen(window, client.name, connection_lost=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.disconnect()
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = int(
                    (y - (SCREEN_HEIGHT - BOARD_LENGTH) / 2) // TILE_LENGTH)
                col = int((x - (SCREEN_WIDTH - BOARD_LENGTH) / 2) // TILE_LENGTH)

                if not 0 <= row <= 7 or not 0 <= col <= 7:
                    continue

                selected = board.selected

                if board.click(client.name, row, col, window):
                    replacement = None

                    if board.board[row][col].piece_name == "pawn" and (row == 0 and board.board[row][col].color == "w" or row == 7 and board.board[row][col].color == "b"):
                        new_piece = []

                        root = tk.Tk()
                        tk.Label(root, text="Enter the piece you want to replace your pawn with").grid(
                            row=0)
                        piece_input = tk.Entry(root)
                        piece_input.grid(row=1)
                        tk.Button(root, text="Enter", command=lambda: new_piece.append(get_piece(
                            root, piece_input, row, col, board.board[row][col].color))).grid(row=2, pady=4)

                        root.mainloop()

                        board.board[row][col] = new_piece[-1]
                        board.update_valid_moves()
                        board.board[row][col].draw(window)

                        replacement = new_piece[-1].piece_name

                    client.send({
                        "command": "move",
                        "p_name": client.name,
                        "pos_before": selected,
                        "pos_after": (row, col),
                        "replacement": replacement,
                    })

        pygame.display.update()

# membuat function main untuk menjalankan game


def main() -> None:

    pygame.init()

    user = random.sample(range(10), 1)

    name = "player " + str(user)

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(pygame.image.load(
        os.path.join("assets", "images", "window_icon.png")))

    menu_screen(window, name)


if __name__ == "__main__":
    main()
