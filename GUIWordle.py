import random
import pygame
import wordle

WIDTH, HEIGHT = 800, 800
FPS = 144

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Wordle!')


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pass
        clock.tick(FPS)
        test = pygame.mouse.get_pos()
        pygame.draw.rect(WINDOW, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (test[0], test[1], 1, 1))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
