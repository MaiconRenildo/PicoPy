from tests.base_test import PicoTestBase


class TestInit(PicoTestBase):
    """Classe de teste para inicialização do PicoPy."""
    
    def test_init_black_screen(self):
        """Testa a inicialização do pico-sdl e verifica se a tela está preta comparando com imagem de referência"""
        self.utils.screenshot_and_compare("black_screen.png")
