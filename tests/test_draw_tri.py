from constants import PICO_FILL, PICO_STROKE
from tests.base_test import PicoTestBase


class TestDrawTri(PicoTestBase):
    """Classe de teste para operações de desenho de triângulos."""
    
    def test_draw_tri_fill(self):
        """Testa o desenho de um triângulo preenchido"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_FILL)
        self.utils.pico.pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_tri_fill.png")

    def test_draw_tri_stroke(self):
        """Testa o desenho de um triângulo contornado"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_STROKE)
        self.utils.pico.pico_output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_tri_stroke.png")
