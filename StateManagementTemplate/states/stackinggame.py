import pygame
from states.state import State

class StackingGame(State):
    WIDTH = 500
    HEIGHT = 500
    BLOCK_HEIGHT = 30
    BLOCK_SPEED = 4

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("comic sans", 36)
        self.reset()

    def reset(self):
        self.blocks = []
        self.current_x = 0
        self.current_width = 200
        self.current_y = self.HEIGHT - self.BLOCK_HEIGHT
        self.direction = 1
        self.score = 0
        self.is_game_over = False
        # Add the first block (base)
        self.blocks.append(pygame.Rect(
            (self.WIDTH - self.current_width) // 2,
            self.current_y,
            self.current_width,
            self.BLOCK_HEIGHT
        ))
        self.current_y -= self.BLOCK_HEIGHT

    def update(self, actions, dt):
        if self.is_game_over:
            if actions["action"].pressed:
                self.reset()
            actions["action"].pressed = False
            return

        # Move current block
        self.current_x += self.direction * self.BLOCK_SPEED
        if self.current_x < 0 or self.current_x + self.current_width > self.WIDTH:
            self.direction *= -1

        if actions["action"].pressed:
            # Place the block
            prev_block = self.blocks[-1]
            new_block = pygame.Rect(self.current_x, self.current_y, self.current_width, self.BLOCK_HEIGHT)
            overlap_left = max(prev_block.left, new_block.left)
            overlap_right = min(prev_block.right, new_block.right)
            overlap_width = overlap_right - overlap_left

            if overlap_width <= 0:
                self.is_game_over = True
            else:
                # Cut the block to the overlap
                self.current_width = overlap_width
                self.current_x = overlap_left
                self.blocks.append(pygame.Rect(self.current_x, self.current_y, self.current_width, self.BLOCK_HEIGHT))
                self.score += 1
                self.current_y -= self.BLOCK_HEIGHT
                # Reset for next block
                self.current_x = 0
                self.direction = 1

        actions["action"].pressed = False

    def get_camera_offset(self):
        # Find the y of the top block (smallest y)
        if self.blocks:
            top_y = min(block.top for block in self.blocks)
        else:
            top_y = self.current_y
        # Offset so top block is always at e.g. 60px from the top
        return max(0, 60 - top_y)

    def render(self, display):
        display.fill((30, 30, 30))
        camera_offset = self.get_camera_offset()
        # Draw stacked blocks
        for block in self.blocks:
            draw_rect = block.move(0, camera_offset)
            pygame.draw.rect(display, (0, 200, 255), draw_rect)
        # Draw moving block if not game over
        if not self.is_game_over:
            moving_rect = pygame.Rect(self.current_x, self.current_y, self.current_width, self.BLOCK_HEIGHT)
            moving_rect = moving_rect.move(0, camera_offset)
            pygame.draw.rect(display, (255, 200, 0), moving_rect)
        # Draw score
        score_surf = self.font.render(f"Score: {self.score}", True, (255,255,255))
        display.blit(score_surf, (10, 10))
        # Game over message
        if self.is_game_over:
            over_surf = self.font.render("Game Over! SPACE to restart", True, (255,0,0))
            display.blit(over_surf, (30, 220))