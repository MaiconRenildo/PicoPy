from constants import PICO_FILL, PICO_STROKE
from pico import pico_init, pico_output_clear, pico_output_draw_oval, pico_set_style, pico_set_style
from .utils import screenshot_and_compare

def test_draw_oval_fill():
    """Testa o desenho de uma oval preenchida"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_FILL)
        pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        screenshot_and_compare("draw_oval_fill.png")
    finally:
        pico_init(0)

def test_draw_oval_stroke():
    """Testa o desenho de uma oval contornada"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_STROKE)
        pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        screenshot_and_compare("draw_oval_stroke.png")
    finally:
        pico_init(0)

