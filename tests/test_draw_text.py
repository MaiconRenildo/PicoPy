from tests.base_test import PicoTestBase

class TestDrawText(PicoTestBase):
    """Classe de teste para operações de desenho de texto."""

    DEFAULT_FONT_SIZE = 10

    def test_draw_text_basic(self):
        """Testa o desenho de texto básico com a fonte padrão."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP)), "PicoPy!")
        self.screenshot_and_compare("draw_text_basic.png")

    def test_draw_text_centered(self):
        """Testa o desenho de texto centralizado no meio da janela."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE)), "Centralized!")
        self.screenshot_and_compare("draw_text_centered.png")

    def test_draw_text_in_top_and_centered_with_custom_color(self):
        """Testa o desenho de texto com uma cor personalizada, centralizado horizontalmente."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_GREEN)
        world_w, _ = self.pico.get_dim_world()
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_TOP))
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_CENTER, self.pico.POS_TOP)), "Green Text!")
        self.screenshot_and_compare("draw_text_green_in_top_and_centered.png")


    def test_draw_text_in_bottom_and_centered_with_custom_color(self):
        """Testa o desenho de texto com uma cor personalizada, centralizado horizontalmente."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_GREEN)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_BOTTOM))
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_CENTER, self.pico.POS_BOTTOM)), "Green Text!")
        self.screenshot_and_compare("draw_text_green_in_bottom_and_centered.png")


    def test_draw_text_rotated(self):
        """Testa o desenho de texto rotacionado."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_MAGENTA)
        original_angle = self.pico.get_angle()
        original_anchor_rotate = self.pico.get_anchor_rotate()
        original_anchor_pos = self.pico.get_anchor_pos()
        try:
            self.pico.set_anchor_rotate((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
            self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))

            self.pico.set_angle(45)

            self.pico.output_draw_text(self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE)), "PicoPy")
            self.screenshot_and_compare("draw_text_rotated_45.png")
            
            self.pico.output_clear()

            self.pico.set_angle(90)
            self.pico.output_draw_text(self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE)), "PicoPy")
            self.screenshot_and_compare("draw_text_rotated_90.png")

        finally:
            self.pico.set_angle(original_angle)
            self.pico.set_anchor_rotate(original_anchor_rotate)
            self.pico.set_anchor_pos(original_anchor_pos)


    def test_draw_text_aligned_right_with_90_angle(self):
        """Testa o desenho de texto alinhado à borda direita da janela com ângulo de 90 graus."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_YELLOW)
        original_anchor_pos = self.pico.get_anchor_pos()
        try:
            self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_MIDDLE))
            self.pico.set_anchor_rotate((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
            self.pico.set_angle(90)
            self.pico.output_draw_text(self.pico.pos((self.pico.POS_RIGHT, self.pico.POS_MIDDLE), offset=(self.DEFAULT_FONT_SIZE, 0)), "PicoPy") # Offset para empurrar o texto para a direita, compensando o tamanho da fonte
            self.screenshot_and_compare("draw_text_aligned_right_90.png")
        finally:
            self.pico.set_anchor_pos(original_anchor_pos)

    def test_draw_text_aligned_right_with_minus_90_angle(self):
        """Testa o desenho de texto alinhado à borda direita da janela com ângulo de -90 graus."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_YELLOW)
        original_anchor_pos = self.pico.get_anchor_pos()
        try:
            self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_MIDDLE))
            self.pico.set_anchor_rotate((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
            self.pico.set_angle(-90)
            self.pico.output_draw_text(self.pico.pos((self.pico.POS_RIGHT, self.pico.POS_MIDDLE), offset=(self.DEFAULT_FONT_SIZE, 0)), "PicoPy") # Offset para empurrar o texto para a direita, compensando o tamanho da fonte
            self.screenshot_and_compare("draw_text_aligned_right_minus_90.png")
        finally:
            self.pico.set_anchor_pos(original_anchor_pos)


    def test_draw_text_aligned_left_with_90_angle(self):
        """Testa o desenho de texto alinhado à borda esquerda da janela com ângulo de 90 graus."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_YELLOW)
        original_anchor_pos = self.pico.get_anchor_pos()
        try:
            self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_MIDDLE))
            self.pico.set_anchor_rotate((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
            self.pico.set_angle(90)
            self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_MIDDLE), offset=(-self.DEFAULT_FONT_SIZE, 0)), "PicoPy") # Offset para empurrar o texto para a esquerda, compensando o tamanho da fonte
            self.screenshot_and_compare("draw_text_aligned_left_90.png")
        finally:
            self.pico.set_anchor_pos(original_anchor_pos)

    def test_draw_text_aligned_left_with_minus_90_angle(self):
        """Testa o desenho de texto alinhado à borda esquerda da janela com ângulo de -90 graus."""
        self.pico.set_font(None, self.DEFAULT_FONT_SIZE)
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_YELLOW)
        original_anchor_pos = self.pico.get_anchor_pos()
        try:
            self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_MIDDLE))
            self.pico.set_anchor_rotate((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
            self.pico.set_angle(-90)
            self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_MIDDLE), offset=(-self.DEFAULT_FONT_SIZE, 0)), "PicoPy") # Offset para empurrar o texto para a esquerda, compensando o tamanho da fonte
            self.screenshot_and_compare("draw_text_aligned_left_minus_90.png")
        finally:
            self.pico.set_anchor_pos(original_anchor_pos)

    def test_draw_text_multiple_lines(self):
        """Testa o desenho de múltiplas linhas de texto em posições diferentes."""
        self.pico.output_clear()
        font_size = self.DEFAULT_FONT_SIZE
        self.pico.set_font(None, font_size)
        self.pico.set_color(self.pico.COLOR_YELLOW)
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP)), "First Line")
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP), offset=(0, self.DEFAULT_FONT_SIZE)), "Second Line") # Offset para a segunda linha
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP), offset=(0, self.DEFAULT_FONT_SIZE * 2)), "Third Line")
        self.screenshot_and_compare("draw_text_multiline.png")

    def test_draw_text_empty_string(self):
        """Testa o desenho de uma string vazia (não deve renderizar nada)."""
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.output_draw_text(self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP), offset=(10, 10)), "")
        self.screenshot_and_compare("draw_text_empty_string.png")