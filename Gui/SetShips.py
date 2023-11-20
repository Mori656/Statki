import pygame
from pygame import mixer
import tkinter as tk
from tkinter import Scale
import Gui.game_screen as gs


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()


class SetShips():
    def __init__(self, s):
        self.screen = s
        """
            space - empty space
            S - ship
            . - shotted empty space
            X - shotted ship
        """

        # rows should equal columns
        # square board 8x8, 9x9, 10x10, 11x11, 12x12
        self.game_board_rows = 10
        self.game_board_cols = 10

        self.game_board_1 = [[" " for c in range(self.game_board_cols)] for r in range(self.game_board_rows)]


        # -------------------------------------------------------------------------- end mock

        # title background
        self.title_bg_color = (200, 232, 232)
        self.title_bg_width = 1000
        self.title_bg_height = 75
        self.title_bg_x = (SCREEN_WIDTH // 2) - (self.title_bg_width // 2)
        self.title_bg_y = 0
        self.title_bg_rectangle = pygame.Rect(
            (self.title_bg_x, self.title_bg_y, self.title_bg_width, self.title_bg_height))

        # title text
        self.title_text_string = "Ustaw swoje statki"
        self.title_text_color = (19, 38, 87)
        self.title_font_size = 50
        self.my_font = pygame.font.SysFont("monospace", self.title_font_size, bold=True)
        self.title_text = self.my_font.render(self.title_text_string, 1, self.title_text_color)
        self.title_text_x = SCREEN_WIDTH // 2 - self.title_text.get_rect().width
        self.title_text_y = self.title_bg_y + self.title_text.get_rect().height // 2
        self.text_rect = self.title_text.get_rect(center=self.title_bg_rectangle.center)

        # board colors
        self.tile_color_empty = (255, 255, 255)
        self.tile_color_ship = (140, 70, 20)
        self.tile_color_shotted_empty = (128, 128, 128)
        self.tile_color_shotted_ship = (255, 0, 0)
        self.tile_color_border = (200, 232, 232)

        # bottom ui background (footer)
        self.bottom_ui_bg_color = (200, 232, 232)
        self.bottom_ui_bg_width = SCREEN_WIDTH
        self.bottom_ui_bg_height = 100
        self.bottom_ui_bg_x = 0
        self.bottom_ui_bg_y = 980
        self.bottom_ui_bg_rectangle = pygame.Rect(
            (self.title_bg_x, self.title_bg_y, self.title_bg_width, self.title_bg_height))

        #miejsce na statki
        self.ships_placement = (245, 245, 220)
        self.ships_placement_width = 650
        self.ships_placement_height = 650
        self.ships_placement_x = 1020
        self.ships_placement_y = 250
        self.ships_placement_rectangle = pygame.Rect(
            (self.ships_placement_x, self.ships_placement_y, self.ships_placement_width, self.ships_placement_height))

        # exit button
        self.exit_button_width = 150
        self.exit_button_height = 50
        self.exit_button_x = SCREEN_WIDTH - self.exit_button_width - 10
        self.exit_button_y = 10
        self.exit_button_rect = pygame.Rect(
            (self.exit_button_x, self.exit_button_y, self.exit_button_width, self.exit_button_height))
        self.exit_button_color = (255, 0, 0)
        self.exit_button_hover_color = (200, 0, 0)
        self.exit_button_font_size = 30
        self.exit_button_font = pygame.font.SysFont("monospace", self.exit_button_font_size, bold=True)
        self.exit_button_text = self.exit_button_font.render("Wyjście", 1, (255, 255, 255))
        # exit_sound = pygame.mixer.Sound('button.mp3')

        # confirm button
        self.confirm_button_width = 180
        self.confirm_button_height = 50
        self.confirm_button_x = self.ships_placement_x + (self.ships_placement_width - self.confirm_button_width) // 2
        self.confirm_button_y = self.ships_placement_y + self.ships_placement_height - 64
        self.confirm_button_rect = pygame.Rect(
            (self.confirm_button_x, self.confirm_button_y, self.confirm_button_width, self.confirm_button_height))
        self.confirm_button_color = (0, 255, 0)
        self.confirm_button_hover_color = (0, 200, 0)
        self.confirm_button_font_size = 30
        self.confirm_button_font = pygame.font.SysFont("monospace", self.confirm_button_font_size, bold=True)
        self.confirm_button_text = self.confirm_button_font.render("Zatwierdź", 1, (255, 255, 255))
        self.confirm_button_clicked = False

    def draw_title_text(self):
        self.screen.blit(self.title_text, self.text_rect)

    def draw_title_background(self):
        pygame.draw.rect(self.screen, self.title_bg_color, self.title_bg_rectangle)

    def draw_ship_placement(self):
        pygame.draw.rect(self.screen,(0,0,0),
                         pygame.Rect(self.ships_placement_x-5, self.ships_placement_y-5, self.ships_placement_width+10, self.ships_placement_height+10))
        pygame.draw.rect(self.screen,self.ships_placement,self.ships_placement_rectangle)
        self.draw_ship_placement_text()


    def prepare_board(self, game_board, tile_size, hide_ships=False):
        tile_border_size = 1

        board = pygame.Surface(
            (tile_size * self.game_board_cols + 4 * tile_border_size,
             tile_size * self.game_board_rows + 4 * tile_border_size))

        # Ustaw pozycję planszy w oknie gry
        start_x = 125
        start_y = 250

        for row in range(self.game_board_rows):
            for col in range(self.game_board_cols):
                marker_color = (255, 255, 255)

                #Pozycja myszy
                mouse_x, mouse_y = pygame.mouse.get_pos()

                mouse_x -= start_x
                mouse_y -= start_y

                rect = pygame.Rect(
                    row * tile_size + tile_border_size,
                    col * tile_size + tile_border_size,
                    tile_size - 2 * tile_border_size,
                    tile_size - 2 * tile_border_size)

                #Mysz nad kwadratem - hover efekt
                if rect.collidepoint(mouse_x, mouse_y):
                    marker_color = (200, 200, 200)

                pygame.draw.rect(board, self.tile_color_border,
                                 (row * tile_size, col * tile_size, tile_size, tile_size))

                pygame.draw.rect(board, marker_color, (
                    row * tile_size + tile_border_size, col * tile_size + tile_border_size,
                    tile_size - 2 * tile_border_size,
                    tile_size - 2 * tile_border_size))
        return board

    def draw_axis_description(self, tile_size, start_x, start_y):
        text_color = (12, 13, 13)
        font_size = 30
        offset = 15
        total_space = tile_size * self.game_board_cols

        font = pygame.font.SysFont("monospace", font_size, bold=True)

        for row in range(self.game_board_rows):
            text = font.render(chr(row + 65), 1, text_color)
            self.screen.blit(text, (start_x - tile_size, start_y + row * tile_size + offset))


        for col in range(self.game_board_cols):
            text = font.render(str(col + 1), 1, text_color)
            self.screen.blit(text, (start_x + col * tile_size + offset, start_y - tile_size))

# Ta funkcja jest do usuniecia, tylko info :)-------------------------

    def draw_confirm_button(self):
        pygame.draw.rect(self.screen, self.confirm_button_color, self.confirm_button_rect)

        if self.confirm_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.confirm_button_hover_color, self.confirm_button_rect)

        self.screen.blit(self.confirm_button_text, (self.confirm_button_x + 10, self.confirm_button_y + 10))

    def check_confirm_button_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.confirm_button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            self.confirm_button_clicked = True
        else:
            self.confirm_button_clicked = False
    def draw_ship_placement_text(self):
        text_color = (0, 0, 0)
        font_size = 40
        font = pygame.font.SysFont("monospace", font_size, bold=True)

        text1 = font.render("Tutaj położycie obiekty ", 1, text_color)
        text2 = font.render("statki, kiedy je zrobicie :)", 1, text_color)
        text_x = self.ships_placement_x + self.ships_placement_width // 2 - text1.get_rect().width // 2
        text_y = self.ships_placement_y + self.ships_placement_height // 2 - text1.get_rect().height // 2 - 60

        self.screen.blit(text1, (text_x, text_y))

        text_x = self.ships_placement_x + self.ships_placement_width // 2 - text2.get_rect().width // 2
        text_y = self.ships_placement_y + self.ships_placement_height // 2 - text2.get_rect().height // 2

        self.screen.blit(text2, (text_x, text_y))

