import os
import sys
import time
import sdl2
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pico import PicoPy
from constants import PICO_CENTER, PICO_FILL, PICO_ANY, PICO_MIDDLE

# --- Cores --- #
PLAYER_COLOR = (0, 255, 0, 255)  # Verde
BULLET_COLOR = (255, 255, 0, 255) # Amarelo
ENEMY_COLOR = (255, 0, 0, 255)   # Vermelho
BACKGROUND_COLOR = (0, 0, 0, 255) # Preto
WHITE_COLOR = (255, 255, 255, 255)

# --- Configurações do Jogo --- #
FPS = 60
FRAME_DELAY_MS = 16

# --- Funções Auxiliares --- #
def check_collision(rect1: tuple[int, int, int, int], rect2: tuple[int, int, int, int]) -> bool:
    """Verifica colisão entre dois retângulos (quadrados) representados por tuplas."""
    r1_x, r1_y, r1_w, r1_h = rect1
    r2_x, r2_y, r2_w, r2_h = rect2

    return (
        r1_x < r2_x + r2_w and
        r1_x + r1_w > r2_x and
        r1_y < r2_y + r2_h and
        r1_y + r1_h > r2_y
    )

# Função para criar uma onda de inimigos
def create_enemies_wave(wave_number: int, window_width: int, window_height: int) -> list[dict]:
    enemies = []
    # Aumenta o número de colunas a cada onda, até um limite
    enemy_cols = min(8 + wave_number, 15) # Exemplo: max 15 colunas
    enemy_rows = min(3 + wave_number // 2, 6) # Exemplo: max 6 linhas
    enemy_w, enemy_h = 25, 20
    enemy_spacing_x, enemy_spacing_y = 40, 30
    initial_enemy_y = 50 # Posição Y inicial para a primeira linha de inimigos
    
    # Aumenta a velocidade dos inimigos a cada onda
    enemy_move_speed = 2 + wave_number * 0.5 # Exemplo: 0.5 a mais de velocidade por onda

    # Calcula a largura total da formação de inimigos
    formation_width = enemy_cols * enemy_w + (enemy_cols - 1) * (enemy_spacing_x - enemy_w)
    # Centraliza a formação na tela
    start_x_offset = (window_width - formation_width) // 2

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            ex = start_x_offset + col * enemy_spacing_x
            ey = initial_enemy_y + row * enemy_spacing_y
            enemies.append({
                'x': ex,
                'y': ey,
                'w': enemy_w,
                'h': enemy_h,
                'color': ENEMY_COLOR,
                'speed': enemy_move_speed,
                'active': True
            })
    return enemies

# --- Função Principal do Jogo --- #
def main():
    pico_app = PicoPy()
    pico_app.pico_init(1)

    # Configurações iniciais da janela e do mundo
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    pico_app.pico_set_dim_window((WINDOW_WIDTH, WINDOW_HEIGHT))
    pico_app.pico_set_dim_world((WINDOW_WIDTH, WINDOW_HEIGHT)) # Mundo 1:1 com a janela
    pico_app.pico_set_zoom((100, 100))
    pico_app.pico_set_anchor_pos((0, 0)) # Anchor no canto superior esquerdo para facilitar o posicionamento
    pico_app.pico_set_scroll((0, 0))

    # --- Inicialização do Jogador --- #
    player_w, player_h = 30, 20
    player_x = (WINDOW_WIDTH - player_w) // 2
    player_y = WINDOW_HEIGHT - player_h - 10 # Perto da base da tela
    player_speed = 5

    player = {
        'x': player_x,
        'y': player_y,
        'w': player_w,
        'h': player_h,
        'color': PLAYER_COLOR,
        'speed': player_speed
    }
    player_rect = (player['x'], player['y'], player['w'], player['h']) # Adiciona para colisões

    # --- Inicialização dos Tiros do Jogador --- #
    player_bullets = []
    bullet_w, bullet_h = 4, 10
    bullet_speed = 10
    last_shot_time = 0 # Para controlar a taxa de disparo
    SHOT_COOLDOWN_MS = 200 # 200ms entre tiros

    # --- Inicialização dos Inimigos e Ondas --- #
    current_wave = 1
    enemies = create_enemies_wave(current_wave, WINDOW_WIDTH, WINDOW_HEIGHT)
    enemy_direction = 1 # INICIALIZAÇÃO AQUI: 1 para direita, -1 para esquerda

    running = True
    game_over = False # Nova variável de estado do jogo
    event = sdl2.SDL_Event()
    random.seed(time.time())

    print("Controle a nave com as setas. Atire com ESPAÇO. Destrua os inimigos! Se os inimigos te atingirem ou chegarem ao fim da tela, é Game Over.")

    # --- Loop Principal do Jogo --- #
    while running and not game_over: # Loop continua enquanto não for Game Over
        # --- Processamento de Eventos (SDL_QUIT) ---
        while pico_app.pico_input_event_ask(event, PICO_ANY):
            if int(event.type) == sdl2.SDL_QUIT:
                running = False

        # --- Lógica de Input do Jogador (Movimento e Tiro) ---
        # Movimento lateral do jogador
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_LEFT):
            player['x'] -= player['speed']
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_RIGHT):
            player['x'] += player['speed']

        # Limitar movimento do jogador na tela
        player['x'] = max(0, min(player['x'], WINDOW_WIDTH - player['w'])) # Usar player['w'] aqui
        player_rect = (player['x'], player['y'], player['w'], player['h']) # Atualiza o player_rect

        # Tiro do jogador
        current_time = sdl2.SDL_GetTicks() # Tempo em milissegundos
        if pico_app.pico_get_key(sdl2.SDL_SCANCODE_SPACE) and (current_time - last_shot_time > SHOT_COOLDOWN_MS):
            new_bullet_x = player['x'] + (player['w'] - bullet_w) // 2 # Centro do jogador
            new_bullet_y = player['y']
            player_bullets.append({
                'x': new_bullet_x,
                'y': new_bullet_y,
                'w': bullet_w,
                'h': bullet_h,
                'color': BULLET_COLOR,
                'speed': bullet_speed,
                'active': True
            })
            last_shot_time = current_time

        # --- Atualização de Tiros do Jogador ---
        # Mover tiros e remover os que saem da tela
        for bullet in player_bullets:
            bullet['y'] -= bullet['speed']
        player_bullets = [b for b in player_bullets if b['y'] > 0 and b['active']]

        # --- Atualização de Inimigos (Movimento Horizontal) ---
        active_enemies = [e for e in enemies if e['active']]
        if active_enemies:
            min_enemy_x = min(e['x'] for e in active_enemies)
            max_enemy_x = max(e['x'] + e['w'] for e in active_enemies)
            max_enemy_y = max(e['y'] + e['h'] for e in active_enemies) # Pega a posição Y mais baixa dos inimigos

            # A velocidade do inimigo agora é pega de um inimigo ativo qualquer, já que todos têm a mesma speed
            current_enemy_speed = active_enemies[0]['speed'] if active_enemies else 0

            # Checa se a formação de inimigos atingiu as bordas da tela
            if enemy_direction == 1 and max_enemy_x >= WINDOW_WIDTH - current_enemy_speed: # Perto da borda direita
                enemy_direction = -1
                for enemy in active_enemies: enemy['y'] += 20
            elif enemy_direction == -1 and min_enemy_x <= current_enemy_speed: # Perto da borda esquerda
                enemy_direction = 1
                for enemy in active_enemies: enemy['y'] += 20

            # Mover todos os inimigos ativos na direção atual
            for enemy in active_enemies:
                enemy['x'] += enemy['speed'] * enemy_direction

            # --- Lógica de Game Over: Inimigos atingindo o jogador ou o fundo da tela ---
            if max_enemy_y >= player['y'] - 5: # Inimigo muito perto ou colidindo com a linha do jogador
                # Ou se algum inimigo colidiu diretamente com o jogador
                for enemy in active_enemies:
                    enemy_rect = (enemy['x'], enemy['y'], enemy['w'], enemy['h'])
                    if check_collision(player_rect, enemy_rect):
                        game_over = True
                        print("GAME OVER: Inimigo colidiu com o jogador!")
                        break # Sai do loop de inimigos
                if not game_over and max_enemy_y >= WINDOW_HEIGHT - 10: # Se inimigo passou do limite inferior
                    game_over = True
                    print("GAME OVER: Inimigos atingiram o fim da tela!")

        else:
            # Todos os inimigos da onda foram destruídos, gera a próxima onda!
            current_wave += 1
            enemies = create_enemies_wave(current_wave, WINDOW_WIDTH, WINDOW_HEIGHT)
            enemy_direction = 1 # Reseta a direção para a nova onda
            print(f"Iniciando Onda {current_wave}!")
        # --- Detecção de Colisões (Tiro do Jogador vs. Inimigo) ---
        for bullet in player_bullets:
            if not bullet['active']: continue
            for enemy in enemies:
                if not enemy['active']: continue
                bullet_rect = (bullet['x'], bullet['y'], bullet['w'], bullet['h'])
                enemy_rect = (enemy['x'], enemy['y'], enemy['w'], enemy['h'])
                if check_collision(bullet_rect, enemy_rect):
                    bullet['active'] = False
                    enemy['active'] = False
                    break # Tiro atingiu um inimigo, não precisa checar outros
        # Remover balas e inimigos marcados como inativos/atingidos
        player_bullets = [b for b in player_bullets if b['active']]
        enemies = [e for e in enemies if e['active']]
        # --- Desenho de Todos os Elementos ---
        pico_app.pico_output_clear() # Limpa a tela
        pico_app.pico_set_style(PICO_FILL) # Desenha preenchido
        if not game_over:
            # Desenha inimigos
            pico_app.pico_set_color(ENEMY_COLOR)
            for enemy in enemies:
                pico_app.pico_output_draw_rect((enemy['x'], enemy['y'], enemy['w'], enemy['h']))

            # Desenha tiros do jogador
            pico_app.pico_set_color(BULLET_COLOR)
            for bullet in player_bullets:
                pico_app.pico_output_draw_rect((bullet['x'], bullet['y'], bullet['w'], bullet['h']))

            # Desenha jogador (formato de nave triangular)
            pico_app.pico_set_color(PLAYER_COLOR)
            # Definir os vértices do triângulo para a nave
            player_vertices = [
                (player['x'] + player['w'] // 2, player['y']),           # Topo central
                (player['x'], player['y'] + player['h']),               # Base esquerda
                (player['x'] + player['w'], player['y'] + player['h'])  # Base direita
            ]
            pico_app.pico_output_draw_poly(player_vertices, len(player_vertices))
            pico_app.pico_output_present() # Mostra o frame
        else:
            pico_app.pico_set_color(WHITE_COLOR) # Branco
            font_size = 40
            pico_app.pico_set_font(None, font_size)
            # Obtém as dimensões do mundo para centralizar o texto
            world_w, world_h = pico_app.pico_get_dim_world()
            center_x = world_w // 2
            center_y = world_h // 2
            # Define a ancoragem para o centro do texto
            pico_app.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
            pico_app.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            pico_app.pico_set_angle(0) # Assegura que o texto não esteja rotacionado
            pico_app.pico_output_draw_text((center_x, center_y), "GAME OVER!")
            pico_app.pico_output_present()
            pico_app.pico_input_delay(5000)
        pico_app.pico_input_delay(FRAME_DELAY_MS) # Controla o FPS
    # --- Finalização --- #
    pico_app.pico_init(0)
    print("Jogo Space Invaders desligado.")

if __name__ == "__main__":
    sys.exit(main())
