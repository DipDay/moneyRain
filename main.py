from sys import exit
import random
from tkinter import messagebox
import pygame


# Window and timing configuration.
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Player movement limits and collision lanes.
PLAYER_MIN_X = 43
PLAYER_MAX_X = 343
LANE_XS = (45, 137, 230, 325)
PLAYER_DRAW_Y = 535
HEART_DRAW_Y = -17

# Background animation frames stored in final_road/.
BACKGROUND_FRAME_MIN = 2
BACKGROUND_FRAME_SKIP = 280
BACKGROUND_FRAME_RESET = 391


def random_offset():
    """Return an initial Y position for money items above the screen."""

    return -1 * random.randint(100, 1500)


def police_random_offset():
    """Return an initial Y position for police items above the screen."""

    return (-1 * random.randint(600, 4000)) - 150


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame_icon = pygame.image.load("logo.png")
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Money Rain")
clock = pygame.time.Clock()


# Asset filenames must stay unchanged so the game loads exactly as before.
money = pygame.image.load("money.png")
user1 = pygame.image.load("user1.png")
user2 = pygame.image.load("user2.png")
user3 = pygame.image.load("user3.png")
police = pygame.image.load("police.png")
heart = pygame.image.load("heart.png")
label = pygame.image.load("label.png")


# Core game state.
level = 3
frame_num = 0
heart_num = 3
when_crash = 1
when_crash2 = 1
user_x = 180
score = 0
keep_alive = True

money_y = [random_offset() for _ in range(4)]
police_y = [police_random_offset() for _ in range(4)]


def display_score(current_score):
    """Draw the score label and centered score text at the top of the screen."""

    label_x = -157
    if 0 <= current_score < 10:
        label_x = -157
    elif 10 <= current_score < 100:
        label_x = -140
    elif 100 <= current_score < 1000:
        label_x = -122
    elif current_score >= 1000:
        label_x = -104
    elif -100 < current_score <= -10:
        label_x = -130
    elif -1000 < current_score <= -100:
        label_x = -112

    screen.blit(label, [label_x, -43])
    font = pygame.font.SysFont("Comic Sans MS", 30)
    score_text = f"Money: {current_score}$"
    text = font.render(score_text, True, "#ffffff")
    screen.blit(text, [9, 0])


def crashed(idx):
    """Handle collecting a money item and respawn it above the screen."""

    global score

    score += 10
    money_y[idx] = random_offset()


def police_crashed(idx):
    """Handle hitting a police item, which reduces score and hearts."""

    global score
    global heart_num
    global when_crash
    global when_crash2

    if when_crash == 1:
        when_crash = score
    else:
        when_crash2 = score

    score -= 10
    print("Crashed with police", idx + 1, score)

    heart_num -= 1
    police_y[idx] = police_random_offset()


def increase_heart(current_hearts):
    """Restore a heart after a 500-point gap from the last police collision."""

    global when_crash
    global when_crash2
    global score

    if (score - when_crash == 500) or (score - when_crash2 == 500):
        if current_hearts == 3:
            return 0
        if current_hearts == 2:
            when_crash = 1
            return 1
        if current_hearts == 1:
            when_crash = 1
            return 1
    return 0


def update_money_pos(idx, current_level):
    """Move a money item down the screen or respawn it once it leaves view."""

    if money_y[idx] > SCREEN_HEIGHT:
        money_y[idx] = random_offset()
    else:
        money_y[idx] += current_level


def update_police_pos(idx, current_level):
    """Move a police item down the screen or respawn it once it leaves view."""

    if police_y[idx] > SCREEN_HEIGHT:
        police_y[idx] = police_random_offset()
    else:
        police_y[idx] += current_level


def level_num(current_score):
    """Return the current movement speed based on the player's score."""

    if 150 <= current_score < 300:
        return 4
    if 300 <= current_score < 500:
        return 5
    if current_score >= 500:
        return 6
    return 3


def game_over():
    """Show the restart prompt and reset the score-related state if needed."""

    global heart_num
    global score
    global level

    messagebox.showinfo(title="Oops :(", message="GAME OVER!")
    answer = messagebox.askyesno(
        title="Yes or No",
        message="Do you want to play again?",
    )
    if answer:
        heart_num = 3
        score = 0
        level = 3
        return True

    print("Have a nice day!")
    return False


