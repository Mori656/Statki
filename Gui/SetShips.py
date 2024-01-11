import pygame
import Gui.game_screen as gs
import Gui.Pygame_Util as pu

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()


class SetShips():
    def __init__(self, s):
        self.screen = s
        self.load_game_board_size_from_file("Gui/gameboard.txt")  # Load values from file
        self.load_game_ship_numbers_from_file("Gui/ships.txt")

        # rows should equal columns
        # square self.board 8x8, 9x9, 10x10, 11x11, 12x12
        """
            space - empty space
            S - ship
            . - shotted empty space
            X - shotted ship
        """

        # self.game_board_rows = 12
        # self.game_board_cols = 12

        self.game_board_1 = [[" " for _ in range(self.game_board_cols)] for _ in range(self.game_board_rows)]

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

        # self.board colors
        self.tile_color_empty = (255, 255, 255)
        self.tile_color_ship = (140, 70, 20)
        self.tile_color_shotted_empty = (128, 128, 128)  # w tym przypadku kolor zajetych pól obok statku
        self.tile_color_shotted_ship = (255, 0, 0)
        self.tile_color_border = (200, 232, 232)
        self.tile_color_hover = (190, 160, 140)

        # bottom ui background (footer)
        self.bottom_ui_bg_color = (200, 232, 232)
        self.bottom_ui_bg_width = SCREEN_WIDTH
        self.bottom_ui_bg_height = 100
        self.bottom_ui_bg_x = 0
        self.bottom_ui_bg_y = 980
        self.bottom_ui_bg_rectangle = pygame.Rect(
            (self.title_bg_x, self.title_bg_y, self.title_bg_width, self.title_bg_height))

        # miejsce na statki
        self.ships_placement = (245, 245, 220)
        self.ships_placement_width = 650
        self.ships_placement_height = 650
        self.ships_placement_x = 1020
        self.ships_placement_y = 250
        self.ships_placement_rectangle = pygame.Rect(
            (self.ships_placement_x, self.ships_placement_y, self.ships_placement_width, self.ships_placement_height))

        # confirm button
        self.confirm_button_x = self.ships_placement_x + (self.ships_placement_width - 180) // 2 + 150
        self.confirm_button_y = self.ships_placement_y + self.ships_placement_height - 64
        self.confirm_button_color = (0, 255, 0)
        self.confirm_button_hover_color = (0, 200, 0)
        self.confirm_button = pu.button(self.confirm_button_color, self.confirm_button_x, self.confirm_button_y, 180,
                                        50, "Zatwierdź", (255, 255, 255), "monospace", 30, True)

        # exit button
        self.exit_button_color = (200, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color, SCREEN_WIDTH - 60, 10, 50, 50, "X", (255, 255, 255),
                                     "monospace", 30)

        # settings button
        self.settings_button_color = (128, 128, 128)
        self.settings_button_hover_color = (128, 128, 200)
        self.settings_button = pu.button(self.settings_button_color, SCREEN_WIDTH - 270, 10, 200, 50, "Ustawienia",
                                         (255, 255, 255), "monospace", 30)

        # reset button
        self.reset_button_x = self.ships_placement_x + (self.ships_placement_width - 180) // 2 - 150
        self.reset_button_y = self.ships_placement_y + self.ships_placement_height - 64
        self.reset_button_color = (200, 0, 0)
        self.reset_button_hover_color = (150, 0, 0)
        self.reset_button = pu.button(self.reset_button_color, self.reset_button_x, self.reset_button_y, 180, 50,
                                      "Resetuj", (255, 255, 255), "monospace", 30, True)

        # Symboliczne statki w formie przycisków
        # Ilość statków
        self.tab_number_of_ship = []
        self.set_ships_number(self.number1, self.number2, self.number3, self.number4)

        self.font_number_ship = pygame.font.SysFont("monospace", 20, bold=True)
        self.chosen_ship = 0
        self.rotation = 'v'
        # Tablica z wizualnymi statkami
        self.but_show_ship = []
        self.tile_size = 650 // self.game_board_rows
        self.tile_color = (140, 70, 20)
        for i in range(4):
            butship = pu.button(self.tile_color, self.ships_placement_x + 50 + i * (self.tile_size + 100),
                                self.ships_placement_y + 100, self.tile_size, self.tile_size + (self.tile_size * i))
            self.but_show_ship.append(butship)

        # Tablica na której rozmieścimy kolizje statków
        self.board_rect = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]

        self.start_x = 125
        self.start_y = 250
        self.tile_border_size = 1

        self.prepare_board(self.start_x, self.start_y)

        # Tablica do późniejszego przechowywania statków
        self.but_ships = []

        # Zmienna do okrerślania czy wszystkie statki są położone
        self.all_ships_placed = False

        # legend button
        self.legend_button_color = (0, 200, 0)
        self.legend_button_hover_color = (0, 150, 0)
        self.legend_button = pu.button(self.legend_button_color,
                                       SCREEN_WIDTH - 430, 10,
                                       150, 50, "Legenda", (255, 255, 255), "monospace", 30
                                       )

        # legend
        self.legend_bg_color = (189, 189, 189)
        self.legend_bg_x = 50
        self.legend_bg_y = 150
        self.legend_bg_width = self.screen.get_width() - 2 * self.legend_bg_x
        self.legend_bg_height = 775
        self.legend_bg_rectangle = pygame.Rect(
            (self.legend_bg_x, self.legend_bg_y, self.legend_bg_width, self.legend_bg_height))
        self.show_legend = True

        # legend text
        self.legend_text_color = (0, 0, 0)
        self.legend_font_size = 32
        self.legend_font = pygame.font.SysFont("monospace", self.legend_font_size, bold=True)
        self.legend_padding = 50
        self.legend_row_spacing = 100
        self.legend_text_x = self.legend_bg_x + self.legend_padding
        self.legend_text_y = self.legend_bg_y + self.legend_padding
        self.legend_text_left_margin = 75

        self.legend_texts = ["- puste miejsce",
                             "- statek",
                             "- miejsce, w którym nie można ustawić statku",
                             "- klawisz do obrotu statku"]

        self.legend_rendered_texts = [self.legend_font.render(self.legend_texts[0], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[1], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[2], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[3], 1, self.legend_text_color)]

        self.board_colors = [self.tile_color_empty, self.tile_color_ship,
                             self.tile_color_shotted_empty]

    def draw_legend_button(self):
        self.legend_button.draw(self.screen)

        if self.legend_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.legend_button.color = self.legend_button_hover_color
            self.draw_legend()
        else:
            self.legend_button.color = self.legend_button_color

    def draw_legend(self):
        pygame.draw.rect(self.screen, self.legend_bg_color, self.legend_bg_rectangle)

        for i in range(4):
            if i != 3:
                pygame.draw.rect(self.screen, self.board_colors[i],
                                 (self.legend_bg_x + self.legend_padding,
                                  self.legend_bg_y + self.legend_padding + i * self.legend_row_spacing, 50, 50))
            else:
                text = self.my_font.render('R', True, self.legend_text_color)
                self.screen.blit(text,
                                 (self.legend_bg_x + self.legend_padding + 10,
                                  self.legend_bg_y + self.legend_padding + i * self.legend_row_spacing))

            self.screen.blit(self.legend_rendered_texts[i],
                             (self.legend_text_x + self.legend_text_left_margin,
                              self.legend_text_y + i * self.legend_row_spacing + self.legend_rendered_texts[
                                  i].get_height() // 4))

    def set_new_value(self):
        self.load_game_board_size_from_file('Gui/gameboard.txt')
        self.load_game_ship_numbers_from_file('Gui/ships.txt')
        self.game_board_1 = [[" " for _ in range(self.game_board_cols)] for _ in range(self.game_board_rows)]
        self.board_rect = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        self.prepare_board(self.start_x, self.start_y)
        self.set_ships_number(self.number1,self.number2,self.number3,self.number4)

    def load_game_board_size_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            if len(lines) >= 2:
                self.game_board_rows = int(lines[0].strip())
                self.game_board_cols = int(lines[1].strip())
        except FileNotFoundError:
            print(f"Błąd: {filename} nie znaleziony.")
        except Exception as e:
            print(f"Błąd podczas wczytywania wartości z pliku {filename}: {e}")

    def load_game_ship_numbers_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            if len(lines) >= 4:
                self.number1 = int(lines[0].strip())
                self.number2 = int(lines[1].strip())
                self.number3 = int(lines[2].strip())
                self.number4 = int(lines[3].strip())

        except FileNotFoundError:
            print(f"Błąd: {filename} nie znaleziony.")
        except Exception as e:
            print(f"Błąd podczas wczytywania wartości z pliku {filename}: {e}")

    def prepare_board(self, start_x, start_y):
        self.tile_size = 650 // self.game_board_rows
        self.board = pygame.Surface(
            (self.tile_size * self.game_board_cols + 4 * self.tile_border_size,
             self.tile_size * self.game_board_rows + 4 * self.tile_border_size))
        for row in range(self.game_board_rows):
            for col in range(self.game_board_cols):
                if row < len(self.board_rect) and col < len(
                        self.board_rect[row]):  # Dodane warunki sprawdzające indeksy
                    rect = pygame.Rect(
                        row * self.tile_size + self.tile_border_size + start_x,
                        col * self.tile_size + self.tile_border_size + start_y,
                        self.tile_size - 2 * self.tile_border_size,
                        self.tile_size - 2 * self.tile_border_size)
                    self.board_rect[row][col] = rect

    def toggle_rotation(self):
        if self.rotation == 'h':
            self.rotation = 'v'
        else:
            self.rotation = 'h'

    def draw_exit_button(self):
        self.exit_button.draw(self.screen)

        if self.exit_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.exit_button.color = self.exit_button_hover_color
        else:
            self.exit_button.color = self.exit_button_color

    def draw_settings_button(self):

        self.settings_button.draw(self.screen)

        if self.settings_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.settings_button.color = self.settings_button_hover_color
        else:
            self.settings_button.color = self.settings_button_color

    def draw_confirm_button(self):
        self.confirm_button.draw(self.screen)
        if self.confirm_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.confirm_button.color = self.confirm_button_hover_color
        else:
            self.confirm_button.color = self.confirm_button_color

    def draw_reset_button(self):
        self.reset_button.draw(self.screen)
        if self.reset_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.reset_button.color = self.reset_button_hover_color
        else:
            self.reset_button.color = self.reset_button_color

    def draw_title_text(self):
        self.screen.blit(self.title_text, self.text_rect)

    def draw_title_background(self):
        pygame.draw.rect(self.screen, self.title_bg_color, self.title_bg_rectangle)

    def draw_ship_placement(self):
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(self.ships_placement_x - 5, self.ships_placement_y - 5,
                                     self.ships_placement_width + 10, self.ships_placement_height + 10))
        pygame.draw.rect(self.screen, self.ships_placement, self.ships_placement_rectangle)

    def prepare_board_draw(self, game_board, tile_size, hide_ships=False):
        tile_border_size = self.tile_border_size
        board = pygame.Surface(
            (self.tile_size * self.game_board_cols + 4 * tile_border_size,
             self.tile_size * self.game_board_rows + 4 * tile_border_size))

        for row in range(self.game_board_rows):
            for col in range(self.game_board_cols):
                if row < len(game_board) and col < len(game_board[row]):  # Dodane warunki sprawdzające indeksy
                    marker_color = self.tile_color_empty

                    if game_board[row][col] == " ":
                        marker_color = self.tile_color_empty
                    elif game_board[row][col] == "S":
                        marker_color = self.tile_color_ship
                    elif game_board[row][col] == "h":
                        marker_color = self.tile_color_hover
                    elif game_board[row][col] == ".":
                        marker_color = self.tile_color_shotted_empty

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

    def draw_boards(self):
        start_x = 125
        start_y = 250

        # rows == columns
        tile_size = self.tile_size

        self.draw_axis_description(tile_size, start_x, start_y)

        board_draw = self.prepare_board_draw(self.game_board_1, tile_size)

        self.screen.blit(board_draw, (start_x, start_y))

    def draw_bottom_ui(self):
        pygame.draw.rect(self.screen, self.bottom_ui_bg_color,
                         (self.bottom_ui_bg_x, self.bottom_ui_bg_y, self.bottom_ui_bg_width, self.bottom_ui_bg_height))

    def draw_numberships(self):
        for i, butship in enumerate(self.but_show_ship):
            if (butship.but_rect.collidepoint(pygame.mouse.get_pos())):
                butship.color = self.tile_color_hover
            else:
                butship.color = self.tile_color
            butship.draw(self.screen)
            count = "x" + str(self.tab_number_of_ship[i])
            text = self.my_font.render(count, 1, self.title_text_color)
            self.screen.blit(text, (self.ships_placement_x + 50 + i * (self.tile_size + 100),
                                    self.ships_placement_y + 50))

    def place_ship_on_board(self, x, y):

        ship_len = self.chosen_ship + 1
        r_max = self.game_board_rows
        c_max = self.game_board_cols

        rotation = self.rotation
        r = x
        c = y

        possible_to_place = True
        for a, row in enumerate(self.game_board_1):
            for b, col in enumerate(row):
                if col == "h":
                    self.game_board_1[a][b] = " "
        if rotation == "h":
            c_max -= ship_len
        else:
            r_max -= ship_len
        if self.game_board_1[r][c] == " ":
            if rotation == "v" and c + ship_len <= c_max:
                for j in range(ship_len):
                    if self.game_board_1[r][c + j] != " ":
                        possible_to_place = False
                        break
            elif rotation == "h" and r + ship_len <= r_max:
                for j in range(ship_len):
                    if self.game_board_1[r + j][c] != " ":
                        possible_to_place = False
                        break
            else:
                possible_to_place = False
        else:
            possible_to_place = False
        # mark adjacent fields
        if possible_to_place:
            if rotation == "v":
                for j in range(-1, ship_len + 1):
                    if 0 <= c + j < self.game_board_cols:
                        self.game_board_1[r][c + j] = "."
                        if r + 1 < self.game_board_rows:
                            self.game_board_1[r + 1][c + j] = "."
                        if r - 1 >= 0:
                            self.game_board_1[r - 1][c + j] = "."
            else:
                for j in range(-1, ship_len + 1):
                    if 0 <= r + j < self.game_board_rows:
                        self.game_board_1[r + j][c] = "."
                        if c + 1 < self.game_board_cols:
                            self.game_board_1[r + j][c + 1] = "."
                        if c - 1 >= 0:
                            self.game_board_1[r + j][c - 1] = "."

        # put ship
        if possible_to_place:
            if rotation == "v":
                for j in range(ship_len):
                    self.game_board_1[r][c + j] = "S"
            else:
                for j in range(ship_len):
                    self.game_board_1[r + j][c] = "S"
            self.tab_number_of_ship[self.chosen_ship] -= 1
            self.all_ships_placed = True
            for a in self.tab_number_of_ship:
                if a != 0:
                    self.all_ships_placed = False

    def clear_empty_on_board(self):
        for r in range(self.game_board_rows):
            for c in range(self.game_board_cols):
                if self.game_board_1[r][c] == ".":
                    self.game_board_1[r][c] = " "

    def mark_hover_tile(self, x, y):
        ship_len = self.chosen_ship + 1
        r_max = self.game_board_rows
        c_max = self.game_board_cols

        rotation = self.rotation
        r = x
        c = y
        for a, row in enumerate(self.game_board_1):
            for b, col in enumerate(row):
                if col == "h":
                    self.game_board_1[a][b] = " "
        possible_to_place = True
        rotation = self.rotation
        if rotation == "h":
            c_max -= ship_len
        else:
            r_max -= ship_len
        if self.game_board_1[r][c] == " ":
            if rotation == "v" and c + ship_len <= c_max:
                for j in range(ship_len):
                    if self.game_board_1[r][c + j] != " ":
                        possible_to_place = False
                        break
            elif rotation == "h" and r + ship_len <= r_max:
                for j in range(ship_len):
                    if self.game_board_1[r + j][c] != " ":
                        possible_to_place = False
                        break
            else:
                possible_to_place = False
        else:
            possible_to_place = False

        if possible_to_place:
            if rotation == "v":
                for j in range(ship_len):
                    self.game_board_1[r][c + j] = "h"
            else:
                for j in range(ship_len):
                    self.game_board_1[r + j][c] = "h"

    def reset_board(self):

        for a, row in enumerate(self.game_board_1):
            for b, col in enumerate(row):
                self.game_board_1[a][b] = " "

        self.set_ships_number(self.number1, self.number2, self.number3, self.number4)
        self.all_ships_placed = False

    def set_ships_number(self, a, b, c, d):

        self.tab_number_of_ship = [a, b, c, d]

    def use_draw(self):
        self.draw_title_background()
        self.draw_title_text()
        self.draw_boards()
        self.draw_bottom_ui()
        self.draw_ship_placement()
        self.draw_confirm_button()
        self.draw_settings_button()
        self.draw_exit_button()
        self.draw_reset_button()
        self.draw_numberships()
        self.draw_legend_button()
