import pygame
import wordle

WIDTH, HEIGHT = 800, 800
FPS = 60

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
        pygame.draw.rect(WINDOW, (255, 255, 255), (test[0], test[1], 500, 500))

    pygame.quit()

if __name__ == "__main__":
    main()
