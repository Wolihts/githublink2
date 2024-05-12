import tkinter as tk
from logic import *

class GUI:
    def __init__(self, game: tk.Tk) -> None:
        """
        Start Gui setup for the the game,
        Not limited to but includes window, title, sizes, buttons etc
        We are also setting up our direction keys here,
        (W, A, S, D) & (Arrows Up, Down, Right, Left)
        """
        self.game = game
        self.game.title("Snake")
        self.game.resizable(False, False)
        self.player_id = "Player 1"
        self.logic = Logic(self.player_id)
        self.canvas = tk.Canvas(self.game, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()
        self.player_label = tk.Label(self.game, text=f"Active Player: {self.player_id}", font=('Arial', 16))
        self.player_label.pack()
        self.score_label = tk.Label(self.game, text="Score: 0", font=('Arial', 14))
        self.score_label.pack()
        self.leaderboard_label = tk.Label(self.game, text="Leaderboard:\n" + self.logic.get_leaderboard(), font=('Arial', 14))
        self.leaderboard_label.pack()
        self.start_button = tk.Button(self.game, text="Start Game", command=self.start)
        self.start_button.pack()
        self.player_button = tk.Button(self.game, text="Switch Player", command=self.switch_player)
        self.player_button.pack()

        self.game.bind("<Left>", self.pressed_keys)
        self.game.bind("<Right>", self.pressed_keys)
        self.game.bind("<Up>", self.pressed_keys)
        self.game.bind("<Down>", self.pressed_keys)
        self.game.bind("a", self.pressed_keys)
        self.game.bind("d", self.pressed_keys)
        self.game.bind("w", self.pressed_keys)
        self.game.bind("s", self.pressed_keys)
        
        self.reset_scores_button = tk.Button(self.game, text="Reset Scores", command=self.reset_scores)
        self.reset_scores_button.pack()
        
        self.game.protocol("WM_DELETE_WINDOW", self.ending)
    
    def reset_scores(self) -> None:
        """
        Reset scores, this means back to initial settings of zero, so click carefully
        """
        self.logic.reset_scores()
        self.score_label.config(text="Score: 0")
        self.leaderboard_label.config(text="Leaderboard:\n" + self.logic.get_leaderboard())
        self.canvas.create_text(WIDTH // 2, HEIGHT // 4, text="Scores Reset", fill="white", font=('Arial', 16))
        
    def pressed_keys(self, e) -> None:
        """
        handling the keys from our inital state,
        we are using tkinter key events "e(tk.event)"
        """
        key = e.keysym
        if (key == "Left" or key == "a") and self.logic.direction != 'Right':
            self.logic.direction = 'Left'
        elif (key == "Right" or key == "d") and self.logic.direction != 'Left':
            self.logic.direction = 'Right'
        elif (key == "Up" or key == "w") and self.logic.direction != 'Down':
            self.logic.direction = 'Up'
        elif (key == "Down" or key == "s") and self.logic.direction != 'Up':
            self.logic.direction = 'Down'

    def gameWindow(self) -> None:
        """
        drawing the elements for the canvas of Snake
        """
        self.canvas.delete(tk.ALL)
        for segment in self.logic.snake:
            x1, y1 = segment
            x2, y2 = x1 + DOT_SIZE, y1 + DOT_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='')
        food_x1, food_y1 = self.logic.food
        food_x2, food_y2 = food_x1 + DOT_SIZE, food_y1 + DOT_SIZE
        self.canvas.create_rectangle(food_x1, food_y1, food_x2, food_y2, fill='red', outline='')

    def start(self) -> None:
        """
        Start of the game and gui refresh
        """
        self.start_button.pack_forget()
        self.logic.reset_game()
        self.refresh()

    def refresh(self) -> None:
        """
        Refreshes the state of the game, and we also do the same for the gui
        """
        if self.logic.move_snake():
            self.gameWindow()
            self.score_label.config(text=f"Score: {self.logic.score}")
            self.leaderboard_label.config(text="Leaderboard:\n" + self.logic.get_leaderboard())
            if self.logic.running:
                self.game.after(MOVEMENT_DELAY, self.refresh)
            else:
                self.logic.refresh_leaderboard()
                self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=('Arial', 24))
                self.start_button.config(text="Restart Game")
                self.start_button.pack()
        else:
            self.logic.refresh_leaderboard()
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=('Arial', 24))
            self.start_button.config(text="Restart Game")
            self.start_button.pack()

    def switch_player(self) -> None:
        """
        Switch between ONLY two players 1 and 2.
        We also refresh the gui fpr this
        """
        if self.logic.running:
            self.logic.running = False
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=('Arial', 24))
        if self.player_id == "Player 1":
            self.player_id = "Player 2"
        else:
            self.player_id = "Player 1"
        self.logic = Logic(self.player_id)
        self.player_label.config(text=f"Active Player: {self.player_id}")
        self.score_label.config(text="Score: 0")
        self.leaderboard_label.config(text="Leaderboard:\n" + self.logic.get_leaderboard())
        self.start_button.config(text="Start Game")
        self.start_button.pack()

    def ending(self) -> None:
        """
        Handling the Window Closing 
        """
        self.logic.refresh_leaderboard()
        self.game.destroy()
