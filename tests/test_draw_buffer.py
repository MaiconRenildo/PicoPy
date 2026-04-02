from tests.base_test import PicoTestBase


class TestDrawBuffer(PicoTestBase):
    """Classe de teste para operações de desenho de buffer."""

    BUFFER_DIM_SMALL = (10, 10)
    BUFFER_DIM_MEDIUM = (20, 20)

    COLOR_RED = (255, 0, 0, 255)
    COLOR_BLUE = (0, 0, 255, 255)
    COLOR_GREEN = (0, 255, 0, 255)
    COLOR_TRANSPARENT = (0, 0, 0, 0)

    ZOOM_100_PERCENT = (100, 100)
    ZOOM_200_PERCENT = (200, 200)
    ZOOM_50_PERCENT = (50, 50)
    
    def test_draw_buffer_simple_square(self):
        """
        Testa o desenho de um buffer RGBA simples(um quadrado vermelho).
        """
        dim = self.BUFFER_DIM_SMALL # Define as dimensões do buffer -> 10x10
        # Cria um buffer RGBA para um quadrado vermelho
        red_pixel = self.COLOR_RED # Cada pixel é (255, 0, 0, 255) para vermelho opaco
        buffer = [red_pixel] * (dim[0] * dim[1])
        pos = self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP), offset=(10, 10))
        self.pico.output_draw_buffer(pos, buffer, dim)
        self.screenshot_and_compare("test_draw_buffer_simple_square.png")

    def test_draw_buffer_with_transparent_pixel(self):
        """
        Testa o desenho de um buffer RGBA com um pixel transparente no centro.
        """
        buffer_w, buffer_h = self.BUFFER_DIM_MEDIUM
        dim = (buffer_w, buffer_h)

        # Cria um buffer azul com um pixel transparente no centro
        blue_pixel = self.COLOR_BLUE
        transparent_pixel = self.COLOR_TRANSPARENT
        buffer: list[tuple[int, int, int, int]] = [blue_pixel] * (buffer_w * buffer_h)

        # Coloca um pixel transparente no centro
        # Ajustado para a esquerda e para cima
        center_x = buffer_w // 2 - 1
        center_y = buffer_h // 2 - 1
        # O cálculo do índice na lista linear
        offset_to_row_start = center_y * buffer_w
        buffer_index = offset_to_row_start + center_x
        buffer[buffer_index] = transparent_pixel
        pos = self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        self.pico.output_draw_buffer(pos, buffer, dim)
        self.screenshot_and_compare("test_draw_buffer_with_transparent_pixel.png")

    def test_draw_buffer_with_offset_and_scale2(self):
        """
        Testa o desenho de um buffer na mesma posição com e sem zoom.
        """
        buffer_w, buffer_h = self.BUFFER_DIM_SMALL
        dim = (buffer_w, buffer_h)
        green_pixel = self.COLOR_GREEN
        buffer = [green_pixel] * (buffer_w * buffer_h)
        # --- Teste 1: Sem Zoom (100%) - Quadrado Centralizado ---
        self.pico.set_zoom(self.ZOOM_100_PERCENT) # Garante zoom padrão
        self.pico.output_clear() # Limpa a textura antes de desenhar
        # Posição centralizada para zoom 100%: (64//2 - 5, 36//2 - 5) = (27, 13)
        pos_centro = (27, 13)
        self.pico.output_draw_buffer(pos_centro, buffer, dim)

        self.screenshot_and_compare("test_draw_buffer_fixed_pos_100_percent_zoom.png")

        # --- Teste 2: Zoom de 200%(Objeto deve ficar maior) ---
        self.pico.set_zoom(self.ZOOM_200_PERCENT)
        self.pico.output_clear() # Limpa a textura antes de desenhar
        self.pico.output_draw_buffer(pos_centro, buffer, dim)
        self.screenshot_and_compare("test_draw_buffer_fixed_pos_200_percent_zoom.png")

        # --- Teste 3: Zoom de 50%(Objeto deve ficar menor) ---
        self.pico.set_zoom(self.ZOOM_50_PERCENT)
        self.pico.output_clear() # Limpa a textura antes de desenhar
        self.pico.output_draw_buffer(pos_centro, buffer, dim)
        self.screenshot_and_compare("test_draw_buffer_fixed_pos_50_percent_zoom.png")
        # garante que o zoom seja restaurado para o padrão para não afetar outros testes
        self.pico.set_zoom(self.ZOOM_100_PERCENT)
