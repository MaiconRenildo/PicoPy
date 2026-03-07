import os
import sys
import sdl2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pico import PicoPy
from constants import PICO_FILL, PICO_ANY

def main():
    pico_app = PicoPy()
    pico_app.pico_init(1)

    # melhorar a definição das dimensões
    pico_app.pico_set_dim_window((800, 600))
    pico_app.pico_set_dim_world((800, 600))

    pico_app.pico_set_color((0, 0, 255, 255))
    pico_app.pico_set_style(PICO_FILL)

    squares_list = []
    square_size = 5
    running = True
    event = sdl2.SDL_Event()
    print("Clique na janela do PicoPy para desenhar quadrados azuis. Pressione 'X' para sair.")
    while running:
        while pico_app.pico_input_event_ask(event, PICO_ANY):
            if int(event.type) == sdl2.SDL_QUIT:
                running = False
            elif int(event.type) == sdl2.SDL_MOUSEBUTTONDOWN:
                # Só desenha com botão esquerdo (1); coordenadas já ajustadas (scroll) pelo PicoPy
                if int(event.button.button) == 1:
                    click_x = int(event.button.x)
                    click_y = int(event.button.y)
                    print(f"Clique detectado em: ({click_x}, {click_y})")
                    squares_list.append((click_x, click_y, square_size, square_size))
                elif int(event.button.button) == 3:
                    # Botão direito: remove ultimo quadrado desenhado
                    click_x = int(event.button.x)
                    click_y = int(event.button.y)
                    print(f"Clique detectado em: ({click_x}, {click_y})")
                    if squares_list:
                        squares_list.pop()
        pico_app.pico_output_clear()
        for rect in squares_list:
            pico_app.pico_output_draw_rect(rect)
        pico_app.pico_output_present()
        pico_app.pico_input_delay(16)

    pico_app.pico_init(0)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())
