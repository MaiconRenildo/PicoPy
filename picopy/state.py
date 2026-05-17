from .settings import Settings

class PicoState:
    def __init__(self):
        self.anchor_pos: tuple[int, int] = (Settings.POS_CENTER, Settings.POS_MIDDLE)
        self.anchor_rotate: tuple[int, int] = (Settings.POS_CENTER, Settings.POS_MIDDLE)
        self.angle: float = 0
        self.clip: tuple[int, int, int, int] = Settings.CLIP_RESET
        # color.clear / color.draw
        self.color_clear: tuple[int, int, int, int] = (0, 0, 0, 255)
        self.color_draw: tuple[int, int, int, int] = (255, 255, 255, 255)
        self.crop: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.cursor_x: bool = False
        self.cursor_cur: tuple[int, int] = (0, 0)
        self.expert: int = 0
        self.flip: tuple[int, int] = (0, 0)
        self.font_ttf = None
        self.font_h: int = 0
        self.fullscreen: bool = False
        self.grid: bool = True  # S.grid = 1 no C
        self.scroll: tuple[int, int] = (0, 0)
        self.style = Settings.DRAW_FILL
        self.scale: tuple[int, int] = (100, 100)
        self.zoom: tuple[int, int] = (100, 100)
        # PICO_DIM_PHY / PICO_DIM_LOG (pico.h); size.org/cur zerados no C até set_size
        self.dim_window = Settings.DIM_WINDOW
        self.dim_world = Settings.DIM_WORLD
        self.grid_world_unit: int = 1
