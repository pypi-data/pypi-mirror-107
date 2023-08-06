from datetime import datetime
from json import load, dump


class Score:
    """A code template for a person keeping track of the number of turns
    each player has taken, as well as how long each turn took.

    Stereotype:
        Information Holder
    """

    def __init__(self, players=list):
        """The class constructor.

        Args:
            self (Score): an instance of Score.
            players (list): a list of players in the round
        """
        self.__turns = {player: [] for player in players}
        self.__fastest = {}
        self.__highest = {}
        self.__start = 0
        self.__end = 0

        with open("mastermind/assets/scores.json", "r") as data:
            self.__leaderboard = load(data)

    def record_turn(self, elapsed, player=str):
        """Records end time of players turn.
        Start time is subtracted from end time, and the resulting elapsed time
        is appended to a given player's

        Args:
            self (Score): an instance of Score.
            elapsed (float): total time taken for turn (in seconds).
            player (string): name of player
        """
        self.__turns[player].append(elapsed)

    def get_stats(self, player=str):
        """Returns tuple of total points (int) and total seconds of
        playtime (float) for given player for current round.

        Points are determined by subtracting the total turns taken from 16.

        Args:
            self (Score): an instance of Score.
            player (string): name of player
        """
        score = 16 - len(self.__turns[player])
        points = score if score > 0 else 0
        playtime = sum(self.__turns[player])

        return(points, playtime)

    def get_board(self):
        """Returns a dictionary of leaderboard stats of winning player turns
        and player times, with structure.

        Args:
            self (Score): an instance of Score.
        """
        with open("mastermind/assets/scores.json", "r") as data:
            board = load(data)

        return board

    def update_board(self, player, stats):
        """Updates leaderboard dictionary with new best score and time.

        Args:
            self (Score): an instance of Score.
            player (string): name of player
            stats (tuple): Tuple of total round points and playtime of player.
        """
        points, playtime = stats
        timestamp = datetime.now().strftime("%Y %m %d %H%M%S")

        self.__leaderboard.update(
            {timestamp: {
                "points": points,
                "playtime": round(playtime, 3),
                "player": player}})

        new_dict = {k: v for (k, v) in sorted(
                self.__leaderboard.items(),
                key=lambda x: x[1]["playtime"])}

        with open("mastermind/assets/scores.json", "w") as data:
            dump(new_dict, data, indent=4)
