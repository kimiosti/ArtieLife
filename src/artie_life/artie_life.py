"""Main application module."""

if __name__ == '__main__':
    from multiprocessing import freeze_support
    from argparse import ArgumentParser
    from typing import TYPE_CHECKING
    from world_engine import WorldEngine, GuiWorldEngine
    from utils.logs import reset_logs_folder, log_game_settings

    if TYPE_CHECKING:
        from typing import List
    
    freeze_support()

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
        "--population",
        default=0,
        type=int,
        help="indicates how many individuals are to be spawned in the initial population of"
            + " each world. If omitted, it defaults to 0. If the GUI option is enabled, more"
            + " individuals can be spawned at any time."
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

    reset_logs_folder()
    log_game_settings(arguments.learning, arguments.genetic_algo)

    engines: "List[WorldEngine]" = [
        WorldEngine(i+1, arguments.population, arguments.learning, arguments.genetic_algo)
            if arguments.gui == "false"
            else GuiWorldEngine(
                i+1,
                arguments.population,
                arguments.learning,
                arguments.genetic_algo
            ) for i in range(arguments.number)
    ]
    for engine in engines:
        engine.start()
