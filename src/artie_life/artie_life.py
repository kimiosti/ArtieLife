"""Main application module."""

if __name__=='__main__':
    from pygame import QUIT, quit as quit_game, init as init_game
    from pygame.event import get as get_all_events
    from pygame.time import Clock
    from pygame.key import set_repeat as set_key_repeat
    from view.game_view import GameView
    from controller.game_controller import GameController
    from controller.input import ClickController, TextController

    init_game()
    set_key_repeat(200, 75)

    game_controller: "GameController" = GameController()
    game_controller.create_world()

    view: "GameView" = GameView()

    click_controller: "ClickController" = ClickController(game_controller.world, view)
    text_controller: "TextController" = TextController(game_controller.world, view)

    clock: "Clock" = Clock()

    view.show_screen()

    dt: "int" = 0
    running: "bool" = True
    while running:
        events = get_all_events()
        for event in events:
            if event.type == QUIT:
                running = False

        if click_controller.is_spawn_requested(events):
            game_controller.spawn_random_living()

        game_controller.update_world(dt / 1000)
        view.render(game_controller.get_map_elems())

        click_controller.handle_living_selection(events)
        if game_controller.is_living_selected():
            text_controller.update(events)
            view.render_bottom_bar(game_controller.get_selected_info())
            click_controller.handle_user_reward(events)
        else:
            text_controller.clear()

        view.show_frame()

        dt = clock.tick(30)

    quit_game()
