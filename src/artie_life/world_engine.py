"""Module containing the single world's execution engine."""
from multiprocessing import Process
from pygame import init, QUIT, quit as quit_game
from pygame.event import get as get_events
from pygame.key import set_repeat as set_key_repeat
from pygame.time import Clock
from controller.game_controller import GameController
from controller.input import ClickController, TextController
from view.game_view import GameView

class WorldEngine(Process):
    """Class representing the single world's execution engine."""

    def __init__(self, world_id: "int", population: "int", learning_enable: "str",
                 genetic_algorithm: "str") -> "None":
        """Constructor for the world's execution engine.
        
        Positional arguments:  
        `world_id`: the in-game world's ID.  
        `population`: the initial population size.  
        `learning_enable`: true/false flag representing if the agents should be  
        learning or acting randomly.  
        `genetic_algorithm`: the kind of genetic algorithm applied to the  
        population, or none if all genomes should be randomly generated."""
        self.world_id = world_id
        self.population = population
        self.learning_enable = learning_enable
        self.genetic_algorithm = genetic_algorithm
        self.running = True
        super().__init__()

    def run(self) -> "None":
        """Main method of the world engine."""
        init()
        game_controller = GameController(self.genetic_algorithm)
        game_controller.create_world(
            self.population,
            self.learning_enable == "true"
        )
        clock = Clock()
        dt: "int" = 0
        while self.running:
            game_controller.update_world(dt / 1000)
            dt = clock.tick()

        game_controller.dump_current_state()
        quit_game()


class GuiWorldEngine(WorldEngine):
    """World engine implementation with GUI rendering enabled."""

    def run(self) -> "None":
        """Main method of the GUI world engine."""
        init()
        set_key_repeat(200, 75)

        game_controller = GameController(self.genetic_algorithm)
        game_controller.create_world(
            self.population,
            self.learning_enable == "true"
        )

        view = GameView()
        click_controller= ClickController(game_controller.world, view)
        text_controller= TextController(game_controller.world, view)

        view.show_screen()

        clock = Clock()
        dt: "int" = 0
        while self.running:
            events = get_events()
            for event in events:
                if event.type == QUIT:
                    self.running = False

            if click_controller.is_spawn_requested(events):
                game_controller.spawn_random_living()

            game_controller.update_world(dt / 1000)
            view.render(game_controller.get_map_elems())

            click_controller.handle_living_selection(events)
            if game_controller.is_living_selected():
                text_controller.update(events)
                view.render_bottom_bar(
                    game_controller.get_selected_info(),
                    game_controller.get_focus_object()
                )
                click_controller.handle_user_reward(events)
            else:
                text_controller.clear()

            view.show_frame()

            dt = clock.tick()

        game_controller.dump_current_state()
        quit_game()
