import os
import sys
import sdl2
import random
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pico import PicoPy
from constants import PICO_FILL, PICO_ANY

def colisao_rects(rect_a_tuple: tuple[int, int, int, int], rect_b_tuple: tuple[int, int, int, int]) -> bool:
    """Verifica colisão entre dois retângulos (quadrados) representados por tuplas."""
    rect_a = sdl2.SDL_Rect(*rect_a_tuple)
    rect_b = sdl2.SDL_Rect(*rect_b_tuple)
    return (rect_a.x < rect_b.x + rect_b.w and
            rect_a.x + rect_a.w > rect_b.x and
            rect_a.y < rect_b.y + rect_b.h and
            rect_a.y + rect_a.h > rect_b.y)

def colisao(quadrado_jogador_tuple: tuple[int, int, int, int], quadrados_vermelhos_list: list[tuple[int, int, int, int]], consumidos: list[int]):
    """Marca quadrados vermelhos como consumidos após colisão com o jogador."""
    for i in range(len(quadrados_vermelhos_list)):
        if not consumidos[i] and colisao_rects(quadrado_jogador_tuple, quadrados_vermelhos_list[i]):
            consumidos[i] = 1  # Marca como consumido

def main():
    pico_app = PicoPy()
    pico_app.pico_init(1)
    
    # Configura o tamanho da janela e do mundo
    pico_app.pico_set_dim_window((800, 600))
    pico_app.pico_set_dim_world((800, 600)) # O mundo lógico é igual ao tamanho da janela
    # pico_app.pico_set_zoom((100, 100)) # Sem zoom
    # pico_app.pico_set_anchor_pos((0, 0)) # Define o anchor no canto superior esquerdo
    # pico_app.pico_set_scroll((0, 0)) # Sem scroll inicial

    random.seed(time.time())

    # Posição inicial do quadrado amarelo (jogador)
    x, y = 400, 300
    tamanho = 10 # Tamanho do quadrado
    velocidade = 5 # Adicionado para controlar a velocidade do jogador
    quadrado_jogador_tuple = (x, y, tamanho, tamanho)

    # Inicializa os quadrados vermelhos e vetor de consumidos
    num_quadrados_vermelhos = 10
    consumidos = [0] * num_quadrados_vermelhos
    quadrados_vermelhos_list = [] # Armazena como tuplas (x, y, w, h)
    for _ in range(num_quadrados_vermelhos):
        qx = random.randint(0, 800 - tamanho)
        qy = random.randint(0, 600 - tamanho)
        quadrados_vermelhos_list.append((qx, qy, tamanho, tamanho))

    running = True
    event = sdl2.SDL_Event() # Objeto de evento SDL2

    # Marca o tempo inicial para o cronômetro
    tempo_inicio = time.time()

    print("Controle o quadrado amarelo com WASD. Colete os vermelhos. Você tem 30 segundos!")

    while running:
        # Verifica se os 30 segundos já passaram
        agora = time.time()
        if (agora - tempo_inicio) >= 30:
            print("VOCÊ PERDEU!")
            running = False
            break

        # Verifica se o jogador venceu (todos os quadrados foram consumidos)
        venceu = True
        for i in range(num_quadrados_vermelhos):
            if consumidos[i] == 0:
                venceu = False
                break
        
        if venceu:
            print("VOCÊ GANHOU!")
            running = False
            break

        # Processa os eventos (teclado e fechamento de janela)
        while pico_app.pico_input_event_ask(event, PICO_ANY):
            if event.type == sdl2.SDL_QUIT:
                running = False
        
        # --- Lógica de Movimento Baseada no Estado do Teclado ---
        # Verifica o estado atual das teclas (não eventos 'KEYDOWN')
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_W): # Verifica se W está pressionado
            y -= velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_S): # Verifica se S está pressionado
            y += velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_A): # Verifica se A está pressionado
            x -= velocidade
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_D): # Verifica se D está pressionado
            x += velocidade
        
        # Atualiza a posição do quadrado amarelo
        quadrado_jogador_tuple = (x, y, tamanho, tamanho)

        # Verifica colisão com os quadrados vermelhos
        colisao(quadrado_jogador_tuple, quadrados_vermelhos_list, consumidos)

        # Limpa a tela (define cor de fundo preta)
        pico_app.pico_output_clear() # Limpa a tela com a cor de fundo padrão (preto)

        # Desenha os quadrados vermelhos restantes
        for i in range(num_quadrados_vermelhos):
            if not consumidos[i]:
                pico_app.pico_set_color((255, 0, 0, 255)) # Cor vermelha
                pico_app.pico_set_style(PICO_FILL)
                pico_app.pico_output_draw_rect(quadrados_vermelhos_list[i])

        # Desenha o quadrado amarelo (jogador)
        pico_app.pico_set_color((255, 255, 0, 255)) # Cor amarela
        pico_app.pico_set_style(PICO_FILL)
        pico_app.pico_output_draw_rect(quadrado_jogador_tuple)

        # Atualiza a tela
        pico_app.pico_output_present()

        pico_app.pico_input_delay(16)  # Aproximadamente 60 FPS

    # Desinicializa o PicoPy ao sair do loop
    pico_app.pico_init(0)
    print("PicoPy desligado.")

if __name__ == "__main__":
    sys.exit(main())
