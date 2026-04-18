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

    def draw(self):
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

    def draw(self):
        """Draws the player as a triangular ship."""
        if self.active:
            pico.set_color(self.color)
            pico.set_style(pico.DRAW_FILL)
            
            # Define vertices for a triangular ship shape
            player_vertices = [
                (int(self.x + self.w // 2), int(self.y)),             # Top center
                (int(self.x), int(self.y + self.h)),                 # Bottom-left
                (int(self.x + self.w), int(self.y + self.h))         # Bottom-right
            ]
            pico.output_draw_poly(player_vertices, len(player_vertices))


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
        # Enemies might have additional properties, e.g., points, type, etc.

    def update(self, direction: int):
        """Moves the enemy horizontally."""
        self.x += self.speed * direction


###### Functions ######
def create_enemies_wave(wave_number: int, world_width: int, world_height: int) -> list[Enemy]:
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
            enemies.append(Enemy(ex, ey, enemy_w, enemy_h, pico.COLOR_RED, enemy_move_speed)) # Using Colors class
    return enemies


#### constants ####
FRAME_DELAY_MS = 16
SHOT_COOLDOWN_MS = 200 # 200ms between shots

# player constants
PLAYER_WIDTH = 4
PLAYER_HEIGHT = 4
PLAYER_INITIAL_SPEED = 1
PLAYER_START_Y_PCT = 90
NO_VERTICAL_MOVEMENT = 0

# bullet constants
BULLET_WIDTH = 1
BULLET_HEIGHT = 2
BULLET_SPEED = 1

# enemy constants
ENEMY_DESCENT_AMOUNT = 0.5

# game over constants
GAME_OVER_FONT_SIZE = 10
GAME_OVER_MESSAGE_DELAY_MS = 5000

# direction constants
DIRECTION_RIGHT = 1
DIRECTION_LEFT = -1

pico = PicoPy()
pixels_per_world_unit = 10
window_width, window_height = pico.get_display_resolution()
world_width = window_width // pixels_per_world_unit
world_height = window_height // pixels_per_world_unit
pico.set_dim_window((window_width, window_height))
pico.set_dim_world((world_width, world_height))
pico.init(True, fullscreen=True)

# Initialize player
player_x, player_y = pico.pos((pico.POS_CENTER, PLAYER_START_Y_PCT))
player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, pico.COLOR_GREEN, PLAYER_INITIAL_SPEED)

# Inicialize player bullets
player_bullets: list[Bullet] = []
last_shot_time = 0

# Inicialize enemies e waves
current_wave = 1
enemies: list[Enemy] = create_enemies_wave(current_wave, world_width, world_height)
enemy_direction = DIRECTION_RIGHT
enemy_vertical_move_amount = ENEMY_DESCENT_AMOUNT

running = True
game_over = False
event = pico.new_event_object()
random.seed(time.time())

print("Control the ship with WASD. Shoot with SPACE. Destroy the enemies! If enemies hit you or reach the bottom, it's Game Over.")

while running and not game_over:
    
    # Close the game if the X of the window is clicked or if the ESC key is pressed
    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event) or pico.is_key_event(event, pico.SCANCODE_ESCAPE):
            running = False

    # Player movement
    if pico.get_key(pico.SCANCODE_LEFT):
        player.move(DIRECTION_LEFT, NO_VERTICAL_MOVEMENT, world_width, world_height)
    if pico.get_key(pico.SCANCODE_RIGHT):
        player.move(DIRECTION_RIGHT, NO_VERTICAL_MOVEMENT, world_width, world_height)

    # Shooting
    current_ticks = pico.get_ticks() # Time in milliseconds
    if pico.get_key(pico.SCANCODE_SPACE) and (current_ticks - last_shot_time > SHOT_COOLDOWN_MS):
        new_bullet_y = player.y
        new_bullet_x = player.x + (player.w - BULLET_WIDTH) // 2
        new_bullet = Bullet(new_bullet_x, new_bullet_y, BULLET_WIDTH, BULLET_HEIGHT, pico.COLOR_YELLOW, BULLET_SPEED)
        player_bullets.append(new_bullet)
        last_shot_time = current_ticks
    for bullet in player_bullets:
        bullet.update() # move the bullet upwards
    player_bullets = [b for b in player_bullets if b.active]

    # --- Enemy Update (Horizontal Movement) ---
    active_enemies = [e for e in enemies if e.active]
    if active_enemies:
        min_enemy_x = min(e.x for e in active_enemies)
        max_enemy_x = max(e.x + e.w for e in active_enemies)
        max_enemy_y = max(e.y + e.h for e in active_enemies)
        current_enemy_speed = active_enemies[0].speed if active_enemies else 0
        if enemy_direction == DIRECTION_RIGHT and max_enemy_x >= world_width - int(current_enemy_speed):
            enemy_direction = DIRECTION_LEFT
            for enemy in active_enemies: enemy.y += enemy_vertical_move_amount
        elif enemy_direction == DIRECTION_LEFT and min_enemy_x <= current_enemy_speed:
            enemy_direction = DIRECTION_RIGHT
            for enemy in active_enemies: enemy.y += enemy_vertical_move_amount
        for enemy in active_enemies:
            enemy.update(enemy_direction) # Using Enemy.update

        # Game Over Logic: Enemies hitting player or bottom
        if max_enemy_y >= player.y:
            for enemy in active_enemies:
                if player.is_colliding_with(enemy): # Using Player.is_colliding_with
                    game_over = True
                    print("GAME OVER: Enemy collided with player!")
                    break
            if not game_over and max_enemy_y >= world_height - 1:
                game_over = True
                print("GAME OVER: Enemies reached the bottom of the screen!")

    else:
        # All enemies in wave destroyed, spawn next wave!
        current_wave += 1
        enemies = create_enemies_wave(current_wave, world_width, world_height)
        enemy_direction = DIRECTION_RIGHT
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
                break

    # --- Drawing All Elements ---
    pico.output_clear()
    pico.set_style(pico.DRAW_FILL)

    if not game_over:
        # Draw enemies
        for enemy in enemies:
            enemy.draw()
        # Draw player bullets
        for bullet in player_bullets:
            bullet.draw() # Using Bullet.draw
        # Draw player
        player.draw() # Using Player.draw
        pico.output_present()
    else:
        pico.output_clear()
        pico.set_color(pico.COLOR_WHITE) # Using Colors class
        pico.set_font(None, GAME_OVER_FONT_SIZE) # Assuming font size 10 is appropriate for GAME OVER text
        text_pos_x, text_pos_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
        # Set anchor for text drawing (important for centering)
        pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
        pico.set_anchor_rotate((pico.POS_CENTER, pico.POS_MIDDLE))
        pico.set_angle(0)
        pico.output_draw_text((text_pos_x, text_pos_y), "GAME OVER!")
        pico.output_present()
        pico.input_delay(GAME_OVER_MESSAGE_DELAY_MS) # Keep game over message on screen for 5 seconds

    pico.input_delay(FRAME_DELAY_MS)

# --- Finalization ---
pico.init(False)
print("Space Invaders game shut down.")