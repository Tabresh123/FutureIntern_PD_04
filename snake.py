import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game with GUI")
        self.root.resizable(False, False)  # Prevent resizing the window

        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake segments
        self.snake_direction = 'Right'  # Initial movement direction
        self.food = None
        self.score = 0
        self.game_over = False

        self.setup_ui()
        self.create_food()
        self.update_game()

    def setup_ui(self):
        # Create score label
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        # Create start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        # Bind keyboard events for controlling the snake
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))

    def start_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Reset snake
        self.snake_direction = 'Right'
        self.score = 0
        self.game_over = False
        self.update_score()
        self.create_food()
        self.update_game()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def change_direction(self, new_direction):
        # Prevent the snake from reversing
        if (self.snake_direction == "Left" and new_direction != "Right") or \
           (self.snake_direction == "Right" and new_direction != "Left") or \
           (self.snake_direction == "Up" and new_direction != "Down") or \
           (self.snake_direction == "Down" and new_direction != "Up"):
            self.snake_direction = new_direction

    def create_food(self):
        """Create food at a random position"""
        food_x = random.randint(0, 29) * 20  # 30 cells wide
        food_y = random.randint(0, 19) * 20  # 20 cells high
        self.food = (food_x, food_y)
        self.canvas.create_rectangle(food_x, food_y, food_x + 20, food_y + 20, fill="red", tag="food")

    def update_game(self):
        """Update the game every 100ms"""
        if self.game_over:
            self.canvas.create_text(300, 200, text="Game Over! Press Start to play again", fill="white", font=("Arial", 16))
            return

        # Move the snake
        head_x, head_y = self.snake[0]
        if self.snake_direction == 'Right':
            head_x += 20
        elif self.snake_direction == 'Left':
            head_x -= 20
        elif self.snake_direction == 'Up':
            head_y -= 20
        elif self.snake_direction == 'Down':
            head_y += 20

        # Check for collision with boundaries or self
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 400 or (head_x, head_y) in self.snake:
            self.game_over = True
            self.update_score()
            return

        # Add the new head to the snake
        self.snake = [(head_x, head_y)] + self.snake[:-1]

        # Check if snake eats the food
        if (head_x, head_y) == self.food:
            self.snake.append(self.snake[-1])  # Add a new segment to snake
            self.score += 10
            self.update_score()
            self.canvas.delete("food")  # Remove food from the canvas
            self.create_food()  # Create new food

        # Clear the canvas and redraw the snake
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tag="snake")

        self.canvas.after(100, self.update_game)  # Call update_game again after 100ms

# Create the Tkinter window
root = tk.Tk()

# Create the SnakeGame instance
game = SnakeGame(root)

# Start the Tkinter main loop
root.mainloop()
