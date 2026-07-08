import time
import random

from picopy.pico import PicoPy

###### Classes ######
class GameObject:
    """Base class for all game objects."""
    def __init__(self, x: float, y: float, w: int, h: int, color: tuple, speed: float = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.speed = speed
        self.active = True # Used for bullets, enemies, etc.

    def get_rect_tuple(self) -> tuple[int, int, int, int]:
        """Returns the object's position and dimensions as a tuple (x, y, w, h)."""
        return (int(self.x), int(self.y), self.w, self.h)

    def draw(self, pico: PicoPy):
        """Draws the game object as a rectangle."""
        if self.active:
            pico.set_color(self.color)
            pico.set_style(pico.DRAW_FILL)
            pico.output_draw_rect(self.get_rect_tuple())

    def is_colliding_with(self, other_object: 'GameObject') -> bool:
        """Checks for collision with another game object."""
        r1_x, r1_y, r1_w, r1_h = self.get_rect_tuple()
        r2_x, r2_y, r2_w, r2_h = other_object.get_rect_tuple()
        return (r1_x < r2_x + r2_w and
                r1_x + r1_w > r2_x and
                r1_y < r2_y + r2_h and
                r1_y + r1_h > r2_y)


class Player(GameObject):
    """Represents the player's ship."""
    def __init__(self, x: float, y: float, w: int, h: int, color: tuple, speed: float):
        super().__init__(x, y, w, h, color, speed)

    def move(self, dx: float, dy: float, world_width: int, world_height: int):
        """Moves the player and limits movement within world bounds."""
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Limit player movement within the world bounds
        self.x = max(0, min(self.x, world_width - self.w))
        self.y = max(0, min(self.y, world_height - self.h))

    def draw(self, pico: PicoPy):
        """Draws the player as a mathematically symmetrical triangular ship."""
        if self.active:
            pico.set_color(self.color)
            pico.set_style(pico.DRAW_FILL)
            
            # Extrai os componentes convertendo uma única vez para performance
            x, y, w, h = int(self.x), int(self.y), self.w, self.h
            
            player_vertices = [
                (x + w // 2, y),      # Top center (Bico da nave)
                (x, y + h),           # Bottom-left
                (x + w, y + h)        # Bottom-right
            ]
            pico.output_draw_poly(player_vertices, 3)


class Bullet(GameObject):
    """Represents a bullet fired by the player."""
    def __init__(self, x: float, y: float, w: int, h: int, color: tuple, speed: float):
        super().__init__(x, y, w, h, color, speed)

    def update(self):
        """Moves the bullet upwards."""
        self.y -= self.speed
        if self.y < 0: # Deactivate if leaves screen
            self.active = False


class Enemy(GameObject):
    """Represents an enemy ship."""
    def __init__(self, x: float, y: float, w: int, h: int, color: tuple, speed: float):
        super().__init__(x, y, w, h, color, speed)

    def update(self, direction: int):
        """Moves the enemy horizontally."""
        self.x += self.speed * direction


###### Functions ######
def create_enemies_wave(pico: PicoPy, wave_number: int, world_width: int, world_height: int) -> list[Enemy]:
    # --- Enemy Wave Generation Constants (Local to function) ---
    BASE_ENEMY_COLS = 6
    MAX_ENEMY_COLS = 15
    BASE_ENEMY_ROWS = 3
    MAX_ENEMY_ROWS = 6
    ENEMY_WAVE_WIDTH, ENEMY_WAVE_HEIGHT = 3, 2
    ENEMY_WAVE_SPACING_X, ENEMY_WAVE_SPACING_Y = 6, 5
    INITIAL_ENEMY_WAVE_Y = 5
    BASE_ENEMY_WAVE_MOVE_SPEED = 0.5
    ENEMY_WAVE_SPEED_MULTIPLIER = 0.1

    enemies = []
    enemy_cols = min(BASE_ENEMY_COLS + wave_number, MAX_ENEMY_COLS)
    enemy_rows = min(BASE_ENEMY_ROWS + wave_number // 2, MAX_ENEMY_ROWS)
    enemy_w, enemy_h = ENEMY_WAVE_WIDTH, ENEMY_WAVE_HEIGHT
    enemy_spacing_x, enemy_spacing_y = ENEMY_WAVE_SPACING_X, ENEMY_WAVE_SPACING_Y
    enemy_move_speed = BASE_ENEMY_WAVE_MOVE_SPEED + wave_number * ENEMY_WAVE_SPEED_MULTIPLIER
    formation_width = enemy_cols * enemy_w + (enemy_cols - 1) * (enemy_spacing_x - enemy_w)
    start_x_offset = (world_width - formation_width) // 2

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            ex = start_x_offset + col * enemy_spacing_x
            ey = INITIAL_ENEMY_WAVE_Y + row * enemy_spacing_y
            enemies.append(Enemy(ex, ey, enemy_w, enemy_h, pico.COLOR_RED, enemy_move_speed))
    return enemies

def reset_game_anchor(pico: PicoPy):
    """Resets the global alignment, rotation anchor, and angle to defaults."""
    pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))
    pico.set_anchor_rotate((pico.POS_LEFT, pico.POS_TOP))
    pico.set_angle(0)

def load_high_score() -> tuple[int, str]:
    """Loads the high score and the holder's name. Returns (0, '---') if empty."""
    try:
        with open("highscore.txt", "r") as file:
            data = file.read().strip().split(",")
            if len(data) == 2:
                return int(data[0]), data[1]
    except (FileNotFoundError, ValueError):
        pass
    return 0, "---"

def save_high_score(new_high_score: int, holder_name: str):
    """Saves the new highest score and the holder's name to a file."""
    try:
        with open("highscore.txt", "w") as file:
            file.write(f"{new_high_score},{holder_name}")
    except IOError:
        print("Error: Could not save high score to file.")


#### Constants ####
FRAME_DELAY_MS = 16
SHOT_COOLDOWN_MS = 200 
POINTS_PER_ENEMY = 10

# Movement directions
DIR_RIGHT, DIR_LEFT = 1, -1

# Player constants
PLAYER_WIDTH, PLAYER_HEIGHT = 4, 4
PLAYER_INITIAL_SPEED = 1

# Bullet constants
BULLET_WIDTH, BULLET_HEIGHT = 1, 2
BULLET_SPEED = 1

# Enemy constants
ENEMY_DESCENT_AMOUNT = 0.5

# Interface and font constants
GAME_OVER_FONT_SIZE = 8
SCORE_FONT_SIZE = 8
TITLE_FONT_SIZE = 8 
GAME_OVER_MESSAGE_DELAY_MS = 3000

# Game States
STATE_MENU, STATE_PLAYING, STATE_PAUSE, STATE_RECORD_INPUT = 0, 1, 2, 3

pico = PicoPy()
pico.set_title("Space Invaders")
world_width, world_height = pico.get_dim_world()
pico.init(True)

# Initialize player
initial_player_x, initial_player_y = pico.pos(
    (pico.POS_CENTER, pico.POS_BOTTOM),
    offset=(0, -(PLAYER_HEIGHT * 2)) 
)
player_x, player_y = initial_player_x, initial_player_y
player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, pico.COLOR_GREEN, PLAYER_INITIAL_SPEED)

