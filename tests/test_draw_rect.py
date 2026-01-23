
from constants import PICO_FILL, PICO_STROKE
from pico import PicoPy

def test_draw_rect_fill():
    """Testa o desenho de um retângulo preenchido"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_FILL)
        Pico.pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_rect_fill.png")
    finally:
        Pico.pico_init(0)

def test_draw_rect_stroke():
    """Testa o desenho de um retângulo contornado"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_STROKE)
        Pico.pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        Pico.screenshot_and_compare("draw_rect_stroke.png")
    finally:
        Pico.pico_init(0)

