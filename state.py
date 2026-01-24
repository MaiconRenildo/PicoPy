from constants import (
    PICO_DIM_WINDOW,
    PICO_DIM_WORLD,
    PICO_CENTER,
    PICO_MIDDLE,
    PICO_FILL,
)

class PicoState:
    def __init__(self):
        # Anchor(ponto de referência)
        # Define qual ponto do objeto é usado como referência para posicionamento ao dar zoom/mover
        self.anchor_pos: tuple[int, int] = (PICO_CENTER, PICO_MIDDLE) # Por padrão, centraliza o objeto
        # Define qual ponto do objeto é usado como centro de rotação ao rotacionar algo
        self.anchor_rotate: tuple[int, int] = (PICO_CENTER, PICO_MIDDLE)
        
        self.angle = 0
        self.clip: tuple[int, int, int, int] = (0, 0, 0, 0)  # (x, y, w, h)
        self.color_clear: tuple[int, int, int, int] = (0, 0, 0, 255)  # (r, g, b, a) - preto
        self.color_draw: tuple[int, int, int, int] = (255, 255, 255, 255)  # branco
        self.crop: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.cursor_x = 0
        self.cursor_cur: tuple[int, int] = (0, 0)
        self.dim_window = PICO_DIM_WINDOW
        self.dim_world = PICO_DIM_WORLD
        self.expert = 0
        self.flip: tuple[int, int] = (0, 0)
        self.font_ttf = None
        self.font_h = 0
        self.fullscreen = 0
        self.grid = 1
        self.scroll: tuple[int, int] = (0, 0)
        self.style = PICO_FILL
        self.scale: tuple[int, int] = (100, 100)
        self.zoom: tuple[int, int] = (100, 100)