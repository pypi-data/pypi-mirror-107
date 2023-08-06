class Paint:
    """A code template for a person creating a picture.

    Stereotype:
        Service Provider, Interfacer
    """

    def __init__(self):
        """The class constructor.

        Args:
            self (Paint): an instance of Paint.

        All assets in this __init__ method are raw strings,
        derived from ASCII art by Roland Hangg. Original image
        may be found at https://www.asciiart.eu/computers/computers
        """
        self.__top = r"""                     ________________________________________________
                    /                                                \
                   |    _________________________________________     |"""

        self.__left_border = """                   |   |"""

        self.__right_border = """|    |"""

        self.__bottom = r"""                   |   |_________________________________________|    |
                   |                                                  |
                    \_________________________________________________/
                           \___________________________________/
                        ___________________________________________
                     _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
                  _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
               _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
            _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
         _-'.-.-.-.-.-. .---.-. .-------------------------. .-.---. .---.-.-.-.`-_
        :-------------------------------------------------------------------------:
        `---._.-------------------------------------------------------------._.---'"""

    def paint_screen(self, player=str, history=list, stats=tuple):
        """Creates image of text on an ASCII art computer screen.

        Args:
            self (Console): an instance of Console.
            player (string): name of player.
            history (list): list of (guess, hint) tuples.
            stats (tuple): Tuple of total round points and playtime of player.
        """
        print(self.__top)
        self.__paint_header(player, stats[0], stats[1])
        for entry in history:
            self.__paint_line(entry[0], entry[1])
        if len(history) < 13:
            i = 0
            while i < (13 - len(history)):
                i += 1
                self.__paint_line('-', '-')
        print(self.__bottom)

    def __paint_header(self, player=str, points=int, playtime=float):
        """Paints header text on an ASCII art computer screen.

        Args:
            self (Console): an instance of Console.
            player (string): name of player.
            points (int): total points for player for round
            playtime (float): elapsed time (seconds) of player for round
        """

        stat_text = f" Lock: ENGAGED [{points} @ {playtime:.2f}]"
        print(self.__left_border, end='')
        print(f"{stat_text:<41}", end='')
        print(self.__right_border)

        title = " User: " + player + " >> echo $HISTORY"
        print(self.__left_border, end='')
        print(f"{title:<41}", end='')
        print(self.__right_border)

        print(self.__left_border, end='')
        print(f"{'........INPUT.......':^20}", end='')
        print(f"{'':^1}", end='')
        print(f"{'.......OUTPUT.......':^20}", end='')
        print(self.__right_border)

    def __paint_line(self, left_col=str, right_col=str):
        """Paints one line of text, in two columns, on ASCII
        art computer screen.

        Args:
            self (Console): an instance of Console.
            left_col (string): text to paint in left column
            right_col (string): text to paint in right column
        """
        print(self.__left_border, end='')
        print(f"{left_col:^20}", end='')
        print(f"{'|':^1}", end='')
        print(f"{right_col:^20}", end='')
        print(self.__right_border)
