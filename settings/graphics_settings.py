
class GraphicsSettings:
    DRAW_FILL: int = 0
    DRAW_STROKE: int = 1

    CLIP_RESET: tuple[int, int, int, int] = (0, 0, 0, 0)

    BYTES_PER_PIXEL_RGBA32: int = 4
    
    DIM_KEEP: tuple[int, int] = (0, 0)
    DIM_WINDOW: tuple[int, int] = (640, 360)
    DIM_WORLD: tuple[int, int] = (64, 36)

    WINDOW_TITLE: str = "pico-SDL"