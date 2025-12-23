import os
from pico import pico_init, pico_output_clear, pico_output_draw_pixel, pico_output_present
from .utils import get_expected_image_path, capture_screenshot_for_comparison, compare_images


def test_draw_pixel():
    """Testa o desenho de pixels e verifica se a imagem gerada corresponde à referência"""
    expected_image = get_expected_image_path("draw_pixel.png")
    pico_init(1)
    try:
        # Limpa a tela antes de desenhar os pixels
        pico_output_clear()

        pico_output_draw_pixel((32, 18)) # (64/2, 36/2)
        pico_output_draw_pixel((30, 18))
        pico_output_draw_pixel((34, 18))
        pico_output_draw_pixel((32, 16))
        pico_output_draw_pixel((32, 20))
        
        pico_output_draw_pixel((5, 5))
        pico_output_draw_pixel((59, 5))
        pico_output_draw_pixel((5, 31))
        pico_output_draw_pixel((59, 31))
        
        tmp_path = capture_screenshot_for_comparison(expected_image)
        if tmp_path is None:
            return
        compare_images(tmp_path, expected_image)
        os.unlink(tmp_path)  # Remove arquivo temporário
    finally:
        pico_init(0)

