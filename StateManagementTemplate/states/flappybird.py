import pygame
import random
import json
import os
from states.state import State

class FlappyBird(State):
    PIPE_WIDTH = 60
    PIPE_GAP = 150
    PIPE_SPEED = 3
    PIPE_INTERVAL = 1500

    def __init__(self, game):
        super().__init__(game)
        self.bird_y = 250
        self.bird_velocity = 0
        self.gravity = 0.4
        self.jump_strength = -8
        self.bird_radius = 20

        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()
        self.score = 0
        self.highscore = self.load_highscore()
        self.font = pygame.font.SysFont("comic sans", 36)
        self.is_game_over = False

    def reset(self):
        self.bird_y = 250
        self.bird_velocity = 0
        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()
        self.score = 0
        self.is_game_over = False

    def load_highscore(self):
        path = "StateManagementTemplate/save_file/flappybird_highscore.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f).get("highscore", 0)
        return 0

    def save_highscore(self):
        path = "StateManagementTemplate/save_file/flappybird_highscore.json"
        with open(path, "w") as f:
            json.dump({"highscore": self.highscore}, f)

    def spawn_pipe(self):
        height = random.randint(60, 350)
        top_rect = pygame.Rect(500, 0, self.PIPE_WIDTH, height)
        bottom_rect = pygame.Rect(500, height + self.PIPE_GAP, self.PIPE_WIDTH, 500 - (height + self.PIPE_GAP))
        self.pipes.append({"top": top_rect, "bottom": bottom_rect, "passed": False})

    def update(self, actions, dt):
        if self.is_game_over:
            if actions["action"].pressed:
                self.reset()
            actions["action"].pressed = False
            return

        if actions["action"].pressed:
            self.bird_velocity = self.jump_strength

        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        if self.bird_y > 480:
            self.bird_y = 480
            self.bird_velocity = 0
            self.is_game_over = True
        if self.bird_y < 0:
            self.bird_y = 0
            self.bird_velocity = 0

        now = pygame.time.get_ticks()
        if now - self.last_pipe_time > self.PIPE_INTERVAL:
            self.spawn_pipe()
            self.last_pipe_time = now

        for pipe in self.pipes:
            pipe["top"].x -= self.PIPE_SPEED
            pipe["bottom"].x -= self.PIPE_SPEED

        self.pipes = [p for p in self.pipes if p["top"].x + self.PIPE_WIDTH > 0]

        bird_rect = pygame.Rect(100 - self.bird_radius, int(self.bird_y) - self.bird_radius, self.bird_radius*2, self.bird_radius*2)

        for pipe in self.pipes:
            if pipe["top"].colliderect(bird_rect) or pipe["bottom"].colliderect(bird_rect):
                self.is_game_over = True

            # Score
            if not pipe["passed"] and pipe["top"].x + self.PIPE_WIDTH < 100:
                pipe["passed"] = True
                self.score += 1
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.save_highscore()

        actions["action"].pressed = False

    def render(self, display):
        display.fill((135, 206, 235))
        for pipe in self.pipes:
            pygame.draw.rect(display, (0, 200, 0), pipe["top"])
            pygame.draw.rect(display, (0, 200, 0), pipe["bottom"])
        pygame.draw.circle(display, (255, 255, 0), (100, int(self.bird_y)), self.bird_radius)

        score_surf = self.font.render(f"Score: {self.score}", True, (0,0,0))
        hs_surf = self.font.render(f"Highscore: {self.highscore}", True, (0,0,0))
        display.blit(score_surf, (10, 10))
        display.blit(hs_surf, (10, 40))

        if self.is_game_over:
            over_surf = self.font.render("Game Over! Press SPACE to restart.", True, (255,0,0))
            display.blit(over_surf, (50, 220))