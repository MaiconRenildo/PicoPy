from pico import pico_init, pico_output_clear, pico_output_draw_pixel, pico_output_draw_pixels
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
