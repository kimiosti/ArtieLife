"""Main application module."""

if __name__=='__main__':
    import pygame
    from pygame.time import Clock
    from view.game_view import GameView
    from controller.game_controller import GameController
    from controller.input import ClickController

    pygame.init()

    game_controller: "GameController" = GameController()
    game_controller.create_world()

    view: "GameView" = GameView()

    click_controller: "ClickController" = ClickController(game_controller.world, view)

    clock: "Clock" = Clock()

    view.show_screen()

    dt: "int" = 0
    running: "bool" = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        click_controller.handle_living_selection(events)
        if click_controller.is_spawn_requested(events):
            game_controller.spawn_random_living()

        game_controller.update_world(dt / 1000)
        view.render(game_controller.get_map_elems())

        if game_controller.is_living_selected():
            view.render_bottom_bar(game_controller.get_selected_info())

        view.show_frame()

        dt = clock.tick(30)

    pygame.quit()
