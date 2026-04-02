from tests.base_test import PicoTestBase


class TestDrawPixel(PicoTestBase):
    """Classe de teste para operações de desenho de pixels."""
    
    def test_draw_pixel(self):
        """Testa o desenho de pixels e verifica se a imagem gerada corresponde à referência"""
        self.pico.output_clear()

        self.pico.output_draw_pixel((32, 18)) # (64/2, 36/2)
        self.pico.output_draw_pixel((30, 18))
        self.pico.output_draw_pixel((34, 18))
        self.pico.output_draw_pixel((32, 16))
        self.pico.output_draw_pixel((32, 20))
        
        self.pico.output_draw_pixel((5, 5))
        self.pico.output_draw_pixel((59, 5))
        self.pico.output_draw_pixel((5, 31))
        self.pico.output_draw_pixel((59, 31))
        
        self.screenshot_and_compare("draw_pixel.png")

    def test_draw_pixels(self):
        """Testa o desenho de múltiplos pixels usando pico_output_draw_pixels"""
        self.pico.output_clear()
        pixels = [
            (32, 18),  # (64/2, 36/2)
            (30, 18),
            (34, 18),
            (32, 16),
            (32, 20),
            (5, 5),
            (59, 5),
            (5, 31),
            (59, 31),
        ]
        self.pico.output_draw_pixels(pixels)
        self.screenshot_and_compare("draw_pixel.png")

    def test_draw_diagonal_pixels(self):
        """Testa o desenho de pixels diagonais"""
        original_dim_window = self.pico.get_dim_window()
        original_dim_world = self.pico.get_dim_world()
        self.pico.set_dim_window((160, 160))
        self.pico.set_dim_world((16, 16))
        self.pico.set_zoom((100, 100))
        for i in range(16):
            self.pico.output_draw_pixel((i, i))
            self.pico.output_draw_pixel((15 - i, i))
        self.pico.output_present()
        self.screenshot_and_compare("diagonal_pixels.png")
        # Restaura dimensões originais (a fixture fará o cleanup do pico_init)
        self.pico.set_dim_window(original_dim_window)
        self.pico.set_dim_world(original_dim_world)
