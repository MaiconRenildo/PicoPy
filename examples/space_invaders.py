import sys
import time
import sdl2
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
def create_enemies_wave(pico: PicoPy, wave_number: int, world_width: int, world_height: int) -> list[Enemy]:
    enemies = []
    enemy_cols = min(6 + wave_number, 15)
    enemy_rows = min(3 + wave_number // 2, 6)
    enemy_w, enemy_h = 3, 2
    enemy_spacing_x, enemy_spacing_y = 6, 5
    initial_enemy_y = 5
    enemy_move_speed = 0.5 + wave_number * 0.1
    formation_width = enemy_cols * enemy_w + (enemy_cols - 1) * (enemy_spacing_x - enemy_w)
    start_x_offset = (world_width - formation_width) // 2

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            ex = start_x_offset + col * enemy_spacing_x
            ey = initial_enemy_y + row * enemy_spacing_y
            enemies.append(Enemy(ex, ey, enemy_w, enemy_h, pico.COLOR_RED, enemy_move_speed)) # Using Colors class
    return enemies


def main():
    # constants
    FRAME_DELAY_MS = 16
    SHOT_COOLDOWN_MS = 200 # 200ms between shots


    pico = PicoPy()
    pixels_per_world_unit = 10
    window_width, window_height = pico.get_display_resolution()
    world_width = window_width // pixels_per_world_unit
    world_height = window_height // pixels_per_world_unit
    pico.set_dim_window((window_width, window_height))
    pico.set_dim_world((world_width, world_height))
    pico.init(True, fullscreen=True)

    # Initialize player
    player_w, player_h = 4,4
    player_x, player_y = pico.pos(
        (pico.POS_CENTER, pico.POS_BOTTOM),
        offset=(0, -(player_h * 2)) # negative offset to move up from the bottom
    )
    player = Player(player_x, player_y, player_w, player_h, pico.COLOR_GREEN, 1)

    # Inicialize player bullets
    player_bullets: list[Bullet] = []
    bullet_w, bullet_h = 1, 2
    bullet_speed = 1
    last_shot_time = 0

    # Inicialize enemies e waves
    current_wave = 1
    enemies: list[Enemy] = create_enemies_wave(pico, current_wave, world_width, world_height)
    enemy_direction = 1 # 1 for right, -1 for left
    enemy_vertical_move_amount = 0.5

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
            player.move(-1, 0, world_width, world_height)
        if pico.get_key(pico.SCANCODE_RIGHT):
            player.move(1, 0, world_width, world_height)

        # Shooting
        current_ticks = pico.get_ticks() # Time in milliseconds
        if pico.get_key(pico.SCANCODE_SPACE) and (current_ticks - last_shot_time > SHOT_COOLDOWN_MS):
            new_bullet_y = player.y
            new_bullet_x = player.x + (player.w - bullet_w) // 2
            new_bullet = Bullet(new_bullet_x, new_bullet_y, bullet_w, bullet_h, pico.COLOR_YELLOW, bullet_speed)
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
            if enemy_direction == 1 and max_enemy_x >= world_width - int(current_enemy_speed):
                enemy_direction = -1
                for enemy in active_enemies: enemy.y += enemy_vertical_move_amount
            elif enemy_direction == -1 and min_enemy_x <= current_enemy_speed:
                enemy_direction = 1
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
            enemies = create_enemies_wave(pico, current_wave, world_width, world_height)
            enemy_direction = 1
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
                enemy.draw(pico)
            # Draw player bullets
            for bullet in player_bullets:
                bullet.draw(pico) # Using Bullet.draw
            # Draw player
            player.draw(pico) # Using Player.draw
            pico.output_present()
        else:
            pico.output_clear()
            pico.set_color(pico.COLOR_WHITE) # Using Colors class
            pico.set_font(None, 10) # Assuming font size 10 is appropriate for GAME OVER text
            text_pos_x, text_pos_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
            # Set anchor for text drawing (important for centering)
            pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
            pico.set_anchor_rotate((pico.POS_CENTER, pico.POS_MIDDLE))
            pico.set_angle(0)
            pico.output_draw_text(text_pos_x, "GAME OVER!")
            pico.output_present()
            pico.input_delay(5000) # Keep game over message on screen for 5 seconds

        pico.input_delay(FRAME_DELAY_MS)

    # --- Finalization ---
    pico.init(False)
    print("Space Invaders game shut down.")

if __name__ == "__main__":
    sys.exit(main())