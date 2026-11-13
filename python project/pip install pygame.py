import random
import sys
import pygame

# pip install pygame

pygame.init()
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)
big_font = pygame.font.SysFont("arial", 48, bold=True)

# Colors
BG = (255, 247, 230)
BASKET_COLOR = (139, 90, 43)
TEXT = (43, 43, 43)
RED = (220, 40, 40)
FRUIT_COLORS = [(220, 40, 40), (255, 165, 0), (150, 60, 200), (255, 220, 40), (60, 180, 75)]


class Basket:
    def __init__(self):
        self.w, self.h = 90, 30
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 60
        self.speed = 8

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        # Mouse control
        if pygame.mouse.get_focused() and pygame.mouse.get_rel()[0] != 0:
            self.x = pygame.mouse.get_pos()[0] - self.w // 2
        self.x = max(0, min(WIDTH - self.w, self.x))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        pygame.draw.rect(screen, BASKET_COLOR, self.rect(), border_radius=8)


class Fruit:
    def __init__(self, speed):
        self.r = 16
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = -self.r
        
        self.speed = speed + random.random() * 1.5
        self.color = random.choice(FRUIT_COLORS)

    def update(self):
        self.y += self.speed

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)


def draw_lives(lives):
    for i in range(3):
        color = RED if i < lives else (180, 180, 180)
        pygame.draw.circle(screen, color, (WIDTH - 30 - i * 35, 25), 12)


def game_over_screen(score, best):
    screen.fill(BG)
    t = big_font.render("Game Over", True, TEXT)
    s = font.render(f"Score: {score}   Best: {best}", True, TEXT)
    r = font.render("Press R to restart or Q to quit", True, TEXT)
    screen.blit(t, t.get_rect(center=(WIDTH // 2, 240)))
    screen.blit(s, s.get_rect(center=(WIDTH // 2, 310)))
    screen.blit(r, r.get_rect(center=(WIDTH // 2, 370)))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                return
        clock.tick(30)


def main():
    best = 0
    while True:
        basket = Basket()
        fruits = []
        score, lives = 0, 3
        spawn_timer = 0
        base_speed = 3
        pygame.mouse.get_rel()

        while lives > 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            basket.move(pygame.key.get_pressed())

            spawn_timer -= 1
            if spawn_timer <= 0:
                fruits.append(Fruit(base_speed))
                spawn_timer = max(25, 70 - score)

            for f in fruits[:]:
                f.update()
                if f.rect().colliderect(basket.rect()):
                    fruits.remove(f)
                    score += 1
                    base_speed = 3 + (score // 5) * 0.4
                elif f.y - f.r > HEIGHT:
                    fruits.remove(f)
                    lives -= 1

            screen.fill(BG)
            basket.draw()
            for f in fruits:
                f.draw()
            screen.blit(font.render(f"Score: {score}", True, TEXT), (12, 12))
            draw_lives(lives)
            pygame.display.flip()
            clock.tick(60)

        best = max(best, score)
        game_over_screen(score, best)


if __name__ == "__main__":
    main()
