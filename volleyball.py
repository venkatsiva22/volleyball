import tkinter as tk
import random

# Constants
WIDTH = 800
HEIGHT = 400
BALL_RADIUS = 20
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 20
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
NET_HEIGHT = 10

class VolleyballGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Volleyball Game")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
        self.canvas.pack()

        # Create paddles
        self.player1_paddle = self.canvas.create_rectangle(50, HEIGHT//2 - PADDLE_HEIGHT//2, 50 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2, fill="red")
        self.player2_paddle = self.canvas.create_rectangle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, WIDTH - 50, HEIGHT//2 + PADDLE_HEIGHT//2, fill="blue")

        # Create net
        self.net = self.canvas.create_rectangle(WIDTH//2 - 5, 0, WIDTH//2 + 5, NET_HEIGHT, fill="black")

        # Create ball
        self.ball = self.canvas.create_oval(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS, fill="white")

        # Game state
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y
        self.player1_score = 0
        self.player2_score = 0

        # Score display
        self.score_display = self.canvas.create_text(WIDTH//2, 20, text=f"Player 1: {self.player1_score}  Player 2: {self.player2_score}", font=("Arial", 16))

        # Key bindings
        self.root.bind("<w>", self.move_player1_up)
        self.root.bind("<s>", self.move_player1_down)
        self.root.bind("<Up>", self.move_player2_up)
        self.root.bind("<Down>", self.move_player2_down)

        self.run_game()

    def run_game(self):
        # Move ball
        self.move_ball()

        # Check for collisions
        self.check_collisions()

        # Update score
        self.update_score()

        # Check for game over
        if self.player1_score >= 10 or self.player2_score >= 10:
            self.game_over()

        # Repeat every 10 ms
        self.root.after(10, self.run_game)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)

        # Ball hitting top/bottom walls
        if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
            self.ball_dy = -self.ball_dy

        # Ball hitting net
        if ball_coords[2] >= self.canvas.coords(self.net)[0] and ball_coords[0] <= self.canvas.coords(self.net)[2]:
            if ball_coords[1] <= self.canvas.coords(self.net)[3] or ball_coords[3] >= HEIGHT:
                self.ball_dy = -self.ball_dy

        # Ball out of bounds (left or right)
        if ball_coords[0] <= 0:
            self.player2_score += 1
            self.reset_ball()

        elif ball_coords[2] >= WIDTH:
            self.player1_score += 1
            self.reset_ball()

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS)
        self.ball_dx = random.choice([4, -4])
        self.ball_dy = random.choice([4, -4])

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)

        # Player 1 paddle collision
        if self.check_paddle_collision(ball_coords, self.player1_paddle):
            self.ball_dx = -self.ball_dx

        # Player 2 paddle collision
        if self.check_paddle_collision(ball_coords, self.player2_paddle):
            self.ball_dx = -self.ball_dx

    def check_paddle_collision(self, ball_coords, paddle):
        paddle_coords = self.canvas.coords(paddle)
        return (ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and
                ball_coords[3] >= paddle_coords[1] and ball_coords[1] <= paddle_coords[3])

    def move_player1_up(self, event):
        self.canvas.move(self.player1_paddle, 0, -PADDLE_SPEED)
        self.check_paddle_boundaries(self.player1_paddle)

    def move_player1_down(self, event):
        self.canvas.move(self.player1_paddle, 0, PADDLE_SPEED)
        self.check_paddle_boundaries(self.player1_paddle)

    def move_player2_up(self, event):
        self.canvas.move(self.player2_paddle, 0, -PADDLE_SPEED)
        self.check_paddle_boundaries(self.player2_paddle)

    def move_player2_down(self, event):
        self.canvas.move(self.player2_paddle, 0, PADDLE_SPEED)
        self.check_paddle_boundaries(self.player2_paddle)

    def check_paddle_boundaries(self, paddle):
        coords = self.canvas.coords(paddle)
        if coords[1] < 0:
            self.canvas.move(paddle, 0, -coords[1])  # Keep paddle within bounds
        elif coords[3] > HEIGHT:
            self.canvas.move(paddle, 0, HEIGHT - coords[3])  # Keep paddle within bounds

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=f"Player 1: {self.player1_score}  Player 2: {self.player2_score}")

    def game_over(self):
        winner = "Player 1" if self.player1_score >= 10 else "Player 2"
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f"{winner} Wins!", font=("Arial", 24), fill="black")
        self.root.after(2000, self.root.quit)  # Wait for 2 seconds then close the game

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    game = VolleyballGame(root)
    root.mainloop()
