from tests.base_test import PicoTestBase


class TestDrawOval(PicoTestBase):
    """Classe de teste para operações de desenho de ovais."""
    
    def test_draw_oval_fill(self):
        """Testa o desenho de uma oval preenchida"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_FILL)
        self.pico.output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_oval_fill.png")

    def test_draw_oval_stroke(self):
        """Testa o desenho de uma oval contornada"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_STROKE)
        self.pico.output_draw_oval((30, 20, 50, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_oval_stroke.png")
