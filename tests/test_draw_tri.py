
from constants import PICO_FILL, PICO_STROKE
from pico import pico_init, pico_output_clear, pico_output_draw_tri, pico_set_style
from .utils import screenshot_and_compare

def test_draw_tri_fill():
    """Testa o desenho de um triângulo preenchido"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_FILL)
        pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        screenshot_and_compare("draw_tri_fill.png")
    finally:
        pico_init(0)

def test_draw_tri_stroke():
    """Testa o desenho de um triângulo contornado"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_STROKE)
        pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        screenshot_and_compare("draw_tri_stroke.png")
    finally:
        pico_init(0)

