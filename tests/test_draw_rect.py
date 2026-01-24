from constants import PICO_FILL, PICO_STROKE
from tests.base_test import PicoTestBase


class TestDrawRect(PicoTestBase):
    """Classe de teste para operações de desenho de retângulos."""
    
    def test_draw_rect_fill(self):
        """Testa o desenho de um retângulo preenchido"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_FILL)
        self.utils.pico.pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_rect_fill.png")

    def test_draw_rect_stroke(self):
        """Testa o desenho de um retângulo contornado"""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_style(PICO_STROKE)
        self.utils.pico.pico_output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        self.utils.screenshot_and_compare("draw_rect_stroke.png")
