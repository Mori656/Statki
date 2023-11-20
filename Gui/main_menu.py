import pygame
# import Pygame_Util as pu
from pygame import mixer

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
class main_menu():
    def __init__(self,s):
        self.screen = s
        # pygame.mixer.init()
        # # mixer.music.load('startButton.mp3')
        # mixer.music.set_volume(0.25)

        # Screen settings

        # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


        # Colors
        self.background_color = (200, 232, 232)
        self.button_color = (38, 38, 37)
        self.button_text_color = (255, 255, 255)
        self.menu_lettering = (19, 38, 87)

        # Fonts
        self.title_font_size = 80
        self.button_font_size = 40
        self.title_font = pygame.font.SysFont("Comics Sans", self.title_font_size, bold=True)
        self.font = pygame.font.SysFont("Comics Sans", self.button_font_size, bold=False)

        # Menu buttons
        self.menu_buttons = [
            {"text": "Rozpocznij Grę", "function": "start_game"},
            {"text": "Opcje", "function": "options"},
            {"text": "Tablica Wyników", "function": "scoreboard"},
            {"text": "Opuść grę", "function": "quit_game"}
        ]

        # Function to draw the game interface
    def draw_main_menu(self):
        self.screen.fill(self.background_color)

        # Draw title
        title_text = pygame.font.SysFont("Arial", self.title_font_size, bold=True)
        title_text = title_text.render("Gra w statki", 1, self.menu_lettering)
        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        title_y = 50  # Adjust the vertical position of the title
        self.screen.blit(title_text, (title_x, title_y))

        # Draw buttons
        button_height = 100
        button_spacing = 40
        total_button_height = (button_height + button_spacing) * len(self.menu_buttons)
        button_y = (SCREEN_HEIGHT - total_button_height) // 2

        for i, button in enumerate(self.menu_buttons):
            button_text = self.font.render(button["text"], 1, self.button_text_color)
            button_width = 300
            button_x = (SCREEN_WIDTH - button_width) // 2

            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # Check if the mouse is over the button
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen,(0, 0, 0), pygame.Rect(button_x-5,button_y-5,button_width+10, button_height+10))
                pygame.draw.rect(self.screen, (100, 50, 50), button_rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, button_rect)

            text_x = button_rect.centerx - button_text.get_width() // 2
            text_y = button_rect.centery - button_text.get_height() // 2

            self.screen.blit(button_text, (text_x, text_y))

            button_y += button_height + button_spacing

        # Function to start a new game
    def start_game(self):
        # Call the code from the previous program, e.g., the function draw_boards()
        #draw_boards()
        mixer.music.play()
        pygame.time.delay(1200)
        pygame.quit()
            

        # Function to display options
    def options(self):
        # Call the code from the previous program, e.g., the function Custom_page_draw()
        #Custom_page_draw()
        mixer.music.play()
        pygame.time.delay(1200)
        pygame.quit()

        # Function to quit the game
    def quit_game(self):
        mixer.music.play()
        pygame.time.delay(1200)
        pygame.quit()

    def scoreboard(self):
        mixer.music.play()
        pygame.time.delay(1200)
        pygame.quit()
        quit()
    
    def use_draw(self):
        self.draw_main_menu()

    def use_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, button in enumerate(self.menu_buttons):
                        button_width = self.font.render(button["text"], 1, self.button_text_color).get_width() + 20
                        button_height = 100
                        button_spacing = 40
                        button_x = (SCREEN_WIDTH - button_width) // 2
                        button_y = (SCREEN_HEIGHT - ((button_height + button_spacing) * len(self.menu_buttons))) // 2 + (
                                i * (button_height + button_spacing))

                        if button_x < event.pos[0] < button_x + button_width and \
                                button_y < event.pos[1] < button_y + button_height:
                            if button["function"] == "start_game":
                                self.start_game()
                            elif button["function"] == "options":
                                self.options()
                            elif button["function"] == "scoreboard":
                                self.scoreboard()
                            elif button["function"] == "quit_game":
                                self.quit_game()

        
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



