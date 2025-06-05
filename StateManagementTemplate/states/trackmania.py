import pygame
import math
pygame.init()

DISPLAY_W, DISPLAY_H = 500, 500
MAP_W, MAP_H = 1500, 1500  # Make the map much larger

class Car:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 0
        self.angle = 0
        self.drift_angle = 0
        self.drifting = False  # Add drifting state
        self.image_orig = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("StateManagementTemplate/Assets/trackmania/car.png").convert_alpha(),
                (width, height)
            ),
            -90  # Rotate 90 degrees to the right
        )
        self.image = self.image_orig

    def update(self, dt, keys):
        ACCEL = 0.3
        FRICTION = 0.04
        TURN_SPEED = 3
        DRIFT_FACTOR = 0.25  # Increase for more visible drift

        # Check if drifting (space bar)
        self.drifting = keys[pygame.K_SPACE]

        # Accelerate/Brake
        if keys[pygame.K_UP]:
            self.speed += ACCEL
        elif keys[pygame.K_DOWN]:
            self.speed -= ACCEL * 0.7
        else:
            # Friction
            if self.speed > 0:
                self.speed -= FRICTION
            elif self.speed < 0:
                self.speed += FRICTION

        self.speed = max(-6, min(10, self.speed))

        # Drifting
        if self.drifting and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and abs(self.speed) > 2:
            drift_direction = 1 if keys[pygame.K_LEFT] else -1
            # Increase drift angle more for visible effect
            self.drift_angle += drift_direction * TURN_SPEED * DRIFT_FACTOR * (abs(self.speed) / 6)
            # Limit drift angle
            self.drift_angle = max(-30, min(30, self.drift_angle))
            # Less direct steering while drifting
            self.angle += drift_direction * TURN_SPEED * (self.speed / 10) * 0.2
        else:
            # Gradually return drift angle to zero
            if self.drift_angle > 0:
                self.drift_angle -= TURN_SPEED * DRIFT_FACTOR
                if self.drift_angle < 0:
                    self.drift_angle = 0
            elif self.drift_angle < 0:
                self.drift_angle += TURN_SPEED * DRIFT_FACTOR
                if self.drift_angle > 0:
                    self.drift_angle = 0

        if not self.drifting:
            if keys[pygame.K_LEFT]:
                self.angle += TURN_SPEED * (self.speed / 10)
            if keys[pygame.K_RIGHT]:
                self.angle -= TURN_SPEED * (self.speed / 10)

        # Move car with drift
        move_angle = self.angle + self.drift_angle
        rad = math.radians(move_angle)
        self.x += -self.speed * math.sin(rad) * dt
        self.y += -self.speed * math.cos(rad) * dt

        # Boundaries (map size)
        if self.x < 0:
            self.x = 0
        elif self.x > MAP_W - self.width:
            self.x = MAP_W - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > MAP_H - self.height:
            self.y = MAP_H - self.height

    def render(self, screen, camera_x, camera_y):
        rotated = pygame.transform.rotate(self.image_orig, self.angle + self.drift_angle)
        rect = rotated.get_rect(center=(self.x - camera_x + self.width // 2, self.y - camera_y + self.height // 2))
        screen.blit(rotated, rect.topleft)

class Track:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = pygame.transform.scale(
            pygame.image.load("StateManagementTemplate/Assets/trackmania/track.png").convert_alpha(),
            (width, height)
        )

    def render(self, screen, camera_x, camera_y):
        screen.blit(self.map, (-camera_x, -camera_y))

    def update(self, dt):
        pass

# --- Main loop with camera ---
if __name__ == "__main__":
    screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    clock = pygame.time.Clock()
    car = Car(MAP_W // 2, MAP_H // 2, 80, 40)
    track = Track(MAP_W, MAP_H)
    running = True

    while running:
        dt = clock.tick(60) / 16  # Normalize dt for consistent speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        car.update(dt, keys)

        # Camera follows car, centered
        camera_x = int(car.x + car.width // 2 - DISPLAY_W // 2)
        camera_y = int(car.y + car.height // 2 - DISPLAY_H // 2)
        # Clamp camera to map bounds
        camera_x = max(0, min(camera_x, MAP_W - DISPLAY_W))
        camera_y = max(0, min(camera_y, MAP_H - DISPLAY_H))

        track.render(screen, camera_x, camera_y)
        car.render(screen, camera_x, camera_y)
        pygame.display.flip()

    pygame.quit()