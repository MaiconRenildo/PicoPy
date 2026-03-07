import os
import sys
import sdl2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pico import PicoPy
from constants import PICO_FILL, PICO_ANY

def main():
    pico_app = PicoPy()
    
    # Inicializa o PicoPy
    pico_app.pico_init(1)
    
    # Configura o tamanho da janela e do mundo
    pico_app.pico_set_dim_window((800, 600))
    pico_app.pico_set_dim_world((800, 600))
    pico_app.pico_set_zoom((100, 100))
    pico_app.pico_set_anchor_pos((0, 0))
    pico_app.pico_set_scroll((0, 0))

    # Posição inicial do quadrado amarelo (jogador)
    x, y = 350, 250 # Posição inicial
    tamanho = 50     # Tamanho do quadrado
    velocidade = 5
    quadrado_jogador_tuple = (x, y, tamanho, tamanho)

    running = True
    event = sdl2.SDL_Event() # Objeto de evento SDL2

    print("Controle o quadrado amarelo com WASD. Pressione 'X' para sair.")

    while running:
        # --- Processamento de Eventos (para eventos como SDL_QUIT) ---
        while pico_app.pico_input_event_ask(event, PICO_ANY):
            if event.type == sdl2.SDL_QUIT:
                running = False
            # Pode processar outros eventos aqui que você queira reagir a cada ocorrência (ex: clique único)
        
        # --- Lógica de Movimento Baseada no Estado do Teclado ---
        # Esta seção AGORA ESTÁ NO MESMO NÍVEL DE INDENTAÇÃO do 'while running'
        # e será executada a cada frame, verificando se as teclas estão pressionadas.
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_W):
            y -= velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_S):
            y += velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_A):
            x -= velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_D):
            x += velocidade
        
        # ... (Restante da lógica do jogo: atualização da posição do quadrado, limpeza, desenho, apresentação) ...
        quadrado_jogador_tuple = (x, y, tamanho, tamanho)

        # Limpa a tela (define cor de fundo preta)
        pico_app.pico_output_clear()

        # Desenha o quadrado amarelo (jogador)
        pico_app.pico_set_color((255, 255, 0, 255)) # amarelo
        pico_app.pico_set_style(PICO_FILL)
        pico_app.pico_output_draw_rect(quadrado_jogador_tuple)

        # Atualiza a tela
        pico_app.pico_output_present()

        pico_app.pico_input_delay(16) # Aproximadamente 60 FPS

    # Desinicializa o PicoPy ao sair do loop
    pico_app.pico_init(0)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())