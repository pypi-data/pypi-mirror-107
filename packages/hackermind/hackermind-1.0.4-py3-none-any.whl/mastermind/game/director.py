from game.board import Board
from game.console import Console
from game.player import Player
from game.score import Score


class Director:
    """A code template for a person who directs the game. The responsibility of
    this class of objects is to control the sequence of play.

    Stereotype:
        Controller

    Attributes:
        keep_playing (boolean): Whether or not the game can continue.
        board (Board): An instance of the class of objects known as Board.
        console (Console): An instance of the Console class of objects.
        helper (Helper): An instance of the class of objects known as Helper.
        move (Move): An instance of the class of objects known as Move.
        player (Player): An instance of the class of objects known as Player.
        roster (Roster): An instance of the class of objects known as Roster.
    """

    def __init__(self):
        """The class constructor.

        Args:
            self (Director): an instance of Director.
        """
        self.__stop_round = False
        self._board = Board()
        self._console = Console()

    def run_game(self):
        """Starts the game loop to control the sequence of play.

        Args:
            self (Director): an instance of Director.
        """
        while not self._console.ask_stop_game():
            players = self._console.menu()
            if not self._console.ask_stop_game():
                self.__play_round(players)
            print("\n"*15)

        self._console.clear_screen()

    def __play_round(self, players=list):
        """Runs a round of play and returns a winner.

        Args:
            self (Director): an instance of Director.
            players (list): a list of player names.
        """
        code = self._board.generate_code()
        self._player = Player(players)
        self._score = Score(players)
        self.__stop_round = False

        while not self.__stop_round:
            for player in players:
                if len(players) > 1:
                    self._console.confirm_start(player)

                history = self._player.get_moves(player)
                stats = self._score.get_stats(player)

                guess, elapsed = self._console.play_turn(player, code,
                                                         history, stats)
                self._score.record_turn(elapsed, player)

                while not self._board.validate_guess(guess):
                    stats = self._score.get_stats(player)
                    guess, elapsed = self._console.play_turn(player, code,
                                                             history, stats,
                                                             redo=True)
                    self._score.record_turn(elapsed, player)

                if guess == code:
                    stats = self._score.get_stats(player)
                    self._score.update_board(player, stats)

                    self.__end_round(player, stats)
                    self.__stop_round = True
                    self._console.restart_menu()
                    break

                hint = self._board.create_hint(code, guess)
                self._console.show_hint(hint)

                move_hint = (guess, hint)
                self._player.record_move(player, move_hint)

    def __end_round(self, winner=str, stats=tuple):
        """Announces the winner and ends the round

        Args:
            self (Director): an instance of Director.
            winner (list): name of the victor.
            stats (tuple): Tuple of total round points and playtime of player.
        """
        self._console.clear_screen()
        points, time = stats
        print("\n"*15)
        self._console.cool_print(f'           {winner} wins!')
        print()
        self._console.cool_print(f'   Points: {points} out of 15')
        self._console.cool_print(f'     Time: {time:.2f} seconds')
        input()
