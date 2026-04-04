import sys
from picopy.pico import PicoPy

def main():
    pico = PicoPy()
    pixels_per_world_unit = 10
    window_width, window_height = 800, 600
    world_width = window_width // pixels_per_world_unit
    world_height = window_height // pixels_per_world_unit
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
            if int(event.type) == pico.EVENT_QUIT:
                running = False
            elif int(event.type) == pico.EVENT_MOUSEBUTTONDOWN:
                if int(event.button.button) == pico.MOUSE_LEFT:
                    squares_list.append((event.button.x, event.button.y, square_size, square_size))
                elif int(event.button.button) == pico.MOUSE_RIGHT:
                    if squares_list:
                        squares_list.pop()
        pico.output_clear()
        for rect in squares_list:
            pico.output_draw_rect(rect)
        pico.output_present()
        pico.input_delay(16)
    pico.init(False)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())
