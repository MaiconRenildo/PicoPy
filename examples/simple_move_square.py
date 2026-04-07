import sys
from picopy.pico import PicoPy

def main():
    pico = PicoPy()
    pixels_per_world_unit = 10
    window_width, window_height = pico.get_display_resolution()
    world_width = window_width // pixels_per_world_unit
    world_height = window_height // pixels_per_world_unit
    pico.set_dim_window((window_width, window_height))
    pico.set_dim_world((world_width, world_height))
    pico.init(True)

    square_size = 10
    player_speed = 5
    frame_delay_ms = 16
    
    pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))
    player_x, player_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
    player_square_tuple = (player_x, player_y, square_size, square_size)

    running = True
    event_object = pico.new_event_object()

    while running:
        while pico.input_event_ask(event_object, pico.EVENT_ANY):
            if pico.is_quit_event(event_object):
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

        pico.output_clear()

        pico.set_color(pico.COLOR_YELLOW)
        pico.set_style(pico.DRAW_FILL)
        pico.output_draw_rect(player_square_tuple)

        pico.output_present()
        pico.input_delay(frame_delay_ms) # Approximately 60 FPS

    pico.init(False)
    print("PicoPy shut down.")

if __name__ == "__main__":
    sys.exit(main())