def draw_background_frame(current_frame):
    """Load and draw the current animated background frame."""

    frame_name = f"{current_frame}.jpg"
    full_name = f"final_road\\{frame_name}"
    background = pygame.image.load(full_name)
    screen.blit(background, [0, 0])


def draw_player(current_hearts, current_x):
    """Draw the current player sprite and return whether the game continues."""

    if current_hearts == 3:
        screen.blit(user1, [current_x, PLAYER_DRAW_Y])
    elif current_hearts == 2:
        screen.blit(user2, [current_x, PLAYER_DRAW_Y])
    elif current_hearts == 1:
        screen.blit(user3, [current_x, PLAYER_DRAW_Y])
    else:
        return game_over()

    return True


def draw_hearts(current_hearts):
    """Render the life icons that indicate the remaining hearts."""

    if current_hearts == 3:
        screen.blit(heart, [375, HEART_DRAW_Y])
        screen.blit(heart, [326, HEART_DRAW_Y])
        screen.blit(heart, [276, HEART_DRAW_Y])
    elif current_hearts == 2:
        screen.blit(heart, [326, HEART_DRAW_Y])
        screen.blit(heart, [375, HEART_DRAW_Y])
    elif current_hearts == 1:
        screen.blit(heart, [375, HEART_DRAW_Y])


def draw_lane_items(image, positions):
    """Draw one item image across the four fixed lanes."""

    for lane_x, lane_y in zip(LANE_XS, positions):
        screen.blit(image, [lane_x, lane_y])


def lane_contains_player(current_x, lane_index):
    """Return True when the player is inside the collision range for a lane."""

    lane_ranges = (
        current_x < 97,
        80 < current_x < 200,
        190 < current_x < 290,
        280 < current_x < 343,
    )
    return lane_ranges[lane_index]


def handle_collisions():
    """Apply the money and police collision rules for the current frame."""

    for idx in range(4):
        if idx == 0 and money_y[idx] > 485 and lane_contains_player(user_x, idx):
            crashed(idx)
        elif idx == 1 and money_y[idx] > 485 and lane_contains_player(user_x, idx):
            crashed(idx)
        elif idx == 2 and money_y[idx] > 485 and lane_contains_player(user_x, idx):
            crashed(idx)
        elif idx == 3 and money_y[idx] > 485 and lane_contains_player(user_x, idx):
            crashed(idx)

        if idx == 0 and 452 < police_y[idx] < 560 and lane_contains_player(user_x, idx):
            police_crashed(idx)
        elif idx == 1 and 452 < police_y[idx] < 560 and lane_contains_player(user_x, idx):
            police_crashed(idx)
        elif idx == 2 and 452 < police_y[idx] < 560 and lane_contains_player(user_x, idx):
            police_crashed(idx)
        elif idx == 3 and 452 < police_y[idx] < 560 and user_x > 280:
            police_crashed(idx)


def play_game():
    """Run the main gameplay loop until the user exits or stops playing."""

    global frame_num
    global user_x
    global heart_num
    global level
    global keep_alive

    while keep_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and user_x < PLAYER_MAX_X:
            user_x += 10
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and user_x > PLAYER_MIN_X:
            user_x -= 10

        if keys[pygame.K_ESCAPE]:
            p_answer = messagebox.askyesno(
                title="Exit",
                message="Do you want to exit?",
            )
            if p_answer:
                keep_alive = False

        if keys[pygame.K_p]:
            p_answer = messagebox.askyesno(
                title="Paused",
                message="Do you want to continue?",
            )
            if not p_answer:
                keep_alive = False

        level = level_num(score)

        update_money_pos(0, level)
        update_money_pos(1, level)
        update_money_pos(2, level)
        update_money_pos(3, level)

        update_police_pos(0, level)
        update_police_pos(1, level)
        update_police_pos(2, level)
        update_police_pos(3, level)

        frame_num += 1
        if frame_num == BACKGROUND_FRAME_SKIP:
            frame_num = BACKGROUND_FRAME_SKIP + 1
        if frame_num == BACKGROUND_FRAME_RESET:
            frame_num = BACKGROUND_FRAME_MIN

        draw_background_frame(frame_num)

        if not draw_player(heart_num, user_x):
            keep_alive = False
        draw_lane_items(money, money_y)
        draw_lane_items(police, police_y)
        draw_hearts(heart_num)

        handle_collisions()
        heart_num += increase_heart(heart_num)

        display_score(score)
        pygame.display.update()
        clock.tick(FPS)


if keep_alive:
    play_game()
