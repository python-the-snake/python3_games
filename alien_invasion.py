import sys
import pygame

def run_game():
    # инициализирует игру и создает объект экрана.
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.dispaly.set_caption('Alien Invasion')

    # назначение цвета фона
    bg_color = (230, 230, 230)

    # запуск основного цикла игры
    while True:
        # отслеживание событий клавиатуры и мышки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # отображение последнего прорисованного экрана
        pygame.display.flip()

run_game()