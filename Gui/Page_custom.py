import Gui.Pygame_Util as pu
import pygame
from pygame import mixer
import tkinter as tk

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()
pygame.font.init()

class page_custom():
    def __init__(self,s):
        self.screen = s
        self.volume = 0.05

        # pygame.mixer.init()
        # mixer.music.load('background.mp3')
        # mixer.music.play(-1)
        # mixer.music.set_volume(self.volume)
        #self.volume sliders
        self.fontcolor = (19, 38, 87)
        self.slidersWidth = 600
        self.slidersHeight = 40
        self.volumeMusic = 0.20
        self.volumeMusicSlider = pu.slider((255,125,0),(SCREEN_WIDTH - self.slidersWidth) / 2,SCREEN_HEIGHT - 300,self.slidersWidth,self.slidersHeight,self.volumeMusic,0,1)
        self.volumeEffects = 0.20
        self.volumeEffectsSlider = pu.slider((255,125,0),(SCREEN_WIDTH - self.slidersWidth) / 2,SCREEN_HEIGHT - 200,self.slidersWidth,self.slidersHeight,self.volumeEffects,0,1)

        self.background_colour = (200, 232, 232)
        self.screen = pygame.display.set_mode((1920, 1080)) 
        self.screen.fill(self.background_colour) 

        # Tab declaration
        self.BoardSize = []
        self.Ships = [[],[],[],[]]

        # Inicjalizacja przycisku wyjścia
        self.exit_button_width = 150
        self.exit_button_height = 50
        self.exit_button_x = SCREEN_WIDTH - self.exit_button_width - 10
        self.exit_button_y = 10
        self.exit_button_rect = pygame.Rect((self.exit_button_x, self.exit_button_y, self.exit_button_width, self.exit_button_height))
        self.exit_button_color = (255, 0, 0)
        self.exit_button_hover_color = (200, 0, 0)
        self.exit_button_font_size = 30
        self.exit_button_font = pygame.font.SysFont("monospace", self.exit_button_font_size, bold=True)
        self.exit_button_text = self.exit_button_font.render("Wyjście", 1, (255, 255, 255))
        # exit_sound = pygame.mixer.Sound('button.mp3')

        # Add the Settings button
        self.settings_button_width = 160
        self.settings_button_height = 50
        self.settings_button_x = SCREEN_WIDTH - self.settings_button_width - 200
        self.settings_button_y = 10  # Adjust the vertical position
        self.settings_button_rect = pygame.Rect((self.settings_button_x, self.settings_button_y, self.settings_button_width, self.settings_button_height))
        self.settings_button_color = (128,128,128)  # Green button color
        self.settings_button_hover_color = (128,128,200)  # Green hover color
        self.settings_button_font_size = 30
        self.settings_button_font = pygame.font.SysFont("monospace", self.settings_button_font_size, bold=True)
        self.settings_button_text = self.settings_button_font.render("Głośność", 1, (255, 255, 255))

    def Custom_page_draw(self):

        self.screen.fill((200, 232, 232))
        self.fonth1 = pygame.font.SysFont("arial.ttf", 70)
        self.fonth2 = pygame.font.SysFont("arial.ttf", 50)
        # fonth3 = pygame.font.SysFont("arial.ttf", 20)
        text = self.fonth1.render("Rozmiar planszy", False, (0,0,0))
        self.screen.blit(text, (100,50))

        #Ability overlay
        text = self.fonth1.render("Umiejętności specjalne", False, (0,0,0))
        self.screen.blit(text, (1200,100))
        text = self.fonth2.render("Zostaną dodane wkrótce!", False, (0,0,0))
        self.screen.blit(text, (1250,200))

        #sliders text
        deafoult_text_font = pygame.font.SysFont("Comics Sans", 50)
        text = deafoult_text_font.render("Głośność muzyki: " + f"{self.volumeMusic:.2f}" , False, self.fontcolor)
        self.screen.blit(text, (1200,SCREEN_HEIGHT - 350))


        text = deafoult_text_font.render("Głośność efektów: "+ f"{self.volumeEffects:.2f}" , False, self.fontcolor)
        self.screen.blit(text, (1200,SCREEN_HEIGHT - 250))


        #Board Button overlay 
        for x in range(0,4):
            self.BoardSize.append((pu.checkbox((110,0,0), 115 + (x*200), 120, 30, 30)))
            self.BoardSize[x].draw(self.screen)

        # but_tab.append(BoardSize1)


        #Board Text overlay 
        text = self.fonth2.render("9x9", False, (0,0,0))
        self.screen.blit(text, (100,150))
        text = self.fonth2.render("10x10", False, (0,0,0))
        self.screen.blit(text, (280,150))
        text = self.fonth2.render("11x11", False, (0,0,0))
        self.screen.blit(text, (485,150))
        text = self.fonth2.render("12x12", False, (0,0,0))
        self.screen.blit(text, (680,150))

        #self.Ships Text overlay

        text = self.fonth1.render("Statki", False, (0,0,0))
        self.screen.blit(text, (100,250))

        text = self.fonth2.render("Liczba statków o wielkości 1", False, (0,0,0))
        self.screen.blit(text, (130,320))
        text = self.fonth2.render("Liczba statków o wielkości 2", False, (0,0,0))
        self.screen.blit(text, (130,470))
        text = self.fonth2.render("Liczba statków o wielkości 3", False, (0,0,0))
        self.screen.blit(text, (130,620))
        text = self.fonth2.render("Liczba statków o wielkości 4", False, (0,0,0))
        self.screen.blit(text, (130,770))


        for j in range (0,4):
            for i in range (0,9):
                text = self.fonth2.render(str(i), False, (0,0,0))
                self.screen.blit(text, (135+(i*100),410+(j*150)))
        #self.Ships Button overlay 
                self.Ships[j].append((pu.checkbox((0,0,0), 130+(i*100), 380+(j*150), 30, 30)))
                self.Ships[j][i].draw(self.screen)


        # Update the display using flip 
        pygame.display.flip()

    def use_draw(self):
        self.Custom_page_draw()

        # while running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #             running = False
        #         if event.type == pygame.MOUSEBUTTONUP:
        #             # Sprawdź przyciski na planszy i statki
        #             for b in self.BoardSize:
        #                 if b.isOver(pygame.mouse.get_pos()):
        #                     for p in self.BoardSize:
        #                         if p.isChecked():
        #                             p.convert(self.screen)
        #                     b.convert(self.screen)
        #                     pygame.display.flip()
        #             for s in self.Ships:
        #                 for z in s:
        #                     if z.isOver(pygame.mouse.get_pos()):
        #                         for d in s:
        #                             if d.isChecked():
        #                                 d.convert(self.screen)
        #                         z.convert(self.screen)
        #                         pygame.display.flip()
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if self.settings_button_rect.collidepoint(event.pos):
        #                 self.show_volume_settings()
        #             elif self.exit_button_rect.collidepoint(event.pos):
        #                 mixer.music.stop()
        #                 self.exit_sound.play()
        #                 pygame.time.delay(3000)
        #                 running = False

        #     # Rysuj przyciski i tekst na ekranie
        #     pygame.draw.rect(self.screen, self.exit_button_color if not self.exit_button_rect.collidepoint(
        #         pygame.mouse.get_pos()) else self.exit_button_hover_color, self.exit_button_rect)
        #     pygame.draw.rect(self.screen, self.settings_button_color if not self.settings_button_rect.collidepoint(
        #         pygame.mouse.get_pos()) else self.settings_button_hover_color, self.settings_button_rect)

        #     # Tekst na przyciskach
        #     self.screen.blit(self.settings_button_text, (self.settings_button_x + 10, self.settings_button_y + 10))
        #     self.screen.blit(self.exit_button_text, (self.exit_button_x + 10, self.exit_button_y + 10))

            # pygame.display.update()

        # Zakończenie gry
        # pygame.quit()
