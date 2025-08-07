from graphics import Canvas
import time
import random

# Canvas size constants
CANVAS_WIDTH = 500  # Width of the game window
CANVAS_HEIGHT = 600  # Height of the game window

# Paddle constants
PADDLE_Y = CANVAS_HEIGHT - 30  # Vertical position of the paddle
PADDLE_WIDTH = 80  # Width of the paddle
PADDLE_HEIGHT = 15  # Height of the paddle

# Ball constants
BALL_RADIUS = 10  # Radius of the ball

# Brick layout constants
BRICK_GAP = 5  # Gap between bricks
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * 9) / 10  # Width of each brick
BRICK_HEIGHT = 10  # Height of each brick

# Game state constants
TURNS = 3  # Total number of lives
BRICK_ROWS = 10  # Total number of rows of bricks
BRICKS_PER_ROW = 10  # Number of bricks per row
TOTAL_BRICKS = BRICK_ROWS * BRICKS_PER_ROW  # Total number of bricks

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)  # Create the game window
    create_bricks(canvas)  # Draw the bricks on the screen

    bricks_left = TOTAL_BRICKS  # Track remaining bricks
    turns_left = TURNS  # Track remaining lives

    paddle = create_paddle(canvas)  # Create one paddle

    while turns_left > 0:
        ball = create_ball(canvas)  # Create a new ball
        change_x, change_y = random_velocity()  # Initial movement direction

        while True:
            canvas.move(ball, change_x, change_y)  # Move ball on screen
            x = canvas.get_left_x(ball)  # Get left x of ball
            y = canvas.get_top_y(ball)  # Get top y of ball

            # Reverse x direction if it hits left or right wall
            if x <= 0 or x + BALL_RADIUS * 2 >= CANVAS_WIDTH:
                change_x = -change_x

            # Reverse y direction if it hits top wall
            if y <= 0:
                change_y = -change_y

            # Lose a life if ball touches bottom
            if y + BALL_RADIUS * 2 >= CANVAS_HEIGHT:
                canvas.delete(ball)  # Remove the ball
                turns_left -= 1  # Lose a life
                break  # End this turn

            # Move paddle with mouse
            mouse_x = canvas.get_mouse_x()  # Get horizontal mouse position
            if mouse_x is not None:
                new_x = mouse_x - PADDLE_WIDTH / 2  # Center the paddle
                new_x = max(0, min(new_x, CANVAS_WIDTH - PADDLE_WIDTH))  # Limit within screen
                canvas.moveto(paddle, new_x, PADDLE_Y)  # Move paddle

            # Detect collisions
            collision_type, obj = check_collision(canvas, ball, paddle)
            if collision_type == "paddle":
                change_y = -abs(change_y)  # Bounce up if hits paddle
            elif collision_type == "brick":
                canvas.delete(obj)  # Remove the brick
                bricks_left -= 1  # Decrease brick count
                change_y = -change_y  # Bounce

                if bricks_left == 0:
                    canvas.delete(ball)  # Clear ball
                    print("You win!")  # Player wins
                    return

            time.sleep(1 / 60)  # Control game speed

    print("Game over!")  # Player loses

def create_bricks(canvas):
    colors = ["red", "orange", "yellow", "green", "cyan"]  # Brick colors
    for row in range(BRICK_ROWS):
        color = colors[row // 2]  # Each color repeats 2 rows
        for col in range(BRICKS_PER_ROW):
            x = col * (BRICK_WIDTH + BRICK_GAP)  # X position of brick
            y = 50 + row * (BRICK_HEIGHT + BRICK_GAP)  # Y position of brick
            canvas.create_rectangle(
                x,
                y,
                x + BRICK_WIDTH,
                y + BRICK_HEIGHT,
                color,
                color  # Fill and border same color
            )

def create_ball(canvas):
    x = (CANVAS_WIDTH - BALL_RADIUS * 2) / 2  # Center X
    y = (CANVAS_HEIGHT - BALL_RADIUS * 2) / 2  # Center Y
    return canvas.create_oval(
        x, y,
        x + BALL_RADIUS * 2,
        y + BALL_RADIUS * 2,
        "black"  # Ball color
    )

def random_velocity():
    change_x = random.uniform(3, 5)  # Random horizontal speed
    change_y = 5  # Fixed vertical speed
    if random.choice([True, False]):
        change_x = -change_x  # Random left or right
    return change_x, change_y

def create_paddle(canvas):
    x = (CANVAS_WIDTH - PADDLE_WIDTH) / 2  # Center horizontally
    y = PADDLE_Y  # Fixed vertical position
    return canvas.create_rectangle(
        x, y,
        x + PADDLE_WIDTH, y + PADDLE_HEIGHT,
        "black"  # Paddle color
    )

def check_collision(canvas, ball, paddle):
    x = canvas.get_left_x(ball)  # X of ball
    y = canvas.get_top_y(ball)  # Y of ball
    size = BALL_RADIUS * 2  # Diameter of ball

    overlapping = canvas.find_overlapping(x, y, x + size, y + size)  # All overlapping objects

    for obj in overlapping:
        if obj == ball:
            continue  # Skip the ball itself
        elif obj == paddle:
            return "paddle", obj  # Hit paddle
        else:
            return "brick", obj  # Hit brick

    return None, None  # No collision

if __name__ == '__main__':
    main()
