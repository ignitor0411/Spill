import pygame
import pygame.freetype
from states.state import State
from states.etkultspill import EtKultSpill
from states.mrpresident import MrPresident
# Importer flere states her etter hvert som du lager dem
# from states.annenstate import AnnenState

class Button:
    def __init__(self, rect, text, font, text_color=(255,255,255), color=(130,0,130), hover_color=(100,0,100)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        # Tegn knapp
        pygame.draw.rect(surface, self.hover_color if is_hover else self.color, self.rect)
        # Tegn hvit ramme
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.bg = pygame.image.load("StateManagementTemplate/assets/MainMenu_bg.png")
        self.bg = pygame.transform.scale(self.bg, (self.game.screen.get_width(), self.game.screen.get_height()))
        self.states = [
            ("EtKultSpill", EtKultSpill), 
            # ("Annen State", AnnenState),
        ]
        self.buttons = []
        button_width = 250
        button_height = 60
        spacing = 20
        start_y = 120
        for i, (name, _) in enumerate(self.states):
            rect = (
                (self.game.screen.get_width() - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.buttons.append(Button(rect, f"Start {name}", self.game.font))
        self.selected_index = 0  # Hvilken knapp som er valgt med piltaster

    def update(self, actions, dt):
        # PILTASTER: Oppdater valgt knapp
        if actions["down"].pressed:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        if actions["up"].pressed:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        # ENTER: Velg valgt knapp
        if actions["return"].pressed:
            self.game.state = self.states[self.selected_index][1](self.game)

        # MUSEKLIKK: Sjekk om noen knapp er klikket
        for i, button in enumerate(self.buttons):
            if actions["leftmouse"].pressed and button.is_hovered():
                self.game.state = self.states[i][1](self.game)
                break

        # Hvis musen er over en knapp, marker den som valgt (men ikke hvis du nettopp brukte piltast)
        mouse_over = False
        for i, button in enumerate(self.buttons):
            if button.is_hovered():
                self.selected_index = i
                mouse_over = True
                break

        # Nullstill pressed-flagg
        actions["leftmouse"].pressed = False
        actions["up"].pressed = False
        actions["down"].pressed = False
        actions["return"].pressed = False

    def render(self, display):
        self.game.screen.blit(self.bg, (0, 0))
        for i, button in enumerate(self.buttons):
            # Tegn ekstra ramme rundt valgt knapp
            if i == self.selected_index:
                pygame.draw.rect(display, (255,255,0), button.rect.inflate(8,8), 4)  # Gul ramme
            button.draw(display)
