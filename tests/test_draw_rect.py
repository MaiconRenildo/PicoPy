from tests.base_test import PicoTestBase


class TestDrawRect(PicoTestBase):
    """Classe de teste para operações de desenho de retângulos."""
    
    def test_draw_rect_fill(self):
        """Testa o desenho de um retângulo preenchido"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_FILL)
        self.pico.output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_rect_fill.png")

    def test_draw_rect_stroke(self):
        """Testa o desenho de um retângulo contornado"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_STROKE)
        self.pico.output_draw_rect((27, 17, 40, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_rect_stroke.png")
