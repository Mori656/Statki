import os

import Gui.Pygame_Util as pu
import pygame
import subprocess
from pygame import mixer
import tkinter as tk
import Gui.game_screen


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()
pygame.font.init()




class page_custom():
    def __init__(self, s, vol1, vol2):
        self.screen = s
        self.volume = 0.10

        self.fontcolor = (19, 38, 87)



        # Volume Sliders
        self.volumeMusic = vol1
        self.volumeEffects = vol2
        self.slidersWidth = 600
        self.slidersHeight = 40
        self.volumeMusicSlider = pu.slider((255,125,0),1100, SCREEN_HEIGHT - 300, self.slidersWidth, self.slidersHeight, self.volumeMusic, 0, 1)
        self.volumeEffectsSlider = pu.slider((255,125,0),1100, SCREEN_HEIGHT - 200, self.slidersWidth, self.slidersHeight, self.volumeEffects, 0, 1)

        # Background color
        self.background_colour = (200, 232, 232)

        # Tab declaration
        self.BoardSize = []
        self.Ships = [[],[],[],[]]



        # Przycisk graj
        self.play_button_color = (0, 200, 0)
        self.play_button_hover_color = (0, 150, 0)
        self.play_button = pu.button(self.play_button_color, SCREEN_WIDTH - 400, 10, 150, 50, "Graj", (0, 0, 0),"monospace", 30)

        # Inicjalizacja przycisku wyjścia
        self.exit_button_color = (200, 0, 0)
        self.exit_button_hover_color = (150, 0, 0)
        self.exit_button = pu.button(self.exit_button_color, SCREEN_WIDTH - 60, 10, 50, 50, "X", (0,0,0), "monospace", 30)

        # Menu button
        self.menu_button_color = (128, 128, 128)
        self.menu_button_hover_color = (128, 128, 200)
        self.menu_button = pu.button(self.menu_button_color, SCREEN_WIDTH - 220, 10, 150, 50, "Menu", (0,0,0), "monospace", 30)

        # Board tab
        for x in range(0,4):
            self.BoardSize.append((pu.checkbox((110,0,0), 115 + (x*200), 120, 30, 30)))

        # Checkbox tab
        for j in range(0,4):
            for i in range(0,9):
                self.Ships[j].append((pu.checkbox((0,0,0), 130+(i*100), 380+(j*150), 30, 30)))


    def Custom_page_draw(self):
        self.screen.fill(self.background_colour)
        self.fonth1 = pygame.font.SysFont("arial.ttf", 70)
        self.fonth2 = pygame.font.SysFont("arial.ttf", 50)

        text = self.fonth1.render("Rozmiar planszy", False, (0,0,0))
        self.screen.blit(text, (100,50))

        text = self.fonth1.render("Umiejętności specjalne", False, (0,0,0))
        self.screen.blit(text, (1200,100))

        text = self.fonth2.render("Zostaną dodane wkrótce!", False, (0,0,0))
        self.screen.blit(text, (1250,200))

        deafoult_text_font = pygame.font.SysFont("Comics Sans", 50)

        text = deafoult_text_font.render("Głośność muzyki: " + f"{self.volumeMusic:.2f}" , False, self.fontcolor)
        self.screen.blit(text, (1200, SCREEN_HEIGHT - 350))

        text = deafoult_text_font.render("Głośność efektów: "+ f"{self.volumeEffects:.2f}" , False, self.fontcolor)
        self.screen.blit(text, (1200, SCREEN_HEIGHT - 250))

        for x in range(0,4):
            self.BoardSize[x].draw(self.screen)

        text = self.fonth2.render("9x9", False, (0,0,0))
        self.screen.blit(text, (100, 150))

        text = self.fonth2.render("10x10", False, (0,0,0))
        self.screen.blit(text, (280, 150))

        text = self.fonth2.render("11x11", False, (0,0,0))
        self.screen.blit(text, (485, 150))

        text = self.fonth2.render("12x12", False, (0,0,0))
        self.screen.blit(text, (680, 150))

        text = self.fonth1.render("Statki", False, (0,0,0))
        self.screen.blit(text, (100, 250))

        text = self.fonth2.render("Liczba statków o wielkości 1", False, (0,0,0))
        self.screen.blit(text, (130, 320))

        text = self.fonth2.render("Liczba statków o wielkości 2", False, (0,0,0))
        self.screen.blit(text, (130, 470))

        text = self.fonth2.render("Liczba statków o wielkości 3", False, (0,0,0))
        self.screen.blit(text, (130, 620))

        text = self.fonth2.render("Liczba statków o wielkości 4", False, (0,0,0))
        self.screen.blit(text, (130, 770))

        # Checkbox tab
        checkbox_configuration = {
            '9x9': {4: 3, 3: 2, 2: 2, 1: 1},
            '10x10': {4: 4, 3: 3, 2: 2, 1: 1},
            '11x11': {4: 6, 3: 4, 2: 3, 1: 2},
            '12x12': {4: 6, 3: 5, 2: 4, 1: 3}
        }
        selected_board = None

        for j in range(4):
            for i in range(6):
                if not any(bs.isChecked() for bs in self.BoardSize):
                    self.Ships[j][i].draw(self.screen)
                else:
                    selected_board = None
                    if self.BoardSize[0].isChecked():
                        selected_board = '9x9'

                    elif self.BoardSize[1].isChecked():
                        selected_board = '10x10'

                    elif self.BoardSize[2].isChecked():
                        selected_board = '11x11'

                    elif self.BoardSize[3].isChecked():
                        selected_board = '12x12'


                    if selected_board:
                        clickable_count = checkbox_configuration[selected_board].get(4 - j, 0)
                        if i < clickable_count:
                            self.Ships[j][i].draw(self.screen)

        for i in range(4):
            text = self.fonth2.render(str(i + 1), False, (0,0,0))
            self.screen.blit(text, (135 + (i * 100), 770))

        for j in range(4):
            for i in range(checkbox_configuration[selected_board].get(4 - j, 0) if selected_board else 6):
                text = self.fonth2.render(str(i + 1), False, (0,0,0))
                self.screen.blit(text, (135 + (i * 100), 410 + (j * 150)))

        self.draw_exit_button()
        self.draw_menu_button()
        self.draw_play_button()

        self.volumeMusicSlider.newButPos(self.volumeMusic)
        self.volumeEffectsSlider.newButPos(self.volumeEffects)

        self.volumeMusicSlider.draw(self.screen)
        self.volumeEffectsSlider.draw(self.screen)
    def update_gameboard_file(self):
        selected_board = None
        if self.BoardSize[0].isChecked():
            selected_board = '9\n9'
        elif self.BoardSize[1].isChecked():
            selected_board = '10\n10'
        elif self.BoardSize[2].isChecked():
            selected_board = '11\n11'
        elif self.BoardSize[3].isChecked():
            selected_board = '12\n12'
        elif selected_board == None:
            selected_board = '10\n10'


        if selected_board:
            with open("Gui/gameboard.txt", "w") as file:
                file.write(f"{selected_board}\n")
    def update_ship_number_file(self):
        selected_number1 = None
        selected_number2 = None
        selected_number3 = None
        selected_number4 = None
        if self.Ships[0][0].isChecked():
            selected_number1 = '1'
        elif self.Ships[0][1].isChecked():
            selected_number1 = '2'
        elif self.Ships[0][2].isChecked():
            selected_number1 = '3'
        elif self.Ships[0][3].isChecked():
            selected_number1 = '4'
        elif self.Ships[0][4].isChecked():
            selected_number1 = '5'
        elif self.Ships[0][5].isChecked():
            selected_number1 = '6'
        elif self.Ships[0][6].isChecked():
            selected_number1 = '7'
        elif self.Ships[0][7].isChecked():
            selected_number1 = '8'
        elif self.Ships[0][8].isChecked():
            selected_number1 = '9'


        if self.Ships[1][0].isChecked():
            selected_number2 = '1'
        elif self.Ships[1][1].isChecked():
            selected_number2 = '2'
        elif self.Ships[1][2].isChecked():
            selected_number2 = '3'
        elif self.Ships[1][3].isChecked():
            selected_number2 = '4'
        elif self.Ships[1][4].isChecked():
            selected_number2 = '5'
        elif self.Ships[1][5].isChecked():
            selected_number2 = '6'
        elif self.Ships[1][6].isChecked():
            selected_number2 = '7'
        elif self.Ships[1][7].isChecked():
            selected_number2 = '8'
        elif self.Ships[1][8].isChecked():
            selected_number2 = '9'

        if self.Ships[2][0].isChecked():
            selected_number3 = '1'
        elif self.Ships[2][1].isChecked():
            selected_number3 = '2'
        elif self.Ships[2][2].isChecked():
            selected_number3 = '3'
        elif self.Ships[2][3].isChecked():
            selected_number3 = '4'
        elif self.Ships[2][4].isChecked():
            selected_number3 = '5'
        elif self.Ships[2][5].isChecked():
            selected_number3 = '6'
        elif self.Ships[2][6].isChecked():
            selected_number3 = '7'
        elif self.Ships[2][7].isChecked():
            selected_number3 = '8'
        elif self.Ships[2][8].isChecked():
            selected_number3 = '9'

        if self.Ships[3][0].isChecked():
            selected_number4 = '1'
        elif self.Ships[3][1].isChecked():
            selected_number4 = '2'
        elif self.Ships[3][2].isChecked():
            selected_number4 = '3'
        elif self.Ships[3][3].isChecked():
            selected_number4 = '4'
        elif self.Ships[3][4].isChecked():
            selected_number4 = '5'
        elif self.Ships[3][5].isChecked():
            selected_number4 = '6'
        elif self.Ships[3][6].isChecked():
            selected_number4 = '7'
        elif self.Ships[3][7].isChecked():
            selected_number4 = '8'
        elif self.Ships[3][8].isChecked():
            selected_number4 = '9'

        if selected_number1 or selected_number2 or selected_number3 or selected_number4:
            with open("Gui/ships.txt", "w") as file:
                file.write(f"{selected_number1}\n{selected_number2}\n{selected_number3}\n{selected_number4}")


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
    def draw_play_button(self):
        self.play_button.draw(self.screen)

        if self.play_button.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.play_button.color = self.play_button_hover_color
        else:
            self.play_button.color = self.play_button_color

    def load_slider_speaker(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            if len(lines) >= 2:
                self.volumeMusic = float(lines[0].strip())
                self.volumeEffects = float(lines[1].strip())
        except FileNotFoundError:
            print(f"Błąd: {filename} nie znaleziony.")
        except Exception as e:
            print(f"Błąd podczas wczytywania wartości z pliku {filename}: {e}")

    def save_slider_values_to_file(self, file_path, volume_music, volume_effects):
        with open(file_path, "w") as file:
            file.write(f"{volume_music:.2f}\n")
            file.write(f"{volume_effects:.2f}\n")


    def use_draw(self):
        self.volumeMusic = self.volumeMusicSlider.get_value()
        self.volumeEffects = self.volumeEffectsSlider.get_value()
        self.update_gameboard_file()
        self.update_ship_number_file()
        self.save_slider_values_to_file('Gui/sound.txt', self.volumeMusic, self.volumeEffects)
        self.Custom_page_draw()

