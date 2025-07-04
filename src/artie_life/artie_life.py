"""Main application module."""

if __name__=='__main__':
    import pygame
    from view.game_view import GameView
    from controller.game_controller import GameController

    controller = GameController()
    controller.create_world()
    for _ in range(3):
        controller.world.spawn_living()

    view = GameView()

    pygame.init()

    view.show_screen()

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        view.render(controller.get_map_elems())

    pygame.quit()
