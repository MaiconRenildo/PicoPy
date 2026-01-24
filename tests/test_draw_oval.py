from constants import PICO_FILL, PICO_STROKE
from tests.base_test import PicoTestBase


class TestDrawOval(PicoTestBase):
    """Classe de teste para operações de desenho de ovais."""
    
    def test_draw_oval_fill(self):
        """Testa o desenho de uma oval preenchida"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_FILL)
        self.utils.pico.pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_oval_fill.png")

    def test_draw_oval_stroke(self):
        """Testa o desenho de uma oval contornada"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_STROKE)
        self.utils.pico.pico_output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_oval_stroke.png")
