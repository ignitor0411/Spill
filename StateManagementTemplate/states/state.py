import pygame


class State:
    def __init__(self, game):
        self.game = game

    def draw_text(self, surface, string : str, color : pygame.Color, center : tuple):
        text_surf = self.game.font.render(string, False, (255, 255, 255)) # Tekst
        text_rect = text_surf.get_rect(center=center) # Sentrer
        self.game.screen.blit(text_surf, text_rect)

    def update(self, actions, dt):
        pass

    def render(self, display):
        pass
