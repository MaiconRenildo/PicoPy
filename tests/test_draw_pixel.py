from pico import PicoPy

def test_draw_pixel():
    """Testa o desenho de pixels e verifica se a imagem gerada corresponde à referência"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()

        Pico.pico_output_draw_pixel((32, 18)) # (64/2, 36/2)
        Pico.pico_output_draw_pixel((30, 18))
        Pico.pico_output_draw_pixel((34, 18))
        Pico.pico_output_draw_pixel((32, 16))
        Pico.pico_output_draw_pixel((32, 20))
        
        Pico.pico_output_draw_pixel((5, 5))
        Pico.pico_output_draw_pixel((59, 5))
        Pico.pico_output_draw_pixel((5, 31))
        Pico.pico_output_draw_pixel((59, 31))
        
        Pico.screenshot_and_compare("draw_pixel.png")
    finally:
        Pico.pico_init(0)

def test_draw_pixels():
    """Testa o desenho de múltiplos pixels usando pico_output_draw_pixels"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()
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
        Pico.pico_output_draw_pixels(pixels)
        Pico.screenshot_and_compare("draw_pixel.png")
    finally:
        Pico.pico_init(0)

def test_draw_diagonal_pixels():
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        original_dim_window = Pico.pico_get_dim_window()
        original_dim_world = Pico.pico_get_dim_world()
        Pico.pico_set_dim_window((160, 160))
        Pico.pico_set_dim_world((16, 16))
        Pico.pico_set_zoom((100, 100))
        for i in range(16):
            Pico.pico_output_draw_pixel((i, i))
            Pico.pico_output_draw_pixel((15 - i, i))
        Pico.pico_output_present()
        Pico.screenshot_and_compare("diagonal_pixels.png")
    finally:
        Pico.pico_set_dim_window(original_dim_window)
        Pico.pico_set_dim_world(original_dim_world)
        Pico.pico_init(0)