# Az dotąd mozna usunąć -----------------------------------------------
    def draw_boards(self):
        start_x = 125
        start_y = 250

        # rows == columns
        tile_size = 650 // self.game_board_rows

        self.draw_axis_description(tile_size, start_x, start_y)

        board = self.prepare_board(self.game_board_1, tile_size)

        self.screen.blit(board, (start_x, start_y))


    def draw_exit_button(self):
        pygame.draw.rect(self.screen, self.exit_button_color, self.exit_button_rect)

        if self.exit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.exit_button_hover_color, self.exit_button_rect)

        self.screen.blit(self.exit_button_text, (self.exit_button_x + 10, self.exit_button_y + 10))

    def draw_bottom_ui(self):
        pygame.draw.rect(self.screen, self.bottom_ui_bg_color,
                         (self.bottom_ui_bg_x, self.bottom_ui_bg_y, self.bottom_ui_bg_width, self.bottom_ui_bg_height))

    def use_draw(self):
        self.draw_title_background()
        self.draw_title_text()
        self.draw_boards()
        self.draw_bottom_ui()
        self.draw_ship_placement()
        self.draw_confirm_button()



    settings_button_width = 160
    settings_button_height = 50
    settings_button_x = SCREEN_WIDTH - settings_button_width - 200
    settings_button_y = 10  # Adjust the vertical position
    settings_button_rect = pygame.Rect(
        (settings_button_x, settings_button_y, settings_button_width, settings_button_height))
    settings_button_color = (128, 128, 128)  # Green button color
    settings_button_hover_color = (128, 128, 200)  # Green hover color
    settings_button_font_size = 30
    settings_button_font = pygame.font.SysFont("monospace", settings_button_font_size, bold=True)
    settings_button_text = settings_button_font.render("Głośność", 1, (255, 255, 255))

    exit_button_clicked = False