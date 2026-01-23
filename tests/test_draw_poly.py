from constants import PICO_FILL, PICO_STROKE
from pico import PicoPy

def test_draw_triangle_fill_by_poly_function():
    """Testa o desenho de um triângulo preenchido"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_FILL)
        Pico.pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        Pico.screenshot_and_compare("draw_triangle_fill_by_poly_function.png")
    finally:
        Pico.pico_init(0)

def test_draw_triangle_stroke_by_poly_function():
    """Testa o desenho de um triângulo contornado"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_STROKE)
        Pico.pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        Pico.screenshot_and_compare("draw_triangle_stroke_by_poly_function.png")
    finally:
        Pico.pico_init(0)

def test_draw_square_fill_by_poly_function():
    """Testa o desenho de um quadrado preenchido"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_FILL)
        Pico.pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        Pico.screenshot_and_compare("draw_square_fill_by_poly_function.png")
    finally:
        Pico.pico_init(0)

def test_draw_square_stroke_by_poly_function():
    """Testa o desenho de um quadrado contornado"""
    Pico = PicoPy()
    Pico.pico_init(1)   
    try:
        Pico.pico_output_clear()
        Pico.pico_set_style(PICO_STROKE)
        Pico.pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        Pico.screenshot_and_compare("draw_square_stroke_by_poly_function.png")
    finally:
        Pico.pico_init(0)

