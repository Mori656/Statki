import pygame
from pygame import mixer 
import Gui.Pygame_Util as pu

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()

class settings():
    def __init__(self,s):
        self.screen = s

        self.background_colour = (200, 232, 232)
        self.fontcolor = (19, 38, 87)
        self.screen.fill(self.background_colour) 

        #volume sliders
        self.slidersWidth = 600
        self.slidersHeight = 40
        self.volumeMusic = 0.20
        self.volumeMusicSlider = pu.slider((255,125,0),(SCREEN_WIDTH - self.slidersWidth) / 2,SCREEN_HEIGHT - 300,self.slidersWidth,self.slidersHeight,self.volumeMusic,0,1)
        self.volumeEffects = 0.20
        self.volumeEffectsSlider = pu.slider((255,125,0),(SCREEN_WIDTH - self.slidersWidth) / 2,SCREEN_HEIGHT - 200,self.slidersWidth,self.slidersHeight,self.volumeEffects,0,1)

        # Dźwiek gry
        # pygame.mixer.init()
        # mixer.music.load('background.mp3')
        # mixer.music.play(-1)
        # mixer.music.set_volume(self.volumeMusic)

        # Przycisiki

            # Zawartość tekstowa przycisków 
        self.menu_buttons = [
            {"text": "Opuść grę", "function": "quit_game"},
            {"text": "Wróć do Menu", "function": "main_menu"},
            {"text": "Legenda", "function": "game_legend"},
            {"text": "Wzów grę", "function": "game"}
            
            
        ]
            # atrybuty przycisków
        self.button_color = (38, 38, 37)
        self.button_text_color = (255, 255, 255)
        self.button_font = "Comics Sans"
        self.buttons_width = 300
        self.buttons_height = 100
        self.buttons_font_size = 40
        self.buttons_x = (SCREEN_WIDTH-self.buttons_width)/2
        self.buttons_y = (SCREEN_HEIGHT - 370)
        self.buttons_spacing =self.buttons_height + 30



    def Draw_Settings(self):
        settings_title_font = pygame.font.SysFont("Comics Sans", 130)
        text = settings_title_font.render("Ustawienia", False, self.fontcolor)
        self.screen.blit(text, ((SCREEN_WIDTH-text.get_width())/2,50))
        
        #sliders text
        deafoult_text_font = pygame.font.SysFont("Comics Sans", 50)
        text = deafoult_text_font.render("Głośność muzyki: " + f"{self.volumeMusic:.2f}" , False, self.fontcolor)
        self.screen.blit(text, ((SCREEN_WIDTH-text.get_width())/2,SCREEN_HEIGHT - 350))


        text = deafoult_text_font.render("Głośność efektów: "+ f"{self.volumeEffects:.2f}" , False, self.fontcolor)
        self.screen.blit(text, ((SCREEN_WIDTH-text.get_width())/2,SCREEN_HEIGHT - 250))

        #buttons drawing
        a = 0
        for i in self.menu_buttons:
            a +=1
            but = pu.button(self.button_color,self.buttons_x,self.buttons_y - (a*self.buttons_spacing),self.buttons_width,self.buttons_height,
            i["text"], (255, 255, 255), self.button_font, self.buttons_font_size)
            #podświetlanie przycisku
            if but.but_rect.collidepoint(pygame.mouse.get_pos()):
                but.color = (100, 50, 50)
                pygame.draw.rect(self.screen,(0, 0, 0), pygame.Rect(self.buttons_x-5,self.buttons_y-5-(a*self.buttons_spacing),self.buttons_width+10, self.buttons_height+10))
                but.draw(self.screen)
            else:
                but.color = self.button_color
                but.draw(self.screen)

        #draw sliders
        self.volumeMusicSlider.draw(self.screen)
        self.volumeEffectsSlider.draw(self.screen)
        pygame.display.flip()

    def use_draw(self):
        self.Draw_Settings()



        # clock = pygame.time.Clock()
        # running = True


        # while running:
        #     screen.fill(self.background_colour) 
        #     Draw_Settings()
        #     # mouse = pygame.mouse.get_pressed
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #             running = False
        #     if pygame.mouse.get_pressed()[0] and self.volumeMusicSlider.conteiner_rect.collidepoint(pygame.mouse.get_pos()):
        #             self.volumeMusicSlider.move_slider(screen,pygame.mouse.get_pos())
        #             self.volumeMusicSlider.draw(screen)
        #             self.volumeMusic = self.volumeMusicSlider.get_value()
        #             mixer.music.set_volume(self.volumeMusic)
        #     if pygame.mouse.get_pressed()[0] and self.volumeEffectsSlider.conteiner_rect.collidepoint(pygame.mouse.get_pos()):
        #             self.volumeEffectsSlider.move_slider(screen,pygame.mouse.get_pos())
        #             self.volumeEffectsSlider.draw(screen)
        #             self.volumeEffects = self.volumeEffectsSlider.get_value()
        #     pygame.display.update()
        # pygame.quit()