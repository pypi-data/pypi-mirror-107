import os
import inquirer
from time import sleep, time
from sys import stdout
from json import load

from game.roster import Roster
from game.paint import Paint


class Console:
    """A code template for a person who directs the game. The responsibility of
    this class of objects is to control the sequence of play.

    Stereotype:
        Service Provider, Interfacer

    Attributes:
        roster (Roster): An instance of the class of objects known as Roster.
    """

    def __init__(self):
        """The class constructor.

        Args:
            self (Console): an instance of Console.
        """

        self._roster = Roster()
        self._paint = Paint()

        self.stop_game = False
        self.__show_menu = True
        self.__logo = []
        self.__fame = []
        self.__rules = []

        with open("mastermind/assets/logo.txt") as data:
            next(data)
            for line in data:
                self.__logo.append(line)

        with open("mastermind/assets/fame.txt") as data:
            next(data)
            for line in data:
                self.__fame.append(line)

        with open("mastermind/assets/rules.txt") as data:
            next(data)
            for line in data:
                self.__rules.append(line)

    def clear_screen(self):
        """Detects OS type and sends appropriate console command to clear screen.

        Args:
            self (Console): An instance of Console.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def ask_stop_game(self):
        """Returns bool indicating whether game should continue running.

        Args:
            self (Console): an instance of Console.
        """
        return self.stop_game

    def restart_menu(self):
        """Returns bool indicating whether game should continue running.

        Args:
            self (Console): an instance of Console.
        """
        self.__show_menu = True

    def confirm_start(self, player=str):
        """Returns bool indicating whether game should continue running.

        Args:
            self (Console): an instance of Console.
            player (string): name of player for turn confirmation.
        """
        self.clear_screen()
        print("\n" * 11)
        pass_text = "Pass the device to " + player
        print(f"{pass_text : ^100}")
        input(f"{'Press ENTER when ready.' : ^100}")
        return self.stop_game

    def cool_print(self, text=str, newline=True, margin=21, rate=.02):
        """Prints text in typewriter style.

        Args:
            self (Console): an instance of Console.
            text (str): Text to print.
            newline (bool): whether to end with carriage return
        """
        print(" " * margin, end='')
        for letter in text:
            sleep(.02)
            stdout.write(letter)
            stdout.flush()
        if newline:
            print()

    def play_turn(self, player=str, code=str, history=list, stats=tuple,
                  redo=False):
        """Displays board and prompts for player guess. Returns tuplet of
        guess (string) and time taken to guess in seconds (float).

        Args:
            self (Console): an instance of Console.
            player (string): name of player.
            code (string): code to be guessed, for hint generation.
            history (list): list of (guess, hint) tuples.
            stats (tuple): Tuple of total round points and playtime of player.
            redo (bool): whether this is a repeat prompt due to invalid guess.
        """
        self.clear_screen()

        if redo:
            print('\n' * 15)
            self.cool_print("KEYCODE IS 4-DIGIT NUMBER BETWEEN 1000 AND 9999")
            self.cool_print("PRESS ENTER TO RE-ATTEMPT")
            input(" " * 21)
            self.clear_screen()

        self._paint.paint_screen(player, history, stats)
        self.cool_print("RUNNING: d42k_10ckp1ck32.exe")
        self.cool_print("ENTER 4-DIGIT KEYCODE:", newline=False)

        start = time()

        guess = input(" ")

        end = time()
        elapsed = end - start

        return (guess, elapsed)

    def show_hint(self, hint=str):
        """Displays hint for player.

        Args:
            self (Console): an instance of Console.
            hint (str).
        """
        self.clear_screen()
        print('\n' * 15)
        self.cool_print("ERROR 210.04-TC6: [KEYCODE INCORRECT]")
        self.cool_print("DATA CORRUPTED. ATTEMPTING TO DECRYPT METADATA.")
        print()
        sleep(.6)
        self.cool_print(f"[!] METADATA RECOVERED: {hint}")
        print()
        self.cool_print("PRESS ENTER TO REATTEMPT", newline=False)
        input()

    def __print_logo(self, left=5, top=2, bottom=2):
        """Prints logo to screen. Has optional x and y parameters to offset logo
        by specified amount of lines and spaces.

        Args:
            self (Console): An instance of Console.
            left (int): Number of spaces to offset logo from left of screen
            top (int): Number of lines to offset logo from top of screen
            bottom (int): Number of spaces to print below logo
        """

        print('\n' * top, end="")

        for line in self.__logo:
            print((" " * left) + line, end="")

        print('\n' * bottom, end="")

    def __print_rules(self, left=0):
        """Prints rules to screen. Has optional x and y parameters to offset logo
        by specified amount of lines and spaces.

        Args:
            self (Console): An instance of Console.
            left (int): Number of spaces to offset rules from left of screen

        """

        for line in self.__rules:
            print((" " * left) + line, end="")

    def menu(self):
        """Shows menu to start game.

        Args:
            self (Console): an instance of Console.
        """

        while self.__show_menu and not self.stop_game:

            p_num = 0
            if self._roster.get_roster():
                p_num = len(self._roster.get_roster())

            add_text = "Add/Remove Players [" + str(p_num) + " registered]"
            choice_list = [
                (add_text, "add"),
                "Rules",
                ("Leaderboard", "scores"),
                "Quit"
                ]

            if self._roster.get_roster():
                choice_list.insert(0, "START")

            questions = [
                inquirer.List(
                    'selection',
                    message="MENU (Use ↑ and ↓ to select, ENTER to confirm)",
                    choices=choice_list,
                    carousel=True,
                    default="add")
                    ]

            self.clear_screen()
            self.__print_logo()
            selection = inquirer.prompt(questions)['selection'].lower()

            if selection == "start":
                self.__show_menu = False
                return self._roster.get_roster()
            elif selection == "add":
                self.__add_players()
            elif selection == "rules":
                self.__show_rules()
            elif selection == "scores":
                self.__show_scoreboard()
            elif selection == "quit":
                self.__quit()

    def __add_players(self):
        """Asks records player names.

        Args:
            self (Console): an instance of Console.
        """
        players_list = []
        players_list.extend([("NEW PLAYER", "**new**")])
        players_list.extend(self._roster.get_roster())
        players_list.extend([("BACK TO MENU", "**menu**")])

        players = [
            inquirer.List(
                'selection',
                message="ADD/REMOVE (Use ↑ and ↓ to select, ENTER to confirm)",
                choices=players_list,
                default="NEW PLAYER",
                carousel=True)
            ]

        self.clear_screen()
        self.__print_logo()
        selection = inquirer.prompt(players)['selection']

        if selection == "**menu**":
            pass
        elif selection == "**new**":
            name = self.__prompt_name()
            if name:
                self._roster.add_player(name)
        else:
            delete = inquirer.confirm(
                f"Do you want to remove '{selection}'?", default=True
                )
            if delete:
                self._roster.remove_player(selection)
            input(f"'{selection}' removed. Press ENTER to continue.")

    def __prompt_name(self):
        """Prompts for player name,.

        Args:
            self (Console): an instance of Console.
        """
        self.clear_screen()
        self.__print_logo()

        name = input("[!] Enter new player name and press ENTER:\n\n   ")
        if not (2 < len(name) < 16):
            self.clear_screen()
            self.__print_logo()
            print("Username must be between 3 and 15 characters.")
            input("Press ENTER to return to player menu.")
        elif name in self._roster.get_roster():
            self.clear_screen()
            self.__print_logo()
            print("Player already exists.")
            input("Press ENTER to return to player menu.")
        else:
            return name

    def __show_rules(self):
        """Asks records player names.

        Args:
            self (Console): an instance of Console.
        """
        self.clear_screen()
        self.__print_logo()
        self.__print_rules(left=20)
        input()

    def __show_scoreboard(self):
        """Asks records player names.

        Args:
            self (Console): an instance of Console.
        """
        self.clear_screen()

        print('\n' * 2, end="")
        for line in self.__fame:
            print((" " * 5) + line, end="")
        print('\n' * 2, end="")

        with open("mastermind/assets/scores.json", "r") as data:
            board = list(load(data).items())

        space = " " * 11
        print(f"{space}RANK     {'PLAYER':<30}" +
              f"{'TIME':>7} (seconds){'POINTS':>29}\n")

        lines_printed = 0
        for idx, entry in enumerate(board[:10]):
            lines_printed += 1
            space = " " * 10
            n = idx + 1
            year, month, day, time = entry[0].split(" ")
            points = entry[1]["points"]
            playtime = entry[1]["playtime"]
            player = entry[1]["player"]

            print(f"{space}{n:>4}.     {player:<30}" +
                  f"{playtime:>7,.2f}{points:>36}/15")

        lines = "\n" * (12 - lines_printed)
        print(f"{lines}{space}", end="")
        sleep(.25)
        self.cool_print("Press ENTER to return to player menu.",
                        newline=False, margin=0)
        input()

    def __quit(self):
        """Asks records player names.

        Args:
            self (Console): an instance of Console.
        """
        self.clear_screen()
        self.__print_logo()
        print('\n'*3)
        self.cool_print("THANKS FOR PLAYING!")
        sleep(2)
        self.stop_game = True
