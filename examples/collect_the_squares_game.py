
import sys
import random
import time

from picopy.pico import PicoPy

def check_rect_collision(rect_a_tuple: tuple[int, int, int, int], rect_b_tuple: tuple[int, int, int, int]) -> bool:
    """Checks for collision between two rectangles (squares) represented by tuples."""
    ax, ay, aw, ah = rect_a_tuple
    bx, by, bw, bh = rect_b_tuple
    return (ax < bx + bw and
            ax + aw > bx and
            ay < by + bh and
            ay + ah > by)

def handle_collision(player_square_tuple: tuple[int, int, int, int], red_squares_list: list[tuple[int, int, int, int]], consumed_flags: list[int]):
    """Marks red squares as consumed after collision with the player."""
    for i in range(len(red_squares_list)):
        if not consumed_flags[i] and check_rect_collision(player_square_tuple, red_squares_list[i]):
            consumed_flags[i] = 1  # Mark as consumed

def main():
    pico = PicoPy()
    pixels_per_world_unit = 10
    window_width, window_height = pico.get_display_resolution()
    world_width = window_width // pixels_per_world_unit
    world_height = window_height // pixels_per_world_unit
    pico.set_dim_window((window_width, window_height))
    pico.set_dim_world((world_width, world_height))
    pico.init(True)

    square_size = 5
    player_speed = 1
    frame_delay_ms = 16 # Approximately 60 FPS
    text_delay_ms = 3000
    num_red_squares = 10
    game_duration_seconds = 30
    
    # Max limits for random square generation
    max_square_x = world_width - square_size
    max_square_y = world_height - square_size

    # Initial position of the yellow square (player)
    player_x, player_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
    player_square_tuple = (player_x, player_y, square_size, square_size)

    # Initialize red squares and consumed flags
    consumed_flags = [0] * num_red_squares
    red_squares_list = [] # Stores as tuples (x, y, w, h)
    for _ in range(num_red_squares):
        square_x = random.randint(0, max_square_x)
        square_y = random.randint(0, max_square_y)
        red_squares_list.append((square_x, square_y, square_size, square_size))

    running = True
    event = pico.new_event_object() # SDL2 event object

    random.seed(time.time())
    start_time = time.time()

    while running:
        current_time = time.time()
        if (current_time - start_time) >= game_duration_seconds:
            pico.output_clear()
            pico.set_color(pico.COLOR_RED)
            text_pos = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
            pico.output_draw_text(text_pos, "GAME OVER!")
            pico.output_present()
            pico.input_delay(text_delay_ms)
            running = False
            break

        # Check if the player won (all squares consumed)
        has_won = True
        for i in range(num_red_squares):
            if consumed_flags[i] == 0:
                has_won = False
                break
        
        if has_won:
            pico.output_clear() # Limpa a tela
            pico.set_color(pico.COLOR_GREEN)
            text_pos = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
            pico.output_draw_text(text_pos, "YOU WON!")
            pico.output_present() # Exibe a mensagem na tela
            pico.input_delay(3000) # Opcional: espera 3 segundos
            running = False
            break

        # Process events (keyboard and window close)
        while pico.input_event_ask(event, pico.EVENT_QUIT):
            running = False
        
        if pico.get_key(pico.SCANCODE_W):
            player_y -= player_speed
        if pico.get_key(pico.SCANCODE_S):
            player_y += player_speed
        if pico.get_key(pico.SCANCODE_A):
            player_x -= player_speed
        if pico.get_key(pico.SCANCODE_D):
            player_x += player_speed
        
        player_square_tuple = (player_x, player_y, square_size, square_size)
        handle_collision(player_square_tuple, red_squares_list, consumed_flags)
        pico.output_clear()

        # Draw remaining red squares
        for i in range(num_red_squares):
            if not consumed_flags[i]:
                pico.set_color(pico.COLOR_RED)
                pico.set_style(pico.DRAW_FILL)
                pico.output_draw_rect(red_squares_list[i])
        # Draw the yellow square (player)
        pico.set_color(pico.COLOR_YELLOW)
        pico.set_style(pico.DRAW_FILL)
        pico.output_draw_rect(player_square_tuple)
        pico.output_present()
        pico.input_delay(frame_delay_ms)  # Approximately 60 FPS
    pico.init(False)
    print("PicoPy shut down.")

if __name__ == "__main__":
    sys.exit(main())