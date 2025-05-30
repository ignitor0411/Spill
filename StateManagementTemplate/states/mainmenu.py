import pygame
import pygame.freetype
from states.state import State
from states.etkultspill import EtKultSpill

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def update(self, actions, dt):
        if actions["1"].pressed:
            self.game.state = EtKultSpill(self.game)
            actions["1"].pressed = False

    def render(self, display):
        display.fill("black")

        self.draw_text(display, "Trykk 1 for å spille Et Kult Spill", (255, 255, 255), (display.get_width() // 2, display.get_height() // 2))
