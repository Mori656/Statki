import pygame
from pygame import mixer

pygame.mixer.init()

class button():
    def __init__(self, color, x, y, width, height, text="", text_color = (0,0,0), font=None, size=60, bold = False, outline=0):
        self.color = color                              # kolor przycisku
        self.x = x                                      # x pos
        self.y = y                                      # y pos
        self.width = width                              # szerokość przycisku
        self.height = height                            # wysokość przycisku
        self.text = text                                # teskt na przycisku
        self.text_color = text_color                    # kolor tekstu
        self.size = size                                # wielkość tekstu
        self.bold = bold                                # pogrubienie
        self.outline = outline                          # szerokość obramowania
        self.font = pygame.font.SysFont(font, size ,bold)  # rodzaj czcionki

        self.but_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    #Draws the button, outline may be provided
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.but_rect, self.outline)

        if self.text != "":
            text = self.font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    #Returns true if the given pos (either tuple or list) is over the button
    def isOver(self, pos):
            return (pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height)


class checkbox():
    def __init__(self, color , x, y, width, height, backgroundcolor = (255,255,255), checkcolor = (255,0,0), outline=1, check=False, text="", size=60, font=None, textGap = 10):
        self.x = x                                       # x pos
        self.y = y                                       # y pos
        self.width = width                               # szerokość
        self.height = height                             # wysokość
        self.outline = outline                           # grubośc obramowania
        self.color = color                               # color obramowania
        self.check = check                               # zmienna "czy zaznaczone"
        self.backgroundcolor = backgroundcolor           # kolor tła niezaznaczone
        self.checkcolor = checkcolor                     # kolor tła zaznaczone
        self.text = text                                 # tekst
        self.font = pygame.font.SysFont(font, size)      # rodzaj czcionki
        self.size = size                                 # rozmair tekstu
        self.textGap = textGap                           # odległość tekstu od obramowania

        self.check_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    #Draws the checkbox
    def draw(self, win):
        but = button(self.color, self.x, self.y, self.width, self.height, outline=self.outline)
        but.draw(win)

        if self.text != "":
            text = self.font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + self.width+self.textGap, self.y + (self.height/2 - text.get_height()/2)))

        if self.check:
            # pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x + self.width - self.outline, self.y + self.height - self.outline))
            # pygame.draw.line(win, (0, 0, 0), (self.x - self.outline + self.width, self.y), (self.x, self.y + self.height - self.outline))
            pygame.draw.rect(win, self.checkcolor, (self.x + self.outline, self.y + self.outline, self.width - self.outline*2, self.height - self.outline*2))
        else:
            pygame.draw.rect(win, self.backgroundcolor, (self.x + self.outline, self.y + self.outline, self.width - self.outline*2, self.height - self.outline*2))

    #Returns true if the given pos (either tuple or list) is over the box
    def isOver(self, pos):
        return (pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height)
        
    #Returns wether the box is checked or not
    def isChecked(self):
        return self.check

    #Checks or unchecks the box
    def convert(self, win):
        self.check = not self.check
        self.draw(win)

class slider():
    def __init__(self, color , x, y, width, height, value = 0.0, min = 0.0, max = 100.0, backgroundcolor = (255,255,255), outline=0):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min = min
        self.max = max
        
        self.backgroundcolor = backgroundcolor
        self.outline = outline

        self.value = self.width * ((value/ self.max - self.min) + self.min)
        self.conteiner_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pygame.Rect(self.x + self.value - (self.height/2), self.y, self.height, self.height)
        
    def move_slider(self, mpos):
        self.button_rect.centerx = mpos[0]
        self.value = (self.button_rect.centerx - self.x) + 1
        
    #draw a slider    
    def draw(self, win):
        pygame.draw.rect(win, self.backgroundcolor, (self.x,self.y,self.width,self.height))
        pygame.draw.rect(win, self.color,  self.button_rect)
    #sprawdzanie kolizji
    def isOver(self, pos):
        return (pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height)
    #zwraca value
    def get_value(self):
        return (self.value/self.width - self.min) * (self.max - self.min)
    def newButPos(self,val):
        self.value = self.width * ((val/ self.max - self.min) + self.min)
        self.button_rect = pygame.Rect(self.x + self.value - (self.height/2), self.y, self.height, self.height)

class Statek:
    def __init__(self, width, location, direction):
        """
        Inicjalizacja obiektu Statek.

        :param dlugosc: Długość statku (ilość pól, jakie zajmuje na planszy).
        :param polozenie: Tuple (x, y) reprezentujące początkowe pole statku na planszy.
        :param kierunek: 'poziomo' lub 'pionowo', określa kierunek, w którym jest ustawiony statek.
        """
        self.width = width
        self.location = location
        self.direction = direction
        self.shoot_location = set()  # Zbiór pól, które zostały trafione

    def location(self):
        """
        Zwraca zbiór pól zajmowanych przez statek na planszy.
        """
        fields = set()
        x, y = self.location

        for i in range(self.width):
            if self.direction == 'poziomo':
                fields.add((x + i, y))
            elif self.direction == 'pionowo':
                fields.add((x, y + i))

        return fields

    def shot(self, pole):
        """
        Oznacz pole jako trafione przez statek.

        :param pole: Tuple (x, y) reprezentujące pole, które zostało trafione.
        """
        self.shoot_location.add(pole)

    def hadItDrown(self):
        """
        Sprawdza, czy statek został zatopiony (wszystkie jego części zostały trafione).
        """
        return len(self.shoot_location) == self.width


# Przykład użycia:
# statek = Statek(dlugosc=3, polozenie=(2, 3), kierunek='poziomo')
# print(statek.zajmowane_pola())  # Zwróci {(2, 3), (3, 3), (4, 3)}
# statek.trafienie((3, 3))
# print(statek.czy_zatopiony())  # Zwróci False
# statek.trafienie((2, 3))
# statek.trafienie((4, 3))
# print(statek.czy_zatopiony())  # Zwróci True
