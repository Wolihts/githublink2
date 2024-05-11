from typing import *
import random

DOT_SIZE = 10
MOVEMENT_DELAY = 90
WIDTH = 600
HEIGHT = 600
LENGTH = 3
GRID_SIZE = 40

class Logic:
    """
    Start game logic with the players id, player_id is the id of the player
    also setting up the logic of the game itself such as scores and spawn
    """
    def __init__(self, player_id: str) -> None:
        self.player_id = player_id
        self.snake: List[Tuple[int, int]] = []
        for i in range(LENGTH):
            gm = (20, 20 + i * 10)
            self.snake.append(gm)
        self.food: Tuple[int, int] = self.create_food()
        self.direction: str = 'Right'
        self.running: bool = False
        self.score: int = 0
        self.high_scores = self.load_leaderboard()

    def create_food(self) -> Tuple[int, int]:
        """
        food is made here, food will spawn randomly and tuple[int, int] is the cordinates
        """
        while True:
            max_x = (WIDTH // 10) - 1
            max_y = (HEIGHT // 10) - 1
            random_x = random.randint(0, max_x) * 10
            random_y = random.randint(0, max_y) * 10
            food = (random_x, random_y)
            if food not in self.snake:
                return food

    def move_snake(self) -> bool:
        """
        Starts putting logic to moving the snake toward a direction
        without this we won't have a moving snake
        True = move, False = Game Over
        """
        if not self.running:
            return False
        head_x, head_y = self.snake[0]
        move_offsets = {'Left': (-10, 0), 'Right': (10, 0), 'Up': (0, -10), 'Down': (0, 10)}
        head_x = head_x + move_offsets[self.direction][0]
        head_y = head_y + move_offsets[self.direction][1]
        new_head = (head_x, head_y)
        if new_head in self.snake:
            collision = True
        else:
            collision = False
        within_bounds = 0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT
        if collision or not within_bounds:
            self.running = False
            self.load_leaderboard()
            return False
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score = self.score + 10
            self.food = self.create_food()
        else:
            self.snake.pop()
        return True

    def reset_game(self) -> None:
        """
        resetting the game to the start
        """
        self.snake = []
        for i in range(LENGTH):
            coordinate = (20, 20 + i * 10)
            self.snake.append(coordinate)
        self.food = self.create_food()
        self.direction = 'Right'
        self.running = True
        self.score = 0

    def load_leaderboard(self) -> List[Tuple[int, str]]:
        """
        Loading the leaderboard from a file
        List[tuple[int, str]] is the scores that allign with the players
        """
        try:
            with open('leaderboard.txt', 'r') as file:
                lines = file.readlines()
                result = []
                for line in lines:
                    stripped_line = line.strip()
                    split_line = stripped_line.split(':')
                    tuple_line = tuple(split_line)
                    result.append(tuple_line)
                return result
        except FileNotFoundError:
            return []

    def refresh_leaderboard(self) -> None:
        """
        main goal is so that the leaderboard is up to date every game
        this is done with Player ID and latest score
        """
        self.high_scores.append((self.score, self.player_id))
        s_scores = sorted(self.high_scores, key=lambda x: -int(x[0]))
        self.high_scores = s_scores[:2]
        with open('leaderboard.txt', 'w') as file:
            for score, player in self.high_scores:
                file.write(f"{score}:{player}\n")

    def get_leaderboard(self) -> str:
        """
        we get the leaderboard by formatting it, this is done by returning a string
        """
        leaderboard_lines = [f"{player}: {score}" for score, player in self.high_scores]
        return '\n'.join(leaderboard_lines)


    def reset_scores(self) -> None:
        """
        this is extra so that both players are able to reset stats whenever they want
        """
        self.score = 0
        self.high_scores = [(0, 'Player 1'), (0, 'Player 2')]
        with open('leaderboard.txt', 'w') as file:
            for score, player in self.high_scores:
                file.write(f"{score}:{player}\n")