# Initialize player bullets
player_bullets: list[Bullet] = []
last_shot_time = 0

# Initialize score and load ranking/record from file
score = 0
high_score, high_score_name = load_high_score()
new_record_name = ""       # Stores characters during input state
last_key_pressed = None    # Keyboard debounce control

# Initialize enemies and waves
current_wave = 1
enemies: list[Enemy] = create_enemies_wave(pico, current_wave, world_width, world_height)
enemy_direction = DIR_RIGHT
enemy_vertical_move_amount = ENEMY_DESCENT_AMOUNT

running = True
game_over = False
game_state = STATE_MENU  
return_pressed = False   
event = pico.new_event_object()
random.seed(time.time())

print("Control the ship with LEFT/RIGHT arrows. Shoot with SPACE. Destroy the enemies! If enemies hit you or reach the bottom, it's Game Over.")

while running:
    
    # Close the game if the X of the window is clicked or if the ESC key is pressed
    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event) or pico.is_key_event(event, pico.SCANCODE_ESCAPE):
            running = False

    # Lógica de clique único para a tecla ENTER (RETURN)
    key_return = pico.get_key(pico.SCANCODE_RETURN)
    released_return = False
    if key_return and not return_pressed:
        return_pressed = True
        released_return = True
    elif not key_return:
        return_pressed = False

    # --- Sistema Nativo de Captura de Letras (Debounce) ---
    pressed_char = None
    if game_state == STATE_RECORD_INPUT:
        for code in range(pico.SCANCODE_A, pico.SCANCODE_Z + 1):
            if pico.get_key(code):
                if last_key_pressed != code:  
                    last_key_pressed = code
                    pressed_char = chr(ord('A') + (code - pico.SCANCODE_A))
                break
        else:
            if not pico.get_key(pico.SCANCODE_BACKSPACE):
                last_key_pressed = None

    pico.output_clear()

    # --- 1. ESTADO: MENU INICIAL ---
    if game_state == STATE_MENU:
        pico.set_color(pico.COLOR_GREEN)
        pico.set_font(None, TITLE_FONT_SIZE)

        # Divisão do título de forma simétrica sem números mágicos
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_BOTTOM))
        y_offset = 0 if high_score == 0 else -SCORE_FONT_SIZE            
        mx, my = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE), offset=(0, y_offset))
        pico.output_draw_text((mx, my), "SPACE")
        
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
        pico.output_draw_text((mx, my), "INVADERS")

        # Exibição do Recorde Atual (Ranking persistente)
        if high_score > 0:
            pico.set_color(pico.COLOR_YELLOW)
            pico.set_font(None, SCORE_FONT_SIZE)
            pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
            pico.output_draw_text((mx, my + 8), f"HI-SCORE: {high_score}")
            mx, my = pico.pos((pico.POS_CENTER, pico.POS_TOP), offset=(0, SCORE_FONT_SIZE*2))
            pico.output_draw_text((mx, my + 8), f"BY {high_score_name}")

        if released_return:
            game_state = STATE_PLAYING

            score = 0
            current_wave = 1
            game_over = False
            enemy_direction = DIR_RIGHT
            enemies = create_enemies_wave(pico, current_wave, world_width, world_height)
            player_bullets.clear()
            player.x, player.y = initial_player_x, initial_player_y
            player.active = True

    # --- 2. ESTADO: PAUSE ---
    elif game_state == STATE_PAUSE:
        if released_return:
            game_state = STATE_PLAYING

        reset_game_anchor(pico)

        for enemy in enemies: enemy.draw(pico)
        for bullet in player_bullets: bullet.draw(pico)
        player.draw(pico)

        # Desenha o placar estático
        pico.set_color(pico.COLOR_WHITE)
        pico.set_font(None, SCORE_FONT_SIZE)
        score_x, score_y = pico.pos((pico.POS_RIGHT, pico.POS_TOP))
        pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_TOP))
        pico.output_draw_text((score_x, score_y), f"{score}")

        # Desenha o texto de PAUSE por cima
        pico.set_color(pico.COLOR_YELLOW)
        pico.set_font(None, TITLE_FONT_SIZE)
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
        px, py = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
        pico.output_draw_text((px, py), "PAUSE")

    # --- 3. ESTADO: EM JOGO ---
    elif game_state == STATE_PLAYING:
        if released_return and not game_over:
            game_state = STATE_PAUSE
        
        if not game_over:
            reset_game_anchor(pico)
            
            # Player movement
            if pico.get_key(pico.SCANCODE_LEFT):
                player.move(-1, 0, world_width, world_height)
            if pico.get_key(pico.SCANCODE_RIGHT):
                player.move(1, 0, world_width, world_height)

            # Shooting (Alinhado exatamente com o bico do triângulo)
            current_ticks = pico.get_ticks() 
            if pico.get_key(pico.SCANCODE_SPACE) and (current_ticks - last_shot_time > SHOT_COOLDOWN_MS):
                new_bullet_y = player.y
                new_bullet_x = player.x + (player.w // 2)
                new_bullet = Bullet(new_bullet_x, new_bullet_y, BULLET_WIDTH, BULLET_HEIGHT, pico.COLOR_YELLOW, BULLET_SPEED)
                player_bullets.append(new_bullet)
                last_shot_time = current_ticks
                
            for bullet in player_bullets:
                bullet.update() 
            player_bullets = [b for b in player_bullets if b.active]

            # --- Enemy Update & Edge Collision (DRY / Otimizado) ---
            active_enemies = [e for e in enemies if e.active]
            if active_enemies:
                min_enemy_x = min(e.x for e in active_enemies)
                max_enemy_x = max(e.x + e.w for e in active_enemies)
                max_enemy_y = max(e.y + e.h for e in active_enemies)
                speed = active_enemies[0].speed
                
                # Validação de colisão nas bordas (com int() na direita para a física de trava)
                hit_right = (enemy_direction == DIR_RIGHT and max_enemy_x >= world_width - int(speed))
                hit_left  = (enemy_direction == DIR_LEFT  and min_enemy_x <= speed)
                
                if hit_right or hit_left:
                    enemy_direction *= -1 
                    for enemy in active_enemies: 
                        enemy.y += enemy_vertical_move_amount
                        
                for enemy in active_enemies:
                    enemy.update(enemy_direction) 

                # Game Over Logic
                if max_enemy_y >= player.y:
                    for enemy in active_enemies:
                        if player.is_colliding_with(enemy): 
                            game_over = True
                            print("GAME OVER: Enemy collided with player!")
                            break
                    if not game_over and max_enemy_y >= world_height - 1:
                        game_over = True
                        print("GAME OVER: Enemies reached the bottom of the screen!")

            else:
                # All enemies in wave destroyed, spawn next wave!
                current_wave += 1
                enemies = create_enemies_wave(pico, current_wave, world_width, world_height)
                enemy_direction = DIR_RIGHT
                print(f"Starting Wave {current_wave}!")

            # Collision Detection (Player Bullet vs. Enemy)
            for bullet in player_bullets:
                if not bullet.active:
                    continue
                for enemy in enemies:
                    if not enemy.active: 
                        continue
                    if bullet.is_colliding_with(enemy):
                        bullet.active = False
                        enemy.active = False
                        score += POINTS_PER_ENEMY 
                        break

        # --- Drawing All Elements ---
        pico.set_style(pico.DRAW_FILL)

        if not game_over:
            reset_game_anchor(pico)
            
            for enemy in enemies: enemy.draw(pico)
            for bullet in player_bullets: bullet.draw(pico)
            player.draw(pico)
            
            # --- Desenhar Pontuação (Canto Superior Direito) ---
            pico.set_color(pico.COLOR_WHITE)
            pico.set_font(None, SCORE_FONT_SIZE)
            score_x, score_y = pico.pos((pico.POS_RIGHT, pico.POS_TOP))
            
            pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_TOP))
            pico.set_anchor_rotate((pico.POS_RIGHT, pico.POS_TOP))
            pico.output_draw_text((score_x, score_y), f"{score}")
        else:
            # --- Desenhar Interface de Game Over de Forma Limpa ---
            pico.set_color(pico.COLOR_WHITE)
            pico.set_font(None, GAME_OVER_FONT_SIZE)
            text_pos_x, text_pos_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
            
            pico.set_anchor_pos((pico.POS_CENTER, pico.POS_BOTTOM))
            pico.output_draw_text((text_pos_x, text_pos_y), "GAME OVER!")

            pico.set_font(None, SCORE_FONT_SIZE)
            pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
            pico.output_draw_text((text_pos_x, text_pos_y), f"Score: {score}")
            
            pico.output_present()
            pico.input_delay(GAME_OVER_MESSAGE_DELAY_MS) 
            
            # Redirecionamento de estado dependendo do recorde
            if score > high_score:
                new_record_name = "" 
                game_state = STATE_RECORD_INPUT 
            else:
                score = 0
                game_over = False
                game_state = STATE_MENU

    # --- 4. ESTADO: ENTRADA DE RECORDE ---
    elif game_state == STATE_RECORD_INPUT:
        pico.set_color(pico.COLOR_YELLOW)
        pico.set_font(None, TITLE_FONT_SIZE)
        mx, my = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
        
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_BOTTOM))
        pico.output_draw_text((mx, my), "NEW ")

        pico.set_font(None, SCORE_FONT_SIZE)
        
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
        pico.output_draw_text((mx, my), "HIGH SCORE!")

        # Lógica de exclusão de caracteres (Backspace)
        if pico.get_key(pico.SCANCODE_BACKSPACE):
            if last_key_pressed != pico.SCANCODE_BACKSPACE:
                new_record_name = new_record_name[:-1]
                last_key_pressed = pico.SCANCODE_BACKSPACE
        
        # Acrescenta novos caracteres respeitando o limite máximo de 5
        if pressed_char and len(new_record_name) < 5:
            new_record_name += pressed_char

        # Desenha o nome do jogador exatamente uma linha abaixo da instrução
        pico.set_color(pico.COLOR_WHITE)
        _, name_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE), offset=(0, SCORE_FONT_SIZE))
        pico.output_draw_text((mx, name_y), new_record_name if new_record_name else "_____")

        # Grava os dados finais em disco ao apertar Enter
        if released_return and len(new_record_name) > 0:
            high_score = score
            high_score_name = new_record_name
            save_high_score(high_score, high_score_name)
            
            # Reseta as flags mecânicas e retorna ao menu inicial
            score = 0
            game_over = False
            game_state = STATE_MENU

    pico.output_present()
    pico.input_delay(FRAME_DELAY_MS)

# --- Finalization ---
pico.init(False)
print("Space Invaders game shut down.")