from .settings import Settings

class PicoState:
    def __init__(self):
        # Anchor(ponto de referência)
        # Define qual ponto do objeto é usado como referência para posicionamento ao dar zoom/mover
        self.anchor_pos: tuple[int, int] = (Settings.POS_CENTER, Settings.POS_MIDDLE) # Por padrão, centraliza o objeto
        # Define qual ponto do objeto é usado como centro de rotação ao rotacionar algo
        self.anchor_rotate: tuple[int, int] = (Settings.POS_CENTER, Settings.POS_MIDDLE)
        
        self.angle: float = 0
        self.clip: tuple[int, int, int, int] = (0, 0, 0, 0)  # (x, y, w, h)
        self.color_clear: tuple[int, int, int, int] = (0, 0, 0, 255)  # (r, g, b, a) - preto
        self.color_draw: tuple[int, int, int, int] = (255, 255, 255, 255)  # branco
        self.crop: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.cursor_x: bool = False
        self.cursor_cur: tuple[int, int] = (0, 0)
        self.dim_window = Settings.DIM_WINDOW
        self.dim_world = Settings.DIM_WORLD
        self.expert = 0
        self.flip: tuple[int, int] = (0, 0)
        self.font_ttf = None
        self.font_h = 0
        self.fullscreen: bool = False
        self.grid: bool = True
        self.scroll: tuple[int, int] = (0, 0)
        self.style = Settings.DRAW_FILL
        self.scale: tuple[int, int] = (100, 100)
        self.zoom: tuple[int, int] = (100, 100)
        self.grid_world_unit: int = 20