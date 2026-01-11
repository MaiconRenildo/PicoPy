from pico import pico_init, pico_output_clear, pico_output_draw_rect, pico_set_style
from constants import PICO_FILL, PICO_STROKE
from .utils import screenshot_and_compare

def test_draw_rect_fill():
    """Testa o desenho de um retângulo preenchido"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_FILL)
        pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        screenshot_and_compare("draw_rect_fill.png")
    finally:
        pico_init(0)

def test_draw_rect_stroke():
    """Testa o desenho de um retângulo contornado"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_STROKE)
        pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        screenshot_and_compare("draw_rect_stroke.png")
    finally:
        pico_init(0)

