from pico import PicoPy

def test_draw_line():
    """Testa o desenho de linhas (horizontal, vertical e diagonal)"""
    Pico = PicoPy()
    Pico.pico_init(1)
    try:
        Pico.pico_output_clear()

        # Linha Horizontal
        Pico.pico_output_draw_line((10, 5), (50, 5))
        
        # Linha Vertical
        Pico.pico_output_draw_line((5, 10), (5, 30))
        
        # Linha Diagonal
        Pico.pico_output_draw_line((10, 10), (50, 30))
        
        Pico.screenshot_and_compare("draw_line.png")
    finally:
        Pico.pico_init(0)
