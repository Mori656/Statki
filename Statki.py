import pygame
from pygame import mixer
import Gui.game_screen as gs
import Gui.main_menu as mm
import Gui.Settings as st
import Gui.Page_custom as pc
import Gui.scoreboard as sb
import Gui.SetShips as ss

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# obiekty stron
game = gs.game_screen(screen)
menu = mm.main_menu(screen)
settings = st.settings(screen)
custom = pc.page_custom(screen)
scoreboard = sb.scoreboard(screen)
SetShips = ss.SetShips(screen)

run = True
choice = "main_menu"
while run:
    screen.fill((200, 232, 232))
    if choice == "main_menu":
        pygame.display.set_caption("Statki: Bitwa trwa")
        menu.use_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, button in enumerate(menu.menu_buttons):
                        button_width = menu.font.render(button["text"], 1, menu.button_text_color).get_width() + 20
                        button_height = 100
                        button_spacing = 40
                        button_x = (SCREEN_WIDTH - button_width) // 2
                        button_y = (SCREEN_HEIGHT - (
                                    (button_height + button_spacing) * len(menu.menu_buttons))) // 2 + (
                                           i * (button_height + button_spacing))

                        if button_x < event.pos[0] < button_x + button_width and \
                                button_y < event.pos[1] < button_y + button_height:
                            if button["function"] == "start_game":
                                choice = "setShips"
                            elif button["function"] == "options":
                                choice = "custom"
                            elif button["function"] == "scoreboard":
                                choice = "scoreboard"
                            elif button["function"] == "quit_game":
                                menu.quit_game()
        pygame.display.flip()
    if choice == "setShips":
        SetShips.use_draw()
        SetShips.check_confirm_button_click()
        if SetShips.confirm_button_clicked == True:
            choice="game_screen"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choice = "settings"
    if choice == "game_screen":
        game.use_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choice = "settings"
    if choice == "settings":
        settings.use_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
    if choice == "custom":
        custom.use_draw()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # Sprawdź przyciski na planszy i statki
                    for b in custom.BoardSize:
                        if b.isOver(pygame.mouse.get_pos()):
                            for p in custom.BoardSize:
                                if p.isChecked():
                                    p.convert(custom.screen)
                            b.convert(custom.screen)
                            pygame.display.flip()
                    for s in custom.Ships:
                        for z in s:
                            if z.isOver(pygame.mouse.get_pos()):
                                for d in s:
                                    if d.isChecked():
                                        d.convert(custom.screen)
                                z.convert(custom.screen)
                                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if custom.exit_button_rect.collidepoint(event.pos):
                        mixer.music.stop()
                        custom.exit_sound.play()
                        pygame.time.delay(3000)
                        run = False

            # Rysuj przyciski i tekst na ekranie
            pygame.draw.rect(custom.screen, custom.exit_button_color if not custom.exit_button_rect.collidepoint(
                pygame.mouse.get_pos()) else custom.exit_button_hover_color, custom.exit_button_rect)
            pygame.draw.rect(custom.screen,
                             custom.settings_button_color if not custom.settings_button_rect.collidepoint(
                                 pygame.mouse.get_pos()) else custom.settings_button_hover_color,
                             custom.settings_button_rect)

            # Tekst na przyciskach
            custom.screen.blit(custom.settings_button_text,
                               (custom.settings_button_x + 10, custom.settings_button_y + 10))
            custom.screen.blit(custom.exit_button_text, (custom.exit_button_x + 10, custom.exit_button_y + 10))
    if choice == "scoreboard":
        scoreboard.use_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if scoreboard.exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
    pygame.display.flip()

pygame.quit()