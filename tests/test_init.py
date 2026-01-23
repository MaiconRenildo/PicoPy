from pico import PicoPy

def test_init_black_screen():
    """Testa a inicialização do pico-sdl e verifica se a tela está preta comparando com imagem de referência"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.screenshot_and_compare("black_screen.png")
    finally:
        Pico.pico_init(0)
