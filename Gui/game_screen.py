import random
import pygame
import threading
from pygame import mixer
import Gui.Pygame_Util as pu

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()


class game_screen():
    def __init__(self, s):
        self.screen = s
        # ----------------------------------------------------------------------------------
        """
            space - empty space
            S - ship
            . - shotted empty space
            X - shotted ship
        """

        # rows should equal columns
        # square board 8x8, 9x9, 10x10, 11x11, 12x12
        self.tab_number_of_ship = [4, 3, 2, 1]
        #self.game_board_rows = 10
        #self.game_board_cols = 10
        self.load_game_board_size_from_file("Gui/gameboard.txt")  # Load values from file
        self.load_game_ship_numbers_from_file("Gui/ships.txt")

        self.game_board_1 = [[" " for _ in range(self.game_board_cols)] for _ in range(self.game_board_rows)]

        # to test board are now generated
        # self.game_board_1 = self.generate_ship_board()
        self.game_board_2 = self.generate_ship_manager()
        # --------------------------------------------------------------------------

        self.turn = "player"
        self.is_end = False

        # title background
        self.title_bg_color = (200, 232, 232)
        self.title_bg_width = 1000
        self.title_bg_height = 75
        self.title_bg_x = (SCREEN_WIDTH // 2) - (self.title_bg_width // 2)
        self.title_bg_y = 0
        self.title_bg_rectangle = pygame.Rect(
            (self.title_bg_x, self.title_bg_y, self.title_bg_width, self.title_bg_height))

        # title text
        self.title_text_string = "Statki"
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
        self.tile_color_hover = (200, 200, 200)

        # bottom ui background (footer)
        self.bottom_ui_bg_color = (200, 232, 232)
        self.bottom_ui_bg_width = SCREEN_WIDTH
        self.bottom_ui_bg_height = 100
        self.bottom_ui_bg_x = 0
        self.bottom_ui_bg_y = 980
        self.bottom_ui_bg_rectangle = pygame.Rect(
            (self.title_bg_x, self.title_bg_y, self.title_bg_width, self.title_bg_height))

        # exit button
        self.exit_button_color = (255, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color,
                                     SCREEN_WIDTH - 60, 10,
                                     50, 50, "X", (255, 255, 255), "monospace", 30
                                     )

        # timer
        self.timer_width = 150
        self.timer_height = 50
        self.timer_x = 10
        self.timer_y = 10
        self.timer_rect = pygame.Rect((self.timer_x, self.timer_y, self.timer_width, self.timer_height))
        self.timer_color = (200, 232, 232)
        self.timer_font_size = 30
        self.timer_text_color = (12, 13, 13)
        self.timer_font = pygame.font.SysFont("monospace", self.timer_font_size, bold=True)

        # legend button
        self.legend_button_color = (0, 200, 0)
        self.legend_button_hover_color = (0, 150, 0)
        self.legend_button = pu.button(self.legend_button_color,
                                       SCREEN_WIDTH - 220, 10,
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

        self.legend_texts = ["- puste miejsce / niesprawdzone miejsce",
                             "- statek",
                             "- trafiony statek",
                             "- pudło / miejsce w którym na pewno nie ma statku"]

        self.legend_rendered_texts = [self.legend_font.render(self.legend_texts[0], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[1], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[2], 1, self.legend_text_color),
                                      self.legend_font.render(self.legend_texts[3], 1, self.legend_text_color)]
        # legend ships
        self.board_colors = [self.tile_color_empty, self.tile_color_ship, self.tile_color_shotted_ship,
                             self.tile_color_shotted_empty]

        # Settings button
        self.settings_button_color = (128, 128, 128)
        self.settings_button_hover_color = (128, 128, 200)
        self.settings_button = pu.button(self.settings_button_color,
                                         SCREEN_WIDTH - 430, 10,
                                         200, 50, "Ustawienia", (255, 255, 255), "monospace", 30
                                         )

        # winner
        self.winner_bg_color = (200, 232, 232)
        self.winner_bg_width = 400
        self.winner_bg_height = 75
        self.winner_bg_x = (SCREEN_WIDTH // 2) - (self.winner_bg_width // 2)
        self.winner_bg_y = 950
        self.winner_bg_rectangle = pygame.Rect(
            (self.winner_bg_x, self.winner_bg_y, self.winner_bg_width, self.winner_bg_height))
        
        # zmienne odnośnie miejsca plansz
        self.board_width = 650
        self.start_x = 125
        self.start_y = 250
        self.space_between_boards = 400

        #zmienne odnośnie kawelków plansz
        self.tile_border_size = 1

        # Tablica na której rozmieścimy kolizje statków gracza
        self.board_rect = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        
        self.board_rect = self.prepare_board(self.start_x, self.start_y)

        # Tablica na której rozmieścimy kolizje statków AI
        self.board_rect_AI = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        
        self.board_rect_AI = self.prepare_board(self.start_x+self.space_between_boards+self.board_width, self.start_y)


    def prepare_board(self, start_x, start_y):
        self.tile_size = 650 // self.game_board_rows
        board_rect = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        self.board = pygame.Surface(
            (self.tile_size * self.game_board_cols + 4 * self.tile_border_size,
             self.tile_size * self.game_board_rows + 4 * self.tile_border_size))
        for row in range(self.game_board_rows):
            for col in range(self.game_board_cols):
                if row < len(board_rect) and col < len(
                        board_rect[row]):  # Dodane warunki sprawdzające indeksy
                    rect = pygame.Rect(
                        row * self.tile_size + self.tile_border_size + start_x,
                        col * self.tile_size + self.tile_border_size + start_y,
                        self.tile_size - 2 * self.tile_border_size,
                        self.tile_size - 2 * self.tile_border_size)
                    board_rect[row][col] = rect
        return board_rect

    def draw_title_text(self):
        self.screen.blit(self.title_text, self.text_rect)

    def draw_title_background(self):
        pygame.draw.rect(self.screen, self.title_bg_color, self.title_bg_rectangle)

    def prepare_board_draw(self, game_board, tile_size, hide_ships=False):
        tile_border_size = self.tile_border_size
        board = pygame.Surface(
            (self.tile_size * self.game_board_cols + 4 * tile_border_size,
             self.tile_size * self.game_board_rows + 4 * tile_border_size))
        
        for row in range(self.game_board_rows):
            for col in range(self.game_board_cols):
                if row < len(game_board) and col < len(game_board[row]):  # Dodane warunki sprawdzające indeksy
                    marker_color = (255, 255, 255)

                    if game_board[row][col] == " ":
                        marker_color = self.tile_color_empty
                    elif game_board[row][col] == "S":
                        marker_color = self.tile_color_ship
                    elif game_board[row][col] == "h":
                        marker_color = self.tile_color_hover
                    elif game_board[row][col] == "Sh":
                        marker_color = self.tile_color_hover
                    elif game_board[row][col] == ".":
                        marker_color = self.tile_color_shotted_empty
                    elif game_board[row][col] == "X":
                        marker_color = self.tile_color_shotted_ship
                    
                    if hide_ships:
                        if game_board[row][col] == "S":
                            marker_color = (255, 255, 255)
                    pygame.draw.rect(board, self.tile_color_border,
                                     (row * tile_size, col * tile_size, tile_size, tile_size))

                    pygame.draw.rect(board, marker_color, (
                        row * tile_size + tile_border_size, col * tile_size + tile_border_size,
                        tile_size - 2 * tile_border_size,
                        tile_size - 2 * tile_border_size))

        return board

    def draw_axis_description(self, tile_size, space_between_boards, start_x, start_y):
        text_color = (12, 13, 13)
        font_size = 30
        offset = 15
        total_space = space_between_boards + tile_size * self.game_board_cols

        font = pygame.font.SysFont("monospace", font_size, bold=True)

        for row in range(self.game_board_rows):
            text = font.render(chr(row + 65), 1, text_color)
            self.screen.blit(text, (start_x - tile_size, start_y + row * tile_size + offset))
            self.screen.blit(text, (start_x - tile_size + total_space, start_y + row * tile_size + offset))

        for col in range(self.game_board_cols):
            text = font.render(str(col + 1), 1, text_color)
            self.screen.blit(text, (start_x + col * tile_size + offset, start_y - tile_size))
            self.screen.blit(text, (start_x + col * tile_size + offset + total_space, start_y - tile_size))

    def draw_boards(self):

        self.draw_axis_description(self.tile_size, self.space_between_boards, self.start_x, self.start_y)

        board = self.prepare_board_draw(self.game_board_1, self.tile_size)
        if not self.is_end:
            board2 = self.prepare_board_draw(self.game_board_2, self.tile_size, True)
        else:
            board2 = self.prepare_board_draw(self.game_board_2, self.tile_size, False)

        self.screen.blit(board, (self.start_x, self.start_y))
        self.screen.blit(board2, (self.start_x + self.tile_size * self.game_board_cols + self.space_between_boards, self.start_y))

    def draw_legend_button(self):

        self.legend_button.draw(self.screen)

        if self.legend_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.legend_button.color = self.legend_button_hover_color
        else:
            self.legend_button.color = self.legend_button_color

    def draw_legend(self):

        pygame.draw.rect(self.screen, self.legend_bg_color, self.legend_bg_rectangle)

        for i in range(4):
            pygame.draw.rect(self.screen, self.board_colors[i],
                             (self.legend_bg_x + self.legend_padding,
                              self.legend_bg_y + self.legend_padding + i * self.legend_row_spacing, 50, 50))

            self.screen.blit(self.legend_rendered_texts[i],
                             (self.legend_text_x + self.legend_text_left_margin,
                              self.legend_text_y + i * self.legend_row_spacing + self.legend_rendered_texts[
                                  i].get_height() // 4))

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

    def draw_bottom_ui(self):
        pygame.draw.rect(self.screen, self.bottom_ui_bg_color,
                         (self.bottom_ui_bg_x, self.bottom_ui_bg_y, self.bottom_ui_bg_width, self.bottom_ui_bg_height))

    def draw_timer(self):
        # in ms
        current_time = pygame.time.get_ticks()

        hours = str(current_time // 3600000).zfill(2)
        minutes = str((current_time // 60000) % 60).zfill(2)
        seconds = str((current_time // 1000) % 60).zfill(2)

        timer_text = self.timer_font.render(f"{hours}:{minutes}:{seconds}", 1, self.timer_text_color)

        pygame.draw.rect(self.screen, self.timer_color, self.timer_rect)
        self.screen.blit(timer_text, (self.timer_x + 10, self.timer_y + 10))

    def draw_winner(self):
        # winner
        winner_text_string = ""
        if self.is_end:
            if self.turn == "player":
                winner_text_string = "Komputer zwyciężył"
            else:
                winner_text_string = "Wygrałeś"

            winner_text_color = (19, 38, 87)
            winner_font_size = 50
            winner_font = pygame.font.SysFont("monospace", winner_font_size, bold=True)
            winner_text = winner_font.render(winner_text_string, 1, winner_text_color)
            winner_rect = winner_text.get_rect(center=self.winner_bg_rectangle.center)

            pygame.draw.rect(self.screen, self.winner_bg_color, self.winner_bg_rectangle)
            self.screen.blit(winner_text, winner_rect)

    def use_draw(self):
        self.draw_title_background()
        self.draw_title_text()
        self.draw_boards()
        self.draw_legend_button()
        self.draw_settings_button()
        self.draw_exit_button()
        self.draw_bottom_ui()
        self.draw_timer()

        self.draw_winner()



    # clock = pygame.time.Clock()
    # start_time = pygame.time.get_ticks()

    def generate_ship_manager(self):
        MAX_ERRORS = 50

        b = (None, None)
        i = 0
        while b[0] is None:
            i += 1
            print(i, ". attempt to create a board", sep="")

            b = self.generate_ship_board(MAX_ERRORS)

        print(i+1, ". board created successfully", sep="")
        return b[0]

    def generate_ship_board(self, MAX_ERRORS):
        board = [[" " for _ in range(self.game_board_cols)] for _ in range(self.game_board_rows)]
        ships_to_place = self.tab_number_of_ship.copy()
        i = 0
        errors = 0
        while True:
            errors = 0
            if all(S == 0 for S in ships_to_place):
                break
            ship_len = i+1
            r_max = self.game_board_rows-1
            c_max = self.game_board_cols-1
                
            rotation = "h"
            r = 0
            c = 0
            rotation = random.choice(("v", "h"))
            if rotation == "h":
                c_max = c_max - ship_len + 1
            else:
                r_max = r_max - ship_len + 1
            possible_to_place = False
            while not possible_to_place:
                if errors >= MAX_ERRORS:
                    return None, errors
                errors += 1

                is_cell_free = False
                while not is_cell_free:
                    if errors >= MAX_ERRORS:
                        return None, errors
                    errors += 1

                    r = random.randint(0, r_max)
                    c = random.randint(0, c_max)
                    if board[r][c] == " ":
                        is_cell_free = True

                possible_to_place = True
                if rotation == "h":
                    for j in range(ship_len):
                        if board[r][c + j] != " ":
                            possible_to_place = False
                            break
                else:
                    for j in range(ship_len):
                        if board[r + j][c] != " ":
                            possible_to_place = False
                            break

            # mark adjacent fields
            if possible_to_place:
                if rotation == "h":
                    for j in range(-1, ship_len + 1):
                        if 0 <= c + j < self.game_board_cols:
                            board[r][c + j] = "."
                            if r + 1 < self.game_board_rows:
                                board[r + 1][c + j] = "."
                            if r - 1 >= 0:
                                board[r - 1][c + j] = "."
                else:
                    for j in range(-1, ship_len + 1):
                        if 0 <= r + j < self.game_board_rows:
                            board[r + j][c] = "."
                            if c + 1 < self.game_board_cols:
                                board[r + j][c + 1] = "."
                            if c - 1 >= 0:
                                board[r + j][c - 1] = "."

            # put ship
            if possible_to_place:
                if rotation == "h":
                    for j in range(ship_len):
                        board[r][c + j] = "S"
                else:
                    for j in range(ship_len):
                        board[r + j][c] = "S"
                ships_to_place[i]-=1
                if ships_to_place[i] == 0:
                    i+=1
        for r in range(self.game_board_rows):
            for c in range(self.game_board_cols):
                if board[r][c] == ".":
                    board[r][c] = " "

        # draw board after preparing
        # for r in range(self.game_board_rows):
        #     print(board[r])
        # print()

        return board, errors

    def cpu_move(self):
        self.turn = "pause"
        def delayed_move():
            r, c = None, None
            possible_shoot = False
            while not possible_shoot:
                r = random.randint(0, self.game_board_rows - 1)
                c = random.randint(0, self.game_board_cols - 1)

                if self.game_board_1[r][c] != "." and self.game_board_1[r][c] != "X":
                    possible_shoot = True

            if self.game_board_1[r][c] == "S":
                self.game_board_1[r][c] = "X"
            elif self.game_board_1[r][c] == " ":
                self.game_board_1[r][c] = "."
            self.turn = "player"
        thread = threading.Timer(1.0, delayed_move)
        thread.start()

    def check_end(self):
        if not any("S" in s for s in self.game_board_1):
            self.is_end = True

        elif not any("S" in s for s in self.game_board_2) and not any("Sh" in s for s in self.game_board_2):
            self.is_end = True

        else:
            self.is_end = False

    def player_shoot(self, row_index, col_index):

        if self.game_board_2[row_index][col_index] == "X":
            return
        elif self.game_board_2[row_index][col_index] == ".":
            return
        elif self.game_board_2[row_index][col_index] == "Sh":
            self.game_board_2[row_index][col_index] = "X"
        elif self.game_board_2[row_index][col_index] != "X":
            self.game_board_2[row_index][col_index] = "."

        self.turn="cpu"

    def mark_hover_tile(self, x, y):
        for a, row in enumerate(self.game_board_2):
            for b, col in enumerate(row):
                if col == "h":
                    self.game_board_2[a][b] = " "
                if col == "Sh":
                    self.game_board_2[a][b] = "S"

        if self.game_board_2[x][y] == " ":
            self.game_board_2[x][y] = "h"
        if self.game_board_2[x][y] == "S":
            self.game_board_2[x][y] = "Sh"

        
        

    #Funkcja ustawia noa ilość statków
    def set_ships_number(self, a, b, c, d):

        self.tab_number_of_ship = [self.number1, self.number2, self.number3, self.number4]


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

    # Funkcja do ustawiania nowych wartości po otrzymaniu danych o statkach
    def set_new_value(self):

        self.load_game_board_size_from_file('Gui/gameboard.txt')
        self.load_game_ship_numbers_from_file('Gui/ships.txt')
        self.game_board_1 = [[" " for _ in range(self.game_board_cols)] for _ in range(self.game_board_rows)]
        self.set_ships_number(self.number1,self.number2,self.number3,self.number4)
        self.game_board_2 = self.generate_ship_manager()
        self.board_rect = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        self.board_rect = self.prepare_board(self.start_x, self.start_y)
        self.board_rect_AI = [[pygame.Rect(0, 0, 0, 0) for _ in range(self.game_board_cols)] for _ in
                           range(self.game_board_rows)]
        self.board_rect_AI = self.prepare_board(self.start_x+self.space_between_boards+self.board_width, self.start_y)