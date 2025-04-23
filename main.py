import pygame
import random
import sys

pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1500 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = 30  
    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.velocity = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.size, self.size))  # jaune


class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.x = SCREEN_WIDTH
        self.width = 60
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        return self.x > -self.width

    def draw(self):
        #inversé tuyaux du haut
        top_pipe_height = self.gap_y - PIPE_GAP // 2
        pygame.draw.rect(screen, (0, 200, 0), (self.x, 0, self.width, top_pipe_height))

        bottom_pipe_y = self.gap_y + PIPE_GAP // 2
        bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y
        pygame.draw.rect(screen, (0, 200, 0), (self.x, bottom_pipe_y, self.width, bottom_pipe_height))

    def check_collision(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.size, bird.size)
        top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)
        bottom_pipe = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2,
                                  self.width, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2))
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)


def main():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    font = pygame.font.Font(None, 36)
    game_active = True

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.flap()
                    else:
                        bird = Bird()
                        pipes = []
                        score = 0
                        last_pipe = current_time
                        game_active = True

        if game_active:
            # Màj de l'oiseau
            bird.update()

            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            # Màj des tuyaux
            pipes = [pipe for pipe in pipes if pipe.update()]

            # Vérification des collisions et score
            for pipe in pipes:
                if pipe.check_collision(bird):
                    game_active = False
                elif not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1

        screen.fill(SKY_BLUE)
        
        for pipe in pipes:
            pipe.draw()
        
        bird.draw()

        # Afficher score
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        if not game_active:
            game_over_text = font.render('Game Over - Press SPACE to restart', True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
