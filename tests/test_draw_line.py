from pico import pico_init, pico_output_clear, pico_output_draw_line
from .utils import screenshot_and_compare


def test_draw_line():
    """Testa o desenho de linhas (horizontal, vertical e diagonal)"""
    pico_init(1)
    try:
        pico_output_clear()

        # Linha Horizontal
        pico_output_draw_line((10, 5), (50, 5))
        
        # Linha Vertical
        pico_output_draw_line((5, 10), (5, 30))
        
        # Linha Diagonal
        pico_output_draw_line((10, 10), (50, 30))
        
        screenshot_and_compare("draw_line.png")
    finally:
        pico_init(0)
