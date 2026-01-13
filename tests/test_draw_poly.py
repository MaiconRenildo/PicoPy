from pico import pico_init, pico_output_clear, pico_output_draw_poly, pico_set_style
from constants import PICO_FILL, PICO_STROKE
from .utils import screenshot_and_compare

def test_draw_triangle_fill_by_poly_function():
    """Testa o desenho de um triângulo preenchido"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_FILL)
        pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        screenshot_and_compare("draw_triangle_fill_by_poly_function.png")
    finally:
        pico_init(0)

def test_draw_triangle_stroke_by_poly_function():
    """Testa o desenho de um triângulo contornado"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_STROKE)
        pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        screenshot_and_compare("draw_triangle_stroke_by_poly_function.png")
    finally:
        pico_init(0)

def test_draw_square_fill_by_poly_function():
    """Testa o desenho de um quadrado preenchido"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_FILL)
        pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        screenshot_and_compare("draw_square_fill_by_poly_function.png")
    finally:
        pico_init(0)

def test_draw_square_stroke_by_poly_function():
    """Testa o desenho de um quadrado contornado"""
    pico_init(1)
    try:
        pico_output_clear()
        pico_set_style(PICO_STROKE)
        pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        screenshot_and_compare("draw_square_stroke_by_poly_function.png")
    finally:
        pico_init(0)

