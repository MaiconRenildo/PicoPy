from constants import PICO_FILL, PICO_STROKE
from pico import PicoPy

def test_draw_oval_fill():
    """Testa o desenho de uma oval preenchida"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_FILL)
        Pico.pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_oval_fill.png")
    finally:
        Pico.pico_init(0)

def test_draw_oval_stroke():
    """Testa o desenho de uma oval contornada"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_STROKE)
        Pico.pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_oval_stroke.png")
    finally:
        Pico.pico_init(0)

