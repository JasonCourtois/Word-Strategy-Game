import random
import pygame
import wordle

WIDTH, HEIGHT = 600, 800
FPS = 144

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Wordle!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

LEFT_BORDER = 85
RIGHT_BORER = WIDTH - LEFT_BORDER
MIDDLE = WIDTH / 2
H_SPACING = 90
V_SPACING = 90
SQUARE_LEN = 70


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pass
        clock.tick(FPS)
        WINDOW.fill(WHITE)
        pygame.draw.rect(WINDOW, BLACK, (85, 0, 1, 800))
        pygame.draw.rect(WINDOW, BLACK, (RIGHT_BORER, 0, 1, 800))
        pygame.draw.rect(WINDOW, GREEN, (MIDDLE, 0, 1, 800))
        # Squares
        for i in range(6):
            for j in range(5):
                pygame.draw.rect(WINDOW, BLACK, ((LEFT_BORDER + j * H_SPACING), 20 + (i * V_SPACING), SQUARE_LEN, SQUARE_LEN))
        #pygame.draw.rect(WINDOW, BLACK, (265, 20, SQUARE_LEN, SQUARE_LEN))





        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
