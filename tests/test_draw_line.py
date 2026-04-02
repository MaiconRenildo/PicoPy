from tests.base_test import PicoTestBase


class TestDrawLine(PicoTestBase):
    """Classe de teste para operações de desenho de linha."""
    
    def test_draw_line(self):
        """Testa o desenho de linhas (horizontal, vertical e diagonal)"""
        self.pico.output_clear()

        # Linha Horizontal
        self.pico.output_draw_line((10, 5), (50, 5))
        
        # Linha Vertical
        self.pico.output_draw_line((5, 10), (5, 30))
        
        # Linha Diagonal
        self.pico.output_draw_line((10, 10), (50, 30))
        
        self.screenshot_and_compare("draw_line.png")
