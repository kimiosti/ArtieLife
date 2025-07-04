"""Main application module."""

if __name__=='__main__':
    import pygame
    from pygame.time import Clock
    from view.game_view import GameView
    from controller.game_controller import GameController

    controller: "GameController" = GameController()
    controller.create_world()
    for _ in range(3):
        controller.spawn_living()

    view: "GameView" = GameView()

    pygame.init()
    clock: "Clock" = Clock()

    view.show_screen()

    dt: "int" = 0
    running: "bool" = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        controller.update_world(dt)
        view.render(controller.get_map_elems())

        dt = clock.tick(30)

    pygame.quit()
