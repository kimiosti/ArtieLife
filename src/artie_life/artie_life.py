"""Main application module."""

if __name__ == '__main__':
    from argparse import ArgumentParser
    from typing import TYPE_CHECKING
    from pygame import init, QUIT, quit
    from pygame.event import get as get_events
    from world_engine import WorldEngine

    if TYPE_CHECKING:
        from typing import List

    parser = ArgumentParser(
        description = "Artificial Life simulator combining reinforcement learning"
            + " and genetic algorithms for entertainment purposes",
        epilog = "For more information and source code, visit github.com/kimiosti/ArtieLife"
    )

    parser.add_argument(
        "-n", "--number",
        default=1,
        type=int,
        help="indicates how many instances of the game world are instantiated and executed"
            + " in parallel. If omitted, it defaults to 1."
    )

    parser.add_argument(
        "--gui",
        choices=["true", "false"],
        default="true",
        help="true/false argument indicating whether a graphical rendering of the game world"
            + " is requested. To be used carefully when n != 1, since unexpected behavior"
            + " might occur. If omitted, it defaults to true."
    )

    parser.add_argument(
        "-l", "--learning",
        choices=["true", "false"],
        default="true",
        help="true/false argument indicating if the game agents must learn their behavior, or"
            + " if they should act randomly. If omitted, it defaults to true."
    )

    parser.add_argument(
        "--genetic-algo",
        default="none",
        choices=["none", "params"],
        help="indicates what type of genetic algorithm has to be applied to the game agents'"
            + " population. Accepted values are 'none' to generate random genomes for all"
            + " agents, and 'params' to apply a parameter optimization genetic algorithm."
            + " If omitted, it defaults to 'none'."
    )

    arguments = parser.parse_args()

    engines: "List[WorldEngine]" = [WorldEngine(
        i+1,
        arguments.gui,
        arguments.learning,
        arguments.genetic_algo
    ) for i in range(arguments.number)]
    for engine in engines:
        engine.start()

    init()
    running = True
    while running:
        for event in get_events():
            if event.type == QUIT:
                running = False

    for engine in engines:
        engine.kill()

    quit()
