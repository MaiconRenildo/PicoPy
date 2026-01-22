from pico import pico_init, pico_output_clear, pico_output_draw_pixel, pico_output_draw_pixels, pico_get_dim_window, pico_set_dim_window, pico_get_dim_world, pico_set_dim_world, pico_set_zoom, pico_output_present
from .utils import screenshot_and_compare


def test_draw_pixel():
    """Testa o desenho de pixels e verifica se a imagem gerada corresponde à referência"""
    pico_init(1)
    try:
        pico_output_clear()

        pico_output_draw_pixel((32, 18)) # (64/2, 36/2)
        pico_output_draw_pixel((30, 18))
        pico_output_draw_pixel((34, 18))
        pico_output_draw_pixel((32, 16))
        pico_output_draw_pixel((32, 20))
        
        pico_output_draw_pixel((5, 5))
        pico_output_draw_pixel((59, 5))
        pico_output_draw_pixel((5, 31))
        pico_output_draw_pixel((59, 31))
        
        screenshot_and_compare("draw_pixel.png")
    finally:
        pico_init(0)

def test_draw_pixels():
    """Testa o desenho de múltiplos pixels usando pico_output_draw_pixels"""
    pico_init(1)
    try:
        pico_output_clear()
        pixels = [
            (32, 18),  # (64/2, 36/2)
            (30, 18),
            (34, 18),
            (32, 16),
            (32, 20),
            (5, 5),
            (59, 5),
            (5, 31),
            (59, 31),
        ]
        pico_output_draw_pixels(pixels)
        screenshot_and_compare("draw_pixel.png")
    finally:
        pico_init(0)

def test_draw_diagonal_pixels():
    pico_init(1)
    try:
        original_dim_window = pico_get_dim_window()
        original_dim_world = pico_get_dim_world()
        pico_set_dim_window((160, 160))
        pico_set_dim_world((16, 16))
        pico_set_zoom((100, 100))
        for i in range(16):
            pico_output_draw_pixel((i, i))
            pico_output_draw_pixel((15 - i, i))
        pico_output_present()
        screenshot_and_compare("diagonal_pixels.png")
    finally:
        pico_set_dim_window(original_dim_window)
        pico_set_dim_world(original_dim_world)
        pico_init(0)