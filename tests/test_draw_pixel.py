from pico import pico_init, pico_output_clear, pico_output_draw_pixel
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

