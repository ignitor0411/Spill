import pygame
import pygame.freetype
from states.state import State
from states.etkultspill import EtKultSpill
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
        self.bg = pygame.image.load("StateManagementTemplate/assets/MainMenu_bg.png")  # Last inn bakgrunnsbilde
        self.bg = pygame.transform.scale(self.bg, (self.game.screen.get_width(), self.game.screen.get_height()))
        # Legg til alle states du vil ha knapper for her
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

    def update(self, actions, dt):
        for i, button in enumerate(self.buttons):
            if actions["leftmouse"].pressed and button.is_hovered():
                # Bytt til valgt state
                self.game.state = self.states[i][1](self.game)
        actions["leftmouse"].pressed = False

    def render(self, display):
        self.game.screen.blit(self.bg, (0, 0))  # Tegn bakgrunnsbilde på skjermen
        for button in self.buttons:
            button.draw(display)
