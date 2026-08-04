import random
import time

from picopy.pico import PicoPy


def check_rect_collision(rect_a, rect_b):
    ax, ay, aw, ah = rect_a
    bx, by, bw, bh = rect_b
    return (
        ax < bx + bw
        and ax + aw > bx
        and ay < by + bh
        and ay + ah > by
    )


def handle_collision(player_square, red_squares_list, consumed_flags):
    for i in range(len(red_squares_list)):
        if not consumed_flags[i] and check_rect_collision(
            player_square, red_squares_list[i]
        ):
            consumed_flags[i] = 1



pico = PicoPy()

pico.init(True)
window_width, window_height = pico.get_dim_window()
world_width, world_height = pico.get_dim_world()
pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))

square_size = 5
player_speed = 1
frame_delay_ms = 16
text_delay_ms = 3000
num_red_squares = 10
game_duration_seconds = 30

max_square_x = world_width - square_size
max_square_y = world_height - square_size

player_x, player_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
player_square = (player_x, player_y, square_size, square_size)

consumed_flags = [0] * num_red_squares
red_squares_list = []

random.seed(time.time())
for _ in range(num_red_squares):
    square_x = random.randint(0, max_square_x)
    square_y = random.randint(0, max_square_y)
    red_squares_list.append((square_x, square_y, square_size, square_size))

running = True
event = pico.new_event_object()

start_time = pico.get_ticks()

while running:
    current_time = pico.get_ticks()
    if (current_time - start_time) // 1000 >= game_duration_seconds:
        pico.output_clear()
        pico.set_color(pico.COLOR_RED)
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
        text_pos = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
        pico.output_draw_text(text_pos, "GAME OVER!")
        pico.input_delay(text_delay_ms)
        running = False
        break

    has_won = True
    for i in range(num_red_squares):
        if consumed_flags[i] == 0:
            has_won = False
            break

    if has_won:
        pico.output_clear()
        pico.set_color(pico.COLOR_GREEN)
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
        text_pos = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
        pico.output_draw_text(text_pos, "YOU WON!")
        pico.input_delay(3000)
        running = False
        break

    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event):
            running = False

    if pico.get_key(pico.SCANCODE_W):
        player_y -= player_speed
    if pico.get_key(pico.SCANCODE_S):
        player_y += player_speed
    if pico.get_key(pico.SCANCODE_A):
        player_x -= player_speed
    if pico.get_key(pico.SCANCODE_D):
        player_x += player_speed

    player_square = (player_x, player_y, square_size, square_size)
    handle_collision(player_square, red_squares_list, consumed_flags)
    pico.output_clear()

    for i in range(num_red_squares):
        if not consumed_flags[i]:
            pico.set_color(pico.COLOR_RED)
            pico.set_style(pico.DRAW_FILL)
            pico.output_draw_rect(red_squares_list[i])

    pico.set_color(pico.COLOR_YELLOW)
    pico.set_style(pico.DRAW_FILL)
    pico.output_draw_rect(player_square)
    pico.input_delay(frame_delay_ms)

pico.init(False)
print("PicoPy shut down.")