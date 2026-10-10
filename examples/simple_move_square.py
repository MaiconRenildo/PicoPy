from picopy.pico import PicoPy

pico = PicoPy()
pico.init(True)

square_size = 10
player_speed = 5
frame_delay_ms = 16

pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))
player_x, player_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))

running = True

while running:
    while event := pico.input_event_ask(pico.EVENT_ANY):
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

    pico.output_clear()
    pico.set_color(pico.COLOR_YELLOW)
    pico.set_style(pico.DRAW_FILL)
    pico.output_draw_rect(player_square)

    pico.input_delay(frame_delay_ms)

pico.init(False)
print("PicoPy shut down.")