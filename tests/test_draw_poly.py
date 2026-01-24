from constants import PICO_FILL, PICO_STROKE
from tests.base_test import PicoTestBase


class TestDrawPoly(PicoTestBase):
    """Classe de teste para operações de desenho de polígonos."""
    
    def test_draw_triangle_fill_by_poly_function(self):
        """Testa o desenho de um triângulo preenchido"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_FILL)
        self.utils.pico.pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        self.utils.screenshot_and_compare("draw_triangle_fill_by_poly_function.png")

    def test_draw_triangle_stroke_by_poly_function(self):
        """Testa o desenho de um triângulo contornado"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_STROKE)
        self.utils.pico.pico_output_draw_poly([ (32, 5), (10, 30), (50, 30) ], 3)
        self.utils.screenshot_and_compare("draw_triangle_stroke_by_poly_function.png")

    def test_draw_square_fill_by_poly_function(self):
        """Testa o desenho de um quadrado preenchido"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_FILL)
        self.utils.pico.pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        self.utils.screenshot_and_compare("draw_square_fill_by_poly_function.png")

    def test_draw_square_stroke_by_poly_function(self):
        """Testa o desenho de um quadrado contornado"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_STROKE)
        self.utils.pico.pico_output_draw_poly([ (25, 15), (40, 15), (40, 30), (25, 30) ], 4)
        self.utils.screenshot_and_compare("draw_square_stroke_by_poly_function.png")
