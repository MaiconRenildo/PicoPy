import os
from pico import pico_init
from .utils import get_expected_image_path, capture_screenshot_for_comparison, compare_images


def test_init_black_screen():
    """Testa a inicialização do pico-sdl e verifica se a tela está preta comparando com imagem de referência"""
    expected_image_path = get_expected_image_path("black_screen.png")
    pico_init(1)
    try:
        tmp_path = capture_screenshot_for_comparison(expected_image_path)
        if tmp_path is None:
            return  
        compare_images(tmp_path, expected_image_path)
        os.unlink(tmp_path) # Remove arquivo temporário  
    finally:
        pico_init(0)
