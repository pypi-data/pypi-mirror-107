import random


class Board:
    """ (AH). The Prepare Method and _Create_Hint Method were given.

    A code template to track the gameboard for a Mastermind game.
    The responsibility of this class of objects is to prepare the gameboard
    with a random four digit number and create hints for the players.

    Stereotype:
        Service Provider, Interfacer

    Attributes:
        code (integer): 4-digit number random number between 1000 and 9999.
        guess (integer): each player guesses a four digit number.
    """

    def __init__(self):
        """ (AH).
        The class constructor. Declares and initializes instance Attributes.

        Args:
            self (Board): an instance of Board.
        """
        # _items is a dictionary used in Prepare Method.
        self._items = {}

    def generate_code(self):
        """Sets up the board with an entry for each player.

        Args:
            self (Board): an instance of Board.
            player (Player): an instance of Player.  (AH).
        """
        return str(random.randint(1000, 10000))

    def validate_guess(self, guess):
        """ (AH).
        Board.validate_guess verifies that guess is a four-digit integer.

        Args:
            self (Board): an instance of Board.
            guess (string): The guess that was made.

        Returns:
            Boolean: whether the guess is a four-digit integer.
        """
        if guess is None:
            return False
        elif guess.isdigit() and len(guess) == 4:
            return True
        return False

    def create_hint(self, code, guess):
        """ (_Create_Hint Method was given in a requirement snippet.)
        Generates a hint based on the given code and guess.

        Args:
            self (Board): An instance of Board.
            code (string): The code to compare with.
            guess (string): The guess that was made.

        Returns:
            string: A hint in the form [xxxx]
        """
        hint = ""
        for index, letter in enumerate(guess):
            if code[index] == letter:
                hint += "x"
            elif letter in code:
                hint += "o"
            else:
                hint += "*"
        return hint

    def update_board(self, player, guess):
        """ (AH).
        Updates the gameboard with player, current guess, and current hint.

        Args:
            self (Board): An instance of Board.
            player (Player): an instance of Player.
            guess (string): The guess that was made.

        Returns:
            None.
        """
        name = player.get_name()
        code = self._items[name][0]
        self._items[name][1] = guess
        self._items[name][2] = self.create_hint(code, guess)

    def info_to_display(self, player):
        """ (AH).
        Passes current board info for Director to call Console to display.

        Args:
            self (Board): An instance of Board.
            player (Player): an instance of Player.

        Returns:
            string: A four-digit integer guess in the form [xxxx].
            string: A hint in the form [xxxx]
        """
        name = player.get_name()
        # Returns guess and hint.
        return self._items[name][1], self._items[name][2]
