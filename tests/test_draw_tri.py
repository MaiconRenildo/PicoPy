from tests.base_test import PicoTestBase


class TestDrawTri(PicoTestBase):
    """Classe de teste para operações de desenho de triângulos."""
    
    def test_draw_tri_fill(self):
        """Testa o desenho de um triângulo preenchido"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_FILL)
        self.pico.output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_tri_fill.png")

    def test_draw_tri_stroke(self):
        """Testa o desenho de um triângulo contornado"""
        self.pico.output_clear()
        self.pico.set_style(self.pico.DRAW_STROKE)
        self.pico.output_draw_tri((30, 20, 40, 20)) # x, y, w, h
        self.screenshot_and_compare("draw_tri_stroke.png")
