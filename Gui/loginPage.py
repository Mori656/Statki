import pygame
import Gui.Pygame_Util as pu
import sqlite3
import Gui.main_menu

pygame.init()
pygame.display.set_caption('Wybór profilu')

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (200, 232, 232)
text_color = (19, 38, 87)

#connect with db
dbconn = sqlite3.connect('player.db')
dbcursor = dbconn.cursor()


class loginPage:
    def __init__(self, s):
        self.screen = s
        self.active_login = False
        self.active_password = False

        self.prev_button_state = False

        # message
        self.info_message = ""

        # Fonts
        self.font_title = pygame.font.SysFont("arial", 80, bold=True)
        self.font_label = pygame.font.SysFont("arial", 32, bold=True)
        self.base_font = pygame.font.Font(None, 40)

        # Title
        self.title_text = "Wejdź na profil:"
        self.title_text_width = self.font_title.size(self.title_text)[0]
        self.title_text_x = (SCREEN_WIDTH - self.title_text_width) // 2

        # exit button
        self.exit_button_color = (200, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color, SCREEN_WIDTH - 60, 10, 50, 50, "X", (0, 0, 0), "monospace",
                                     30)

        # menu button
        self.menu_button_color = (128, 128, 128)
        self.menu_button_hover_color = (128, 128, 200)
        self.menu_button = pu.button(self.menu_button_color, SCREEN_WIDTH - 220, 10, 150, 50, "Powrót", (0, 0, 0),
                                     "monospace", 30)

        # login button
        self.login_button_color = (37,38,37)
        self.login_button_hover_color = (100, 50, 50)
        self.login_button = pu.button(self.login_button_color, (SCREEN_WIDTH - 600+300) // 2,
                                      (SCREEN_HEIGHT - 800) // 2 + 400, 300, 50, "Wejdź do gry", (255,255,255), "monospace", 30,bold=True)



        self.base_font = pygame.font.Font(None, 40)
        self.user_text = ''
        self.password_text = ''

        # Clock
        self.clock = pygame.time.Clock()

        # Input rectangle
        self.input_container_rect_back = pygame.Rect((SCREEN_WIDTH - 610) // 2,
                                                     (SCREEN_HEIGHT - 810) // 2 + 30,
                                                     610, 810)

        self.input_container_rect = pygame.Rect((SCREEN_WIDTH - 600) // 2,
                                                (SCREEN_HEIGHT - 800) // 2 + 30,
                                                600, 800)

        self.input_rect_login = pygame.Rect(self.input_container_rect.x + (600 - 300) // 2,
                                            self.input_container_rect.y + (800 - 40) // 2 - 270,
                                            300, 40)
        self.input_rect_password = pygame.Rect(self.input_container_rect.x + (600 - 300) // 2,
                                               self.input_container_rect.y + (800 - 40) // 2 - 146,
                                               300, 40)

        self.input_rect_login_back = pygame.Rect(self.input_container_rect.x + (600 - 300) // 2 - 5,
                                                 self.input_container_rect.y + (800 - 40) // 2 - 270 - 5,
                                                 310, 50)
        self.input_rect_password_back = pygame.Rect(self.input_container_rect.x + (600 - 300) // 2 - 5,
                                                    self.input_container_rect.y + (800 - 40) // 2 - 146 - 5,
                                                    310, 50)

        self.button_back = pygame.Rect((SCREEN_WIDTH - 600+300) // 2-5,
                                      (SCREEN_HEIGHT - 800) // 2 + 400-5,310,60)

        self.color_active = (250, 250, 250)
        self.color_passive = (160, 160, 160)
        self.color_login = self.color_passive
        self.color_password = self.color_passive

    def draw_input_login(self):
        if self.active_login:
            self.color_login = self.color_active
        else:
            self.color_login = self.color_passive

        if self.active_password:
            self.color_password = self.color_active
        else:
            self.color_password = self.color_passive

        pygame.draw.rect(self.screen, (0, 0, 0), self.input_container_rect_back, 0)
        pygame.draw.rect(self.screen, (186, 232, 218), self.input_container_rect, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_rect_login_back, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_rect_password_back, 0)

        pygame.draw.rect(self.screen, self.color_login, self.input_rect_login, 0)
        pygame.draw.rect(self.screen, self.color_password, self.input_rect_password, 0)

        label_surface = self.font_label.render("Login:", True, (0, 0, 0))
        self.screen.blit(label_surface, (self.input_rect_login.x, self.input_rect_login.y - 50))
        label_surface2 = self.font_label.render("Hasło:", True, (0, 0, 0))
        self.screen.blit(label_surface2, (self.input_rect_login.x, self.input_rect_login.y + 78))

        text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_rect_login.x + 5, self.input_rect_login.y + 5))

        masked_password = '*' * len(self.password_text)
        text_surface2 = self.base_font.render(masked_password, True, (0, 0, 0))
        self.screen.blit(text_surface2, (self.input_rect_password.x + 5, self.input_rect_password.y + 5))

    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def use_draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # Draw title
        self.draw_text(self.title_text, self.font_title, text_color, self.title_text_x, 50)

        # rysowanie przycisku wyjścia
        self.exit_button.draw(self.screen)
        if self.exit_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.exit_button.color = self.exit_button_hover_color
        else:
            self.exit_button.color = self.exit_button_color

        # rysowanie przycisku menu
        self.menu_button.draw(self.screen)
        if self.menu_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.menu_button.color = self.menu_button_hover_color
        else:
            self.menu_button.color = self.menu_button_color

        self.draw_input_login()
        self.draw_login_button()

        self.draw_text(self.info_message, self.base_font, text_color, 100, 500)

        pygame.display.flip()
        self.clock.tick(60)

        # Rysowanie tytułu

    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

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

    def handle_text_input(self, event):
        if self.active_login:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else:
                self.user_text += event.unicode
        elif self.active_password:
            if event.key == pygame.K_BACKSPACE:
                self.password_text = self.password_text[:-1]
            else:
                self.password_text += event.unicode

    def draw_login_button(self):
        self.login_button.draw(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        is_button_pressed = pygame.mouse.get_pressed()[0]

        if self.login_button.isOver(mouse_pos):
            pygame.draw.rect(self.screen, (0, 0, 0), self.button_back, 0)
            self.login_button_color = self.login_button_hover_color

            self.login_button.draw(self.screen)
        else:
            self.login_button_color = (37,38,37)

        if self.login_button.but_rect.collidepoint(mouse_pos) and is_button_pressed and not self.prev_button_state:
            print("sukces")
            # self.login_user()  # Wywołuje funkcję logowania użytkownika
        else:
            self.login_button.color = self.login_button_color


    def login_user(self):
        # Sprawdź, czy użytkownik o podanym loginie i haśle istnieje w bazie danych
        dbcursor.execute("SELECT * FROM player WHERE login=? AND password=?", (self.user_text, self.password_text))
        existing_user = dbcursor.fetchone()
        if existing_user is not None:
            self.info_message = "Zalogowano"

        else:
            self.info_message = "Błąd logowania"

