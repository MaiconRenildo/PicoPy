from picopy.pico import PicoPy


pico = PicoPy()
window_width, window_height = 800, 600
world_width, world_height = 80, 60
pico.set_dim_window((window_width, window_height))
pico.set_dim_world((world_width, world_height))
pico.set_color(pico.COLOR_BLUE)
pico.set_style(pico.DRAW_FILL)
pico.init(True)

squares_list = []
square_size = 1 # 1 PIXEL
running = True
event = pico.new_event_object()
print("Clique na janela do PicoPy para desenhar quadrados azuis. Pressione 'X' para sair.")
while running:
    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event):
            running = False
        elif pico.is_mouse_button_event(event, pico.MOUSE_LEFT):
            squares_list.append((event.button.x, event.button.y, square_size, square_size))
        elif pico.is_mouse_button_event(event, pico.MOUSE_RIGHT):
            if squares_list:
                squares_list.pop()
    pico.output_clear()
    for rect in squares_list:
        pico.output_draw_rect(rect)
    pico.input_delay(16)
pico.init(False)
print("PicoPy desligado.")