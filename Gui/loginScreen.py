import pygame
import Gui.Pygame_Util as pu

class loginScreen():
    def __init__(self, s):
        self.screen = s
        self.SCREEN_WIDTH = s.get_width()
        self.SCREEN_HEIGHT = s.get_height()
        self.BACKGROUND_COLOR = (186, 232, 218)
        self.text_color = (19, 38, 87)
        self.title_font_size = 80
        self.title_font = pygame.font.SysFont("Comics Sans", self.title_font_size, bold=True)
        self.title_font = pygame.font.SysFont("Comics Sans", self.title_font_size, bold=True)

        # do tytułu
        self.font = pygame.font.SysFont("arial", 50, bold=True)
        self.title_text = "Wybór profilu"
        self.title_text_width = self.font.size(self.title_text)[0]
        self.title_text_x = (self.SCREEN_WIDTH - self.title_text_width) // 2
        self.menu_lettering = (19, 38, 87)

        # Title
        self.title_text2 = pygame.font.SysFont("Arial", self.title_font_size, bold=True)
        self.title_text2 = self.title_text2.render("Gra w statki", 1, self.menu_lettering)
        self.title_x2 = (self.SCREEN_WIDTH - self.title_text2.get_width()) // 2
        self.title_y2 = 50  # Adjust the vertical position of the title

        # do wyjasnien
        self.fonts = pygame.font.SysFont("arial", 40, bold=True)

        # exit button
        self.exit_button_color = (200, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color, self.SCREEN_WIDTH - 60, 10, 50, 50, "X", (0, 0, 0),
                                     "monospace",
                                     30)

        self.menu_buttons = [
        {"text": "Graj jako gość", "function": "main_menu"},
        {"text": "Wejdź na profil", "function": "loginPage"},
        {"text": "Utwórz profil", "function": "registerPage"},
        ]

        self.button_font = "Comics Sans"
        self.button_font_size = 40
        self.button_height = 100
        self.button_spacing = 40
        self.total_button_height = (self.button_height + self.button_spacing) * len(self.menu_buttons)
        self.button_y = (self.SCREEN_HEIGHT - self.total_button_height) // 2
        self.button_width = 300
        self.button_x = (self.SCREEN_WIDTH - self.button_width) // 2
        self.button_color = (38, 38, 37)
        self.button_color_hover = (100, 50, 50)
        self.button_text_color = (255, 255, 255)
        # Table buttons
        self.tab_but = []

        a = 0
        for button in self.menu_buttons:
            b = pu.button(self.button_color, self.button_x,
                          self.button_y + (a * (self.button_height + self.button_spacing)), self.button_width,
                          self.button_height, button["text"],
                          self.button_text_color, self.button_font, self.button_font_size)
            self.tab_but.append(b)
            a += 1


    # Rysowanie tytułu
    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def use_draw(self):
        # Utwórz mały prostokąt na środku ekranu
        small_rectangle_width = 500
        small_rectangle_height = 700
        small_rectangle_x = (self.SCREEN_WIDTH - small_rectangle_width) // 2
        small_rectangle_y = (self.SCREEN_HEIGHT - small_rectangle_height) // 2

        # Rysuj mały prostokąt
        pygame.draw.rect(self.screen,(0,0,0),(small_rectangle_x-5, small_rectangle_y-5, small_rectangle_width+10, small_rectangle_height+10))
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (small_rectangle_x, small_rectangle_y, small_rectangle_width, small_rectangle_height))

        # Rysuj tytuł wewnątrz prostokąta
        self.draw_text(self.title_text, self.font, self.text_color,
                       small_rectangle_x + (small_rectangle_width - self.title_text_width) // 2,
                       small_rectangle_y + 50)

        self.screen.blit(self.title_text2, (self.title_x2, self.title_y2))

        a = 0
        for b in self.tab_but:

            # Check if the mouse is over the button
            if b.but_rect.collidepoint(pygame.mouse.get_pos()):
                b.color = self.button_color_hover
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.button_x - 5, self.button_y - 5 + (
                        a * (self.button_spacing + self.button_height)), self.button_width + 10,
                                                                 self.button_height + 10))
                b.draw(self.screen)
            else:
                b.color = self.button_color
                b.draw(self.screen)
            a += 1

    # Zmodyfikowana funkcja draw_exit_button
    def draw_exit_button(self, x, y):
        self.exit_button.x = x
        self.exit_button.y = y
        self.exit_button.draw(self.screen)

        if self.exit_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.exit_button.color = self.exit_button_hover_color
        else:
            self.exit_button.color = self.exit_button_color

    # Zmodyfikowana funkcja draw_menu_button
    def draw_menu_button(self, x, y):
        self.menu_button.x = x
        self.menu_button.y = y
        self.menu_button.draw(self.screen)

        if self.menu_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.menu_button.color = self.menu_button_hover_color
        else:
            self.menu_button.color = self.menu_button_color
