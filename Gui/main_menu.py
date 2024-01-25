import pygame
import Gui.Pygame_Util as pu
from pygame import mixer
import Gui.loginPage as lp

loginPage = lp.loginPage

pygame.init()


class main_menu():
    def __init__(self, s):
        self.SCREEN_WIDTH = s.get_width()
        self.SCREEN_HEIGHT = s.get_height()
        self.screen = s
        # pygame.mixer.init()
        # # mixer.music.load('startButton.mp3')
        # mixer.music.set_volume(0.25)

        # Screen settings

        # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Colors
        self.background_color = (200, 232, 232)
        self.button_color = (38, 38, 37)
        self.button_color_hover = (100, 50, 50)
        self.button_text_color = (255, 255, 255)
        self.menu_lettering = (19, 38, 87)

        # Fonts
        self.title_font_size = 80
        self.button_font_size = 40
        self.title_font = pygame.font.SysFont("Comics Sans", self.title_font_size, bold=True)
        self.font = pygame.font.SysFont("Comics Sans", self.button_font_size, bold=False)

        # Menu buttons text
        self.menu_buttons = [
            {"text": "Rozpocznij Grę", "function": "setShips"},
            {"text": "Opcje", "function": "custom"},
            {"text": "Tablica Wyników", "function": "scoreboard"},
            {"text": "Wyloguj się", "function": "loginScreen"},
            {"text": "Opuść grę", "function": "quit_game"}
        ]

        # Buttons atribute
        self.button_font = "Comics Sans"
        self.button_font_size = 40
        self.button_height = 100
        self.button_spacing = 40
        self.total_button_height = (self.button_height + self.button_spacing) * len(self.menu_buttons)
        self.button_y = (self.SCREEN_HEIGHT - self.total_button_height) // 2
        self.button_width = 300
        self.button_x = (self.SCREEN_WIDTH - self.button_width) // 2

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

        # Function to draw the game interface

        # Title
        self.title_text = pygame.font.SysFont("Arial", self.title_font_size, bold=True)
        self.title_text = self.title_text.render("Gra w statki", 1, self.menu_lettering)
        self.title_x = (self.SCREEN_WIDTH - self.title_text.get_width()) // 2
        self.title_y = 50  # Adjust the vertical position of the title

    def draw_main_menu(self):
        self.screen.fill(self.background_color)

        # user_text = self.font.render("Grasz jako", True, self.menu_lettering)
        # user_text_x = self.SCREEN_WIDTH - user_text.get_width() - 20
        # user_text_y = 20
        # self.screen.blit(user_text, (user_text_x, user_text_y))
        # user_login = lp.user_text.user_text
        # login_text = self.font.render(user_login, True, self.menu_lettering)
        # login_text_x = 30
        # login_text_y = 50
        # self.screen.blit(login_text, (login_text_x, login_text_y))

        # Draw title
        self.screen.blit(self.title_text, (self.title_x, self.title_y))
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

    def use_draw(self):
        self.draw_main_menu()

        # Main game loop
        # run = True
        # clock = pygame.time.Clock()

        # while run:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             run = False
        #         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #             run = False
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if event.button == 1:  # Left mouse button
        #                 for i, button in enumerate(menu_buttons):
        #                     button_width = font.render(button["text"], 1, self.button_text_color).get_width() + 20
        #                     button_height = 100
        #                     button_spacing = 40
        #                     button_x = (SCREEN_WIDTH - button_width) // 2
        #                     button_y = (SCREEN_HEIGHT - ((button_height + button_spacing) * len(menu_buttons))) // 2 + (
        #                             i * (button_height + button_spacing))

        #                     if button_x < event.pos[0] < button_x + button_width and \
        #                             button_y < event.pos[1] < button_y + button_height:
        #                         if button["function"] == "start_game":
        #                             start_game()
        #                         elif button["function"] == "options":
        #                             options()
        #                         elif button["function"] == "scoreboard":
        #                             scoreboard()
        #                         elif button["function"] == "quit_game":
        #                             quit_game()

        # draw_main_menu()
        # pygame.display.update()
        # clock.tick(30)



