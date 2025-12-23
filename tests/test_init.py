from pico import pico_init
from .utils import screenshot_and_compare


def test_init_black_screen():
    """Testa a inicialização do pico-sdl e verifica se a tela está preta comparando com imagem de referência"""
    pico_init(1)
    try:
        screenshot_and_compare("black_screen.png")
    finally:
        pico_init(0)
