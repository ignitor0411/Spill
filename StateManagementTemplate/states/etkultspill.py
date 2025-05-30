import pygame
from states.state import State

class EtKultSpill(State):
    def __init__(self, game):
        self.game = game

    def update(self, actions, dt):
        # Tilbake til main menu
        if actions["escape"].pressed:
            self.game.state = self.game.main_menu
            actions["escape"].pressed = False

    def render(self, display):
        display.fill((0, 0, 0))
        self.draw_text(display, "Wow! Sykt kult spil! (trykk ESC for å gå tilbake)", (123, 4, 20), (self.game.screen.get_width() // 2, 20))