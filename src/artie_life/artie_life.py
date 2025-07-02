"""Main application module."""
from view.game_view import GameView

if __name__=='__main__':
    import pygame
    from model.world import World

    world = World()
    for _ in range(3):
        world.spawn_living()

    view = GameView()

    pygame.init()

    view.show_screen()

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        view.render(world)

    pygame.quit()
