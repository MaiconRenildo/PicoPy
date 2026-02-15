from tests.base_test import PicoTestBase


class TestDrawBuffer(PicoTestBase):
    """Classe de teste para operações de desenho de buffer."""
    
    def test_draw_buffer_simple_square(self):
        """
        Testa o desenho de um buffer RGBA simples(um quadrado vermelho).
        """
        dim = (10, 10) # Define as dimensões do buffer -> 10x10
        # Cria um buffer RGBA para um quadrado vermelho
        red_pixel = (255, 0, 0, 255) # Cada pixel é (255, 0, 0, 255) para vermelho opaco
        buffer = [red_pixel] * (dim[0] * dim[1])
        pos = (10, 10)
        self.utils.pico.pico_output_draw_buffer(pos, buffer, dim)
        self.utils.screenshot_and_compare("test_draw_buffer_simple_square.png")

    def test_draw_buffer_with_transparent_pixel(self):
        """
        Testa o desenho de um buffer RGBA com um pixel transparente no centro.
        """
        buffer_w, buffer_h = 20, 20
        dim = (buffer_w, buffer_h)

        # Cria um buffer azul com um pixel transparente no centro
        blue_pixel = (0, 0, 255, 255)
        transparent_pixel = (0, 0, 0, 0)
        buffer: list[tuple[int, int, int, int]] = [blue_pixel] * (buffer_w * buffer_h)

        # Coloca um pixel transparente no centro
        # Ajustado para a esquerda e para cima
        center_x = buffer_w // 2 - 1
        center_y = buffer_h // 2 - 1
        # O cálculo do índice na lista linear
        offset_to_row_start = center_y * buffer_w
        buffer_index = offset_to_row_start + center_x
        buffer[buffer_index] = transparent_pixel
        pos = (0, 0) # Posição do canto superior esquerdo na tela
        self.utils.pico.pico_output_draw_buffer(pos, buffer, dim)
        self.utils.screenshot_and_compare("test_draw_buffer_with_transparent_pixel.png")

    def test_draw_buffer_with_offset_and_scale2(self):
        """
        Testa o desenho de um buffer na mesma posição com e sem zoom.
        """
        buffer_w, buffer_h = 10, 10
        dim = (buffer_w, buffer_h)
        green_pixel = (0, 255, 0, 255)
        buffer = [green_pixel] * (buffer_w * buffer_h)
        # --- Teste 1: Sem Zoom (100%) - Quadrado Centralizado ---
        self.utils.pico.pico_set_zoom((100, 100)) # Garante zoom padrão
        self.utils.pico.pico_output_clear() # Limpa a textura antes de desenhar
        # Posição centralizada para zoom 100%: (64//2 - 5, 36//2 - 5) = (27, 13)
        pos_centro = (27, 13)
        self.utils.pico.pico_output_draw_buffer(pos_centro, buffer, dim)

        self.utils.screenshot_and_compare("test_draw_buffer_fixed_pos_100_percent_zoom.png")

        # --- Teste 2: Zoom de 200%(Objeto deve ficar maior) ---
        self.utils.pico.pico_set_zoom((200, 200))
        self.utils.pico.pico_output_clear() # Limpa a textura antes de desenhar
        self.utils.pico.pico_output_draw_buffer(pos_centro, buffer, dim)
        self.utils.screenshot_and_compare("test_draw_buffer_fixed_pos_200_percent_zoom.png")

        # --- Teste 3: Zoom de 50%(Objeto deve ficar menor) ---
        self.utils.pico.pico_set_zoom((50, 50))
        self.utils.pico.pico_output_clear() # Limpa a textura antes de desenhar
        self.utils.pico.pico_output_draw_buffer(pos_centro, buffer, dim)
        self.utils.screenshot_and_compare("test_draw_buffer_fixed_pos_50_percent_zoom.png")
        # garante que o zoom seja restaurado para o padrão para não afetar outros testes
        self.utils.pico.pico_set_zoom((100, 100))
