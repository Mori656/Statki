import sqlite3

import Gui.Pygame_Util as pu
import sys
import pygame
from pygame import mixer, init

pygame.init()
pygame.display.set_caption('Tablica Wyników')

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (200, 232, 232)
text_color = (19, 38, 87)

# Connect with db
dbconn = sqlite3.connect('player.db')
dbcursor = dbconn.cursor()
dbcursor.execute("SELECT * FROM score")
dbcursor.close()
dbconn.close()



class scoreboard():
    def __init__(self, s):
        self.screen = s
        # do tytułu
        self.font = pygame.font.SysFont("arial", 80, bold=True)
        self.title_text = "Tablica Wyników"
        self.title_text_width = self.font.size(self.title_text)[0]
        self.title_text_x = (SCREEN_WIDTH - self.title_text_width) // 2

        # do wyjasnien
        self.fonts = pygame.font.SysFont("arial", 40, bold=True)

        # exit button
        self.exit_button_color = (200, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color, SCREEN_WIDTH - 60, 10, 50, 50, "X", (0, 0, 0), "monospace",
                                     30)

        # menu button
        self.menu_button_color = (128, 128, 128)
        self.menu_button_hover_color = (128, 128, 200)
        self.menu_button = pu.button(self.menu_button_color, SCREEN_WIDTH - 220, 10, 150, 50, "Menu", (0, 0, 0),
                                     "monospace", 30)

    # Rysowanie tytułu
    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def use_draw(self, y_position=270):
        self.screen.fill(BACKGROUND_COLOR)

        # rysowanie tytułu
        self.draw_text(self.title_text, self.font, text_color, self.title_text_x, 50)

        # rysowanie przycisku wyjścia
        self.draw_exit_button()
        self.draw_menu_button()

        # rysowanie "wyjasnien"
        self.draw_text("Login", self.fonts, text_color, 50, 250)
        self.draw_text("Zwycięstwa", self.fonts, text_color, 350, 250)
        self.draw_text("Porażki", self.fonts, text_color, 650, 250)
        self.draw_text("Bilans", self.fonts, text_color, 950, 250)


        dbconn = sqlite3.connect('player.db')
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM score ORDER BY score.winratio DESC LIMIT 8")
        records = dbcursor.fetchall()
        dbcursor.close()
        dbconn.close()

        for record in records:
            textL = f"{record[1]}"
            textZ = f"{record[2]}"
            textP = f"{record[3]}"
            textB = f"{record[4]}"
            y_position += 80  # Zwiększenie pozycji Y dla każdego kolejnego rekordu
            self.draw_text(textL, self.fonts, text_color, 50, y_position)
            self.draw_text(textZ, self.fonts, text_color, 400, y_position)
            self.draw_text(textP, self.fonts, text_color, 700, y_position)
            self.draw_text(textB, self.fonts, text_color, 1000, y_position)

    def draw_exit_button(self):
        self.exit_button.draw(self.screen)

        if self.exit_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.exit_button.color = self.exit_button_hover_color
        else:
            self.exit_button.color = self.exit_button_color

    def draw_menu_button(self):
        self.menu_button.draw(self.screen)

        if self.menu_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.menu_button.color = self.menu_button_hover_color
        else:
            self.menu_button.color = self.menu_button_color

