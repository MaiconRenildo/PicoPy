import random
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
    pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))
    pico.init(True)
    
    delay_ms = 1000
    square_size = 10
    max_x = world_width - square_size
    max_y = world_height - square_size

    running = True
    while running:
        pico.set_style(pico.DRAW_FILL)
        pico.output_clear()  # Limpa a tela para preto

        random_r = random.randint(0, 255)
        random_g = random.randint(0, 255)
        random_b = random.randint(0, 255)
        random_color = (random_r, random_g, random_b, 255)
        pico.set_color(random_color)

        square_x = random.randint(0, max_x)
        square_y = random.randint(0, max_y)
        square_rect = (square_x, square_y, square_size, square_size)
        pico.output_draw_rect(square_rect) # Desenha o quadrado
        pico.output_present() # Exibe na tela
        pico.input_delay(delay_ms) # Espera 1 segundo

        pico.output_clear() # Limpa a tela para preto
        pico.output_present() # Exibe tela sem o quadrado
        pico.input_delay(delay_ms) # Espera 1 segundo

        # Verifica se o usuário fechou a janela durante a espera
        event = pico.new_event_object()
        while pico.input_event_ask(event, pico.EVENT_QUIT):
            if event.type == pico.EVENT_QUIT:
                running = False
        if not running:
            break
    pico.init(False)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())