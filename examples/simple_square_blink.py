import os
import random
import sys
import sdl2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pico import PicoPy
from constants import PICO_FILL

# Cores
RED = (255, 0, 0, 255)   # Vermelho
BLACK = (0, 0, 0, 255) # Preto (cor de fundo padrão)

def main():
    pico_app = PicoPy()
    
    # Inicializa o PicoPy
    pico_app.pico_init(1)
    
    # Configura o tamanho da janela e do mundo
    pico_app.pico_set_dim_window((640, 480)) # Janela de 640x480
    pico_app.pico_set_dim_world((640, 480))  # Mundo lógico 1:1 com a janela
    pico_app.pico_set_anchor_pos((0, 0))    # Anchor no canto superior esquerdo

    window_width, window_height = pico_app.pico_get_dim_window()

    # Calcula os limites máximos para x e y
    # A posição inicial (canto superior esquerdo) do quadrado
    # não pode ser maior que a largura/altura da janela menos o tamanho do quadrado.
    square_size = 100
    max_x = window_width - square_size
    max_y = window_height - square_size
    running = True
    while running:
        random_r = random.randint(0, 255)
        random_g = random.randint(0, 255)
        random_b = random.randint(0, 255)
        random_color = (random_r, random_g, random_b, 255) # fixa 255 para não transparente
        pico_app.pico_set_style(PICO_FILL)
        
        pico_app.pico_output_clear() # Limpa a tela para preto
        pico_app.pico_set_color(random_color) # Define a cor aleatória
        square_x = random.randint(0, max_x)
        square_y = random.randint(0, max_y)
        square_rect = (square_x, square_y, square_size, square_size)
        pico_app.pico_output_draw_rect(square_rect) # Desenha o quadrado
        pico_app.pico_output_present() # Mostra o quadrado
        
        print("Quadrado visível. Esperando 1 segundo...")
        pico_app.pico_input_delay(1000) # Espera 1 segundo

        # Apaga o quadrado (limpa a tela)
        pico_app.pico_output_clear() # Limpa a tela para preto
        pico_app.pico_output_present() # Mostra a tela limpa

        print("Quadrado invisível. Esperando 1 segundo...")
        pico_app.pico_input_delay(1000) # Espera 1 segundo

        # Verifica se o usuário fechou a janela durante a espera
        event = sdl2.SDL_Event()
        while pico_app.pico_input_event_ask(event, sdl2.SDL_QUIT):
            if event.type == sdl2.SDL_QUIT:
                running = False

        if not running:
            break

    pico_app.pico_init(0)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())