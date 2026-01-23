
from constants import PICO_FILL, PICO_STROKE
from pico import PicoPy

def test_draw_tri_fill():
    """Testa o desenho de um triângulo preenchido"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_FILL)
        Pico.pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_tri_fill.png")
    finally:
        Pico.pico_init(0)

def test_draw_tri_stroke():
    """Testa o desenho de um triângulo contornado"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_STROKE)
        Pico.pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_tri_stroke.png")
    finally:
        Pico.pico_init(0)

