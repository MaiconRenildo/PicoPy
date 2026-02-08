import os
from tests.base_test import PicoTestBase
from constants import PICO_CENTER, PICO_MIDDLE, PICO_LEFT, PICO_TOP, PICO_RIGHT, PICO_BOTTOM

# Definir as dimensões da janela e do mundo para os testes de ancoramento
TEST_WINDOW_DIM = (200, 200)
TEST_WORLD_DIM = (10, 10)

class TestAnchor(PicoTestBase):
    """Classe de teste para operações de ancoramento (anchor_pos)."""

    def setUp(self):
        super().setUp()
        self.utils.pico.pico_set_dim_window(TEST_WINDOW_DIM)
        self.utils.pico.pico_set_dim_world(TEST_WORLD_DIM)
        self.utils.pico.pico_set_zoom((100, 100)) # Zoom padrão para evitar complexidade inicial

    # PIXELS
    def test_pixel_centered_50x50_center_middle_anchor(self):
        """Testa um pixel centralizado com âncora CENTER/MIDDLE."""
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_pixel(pt)
        self.utils.pico.pico_output_present()
        # igual ao "/pixel50x50y_lefttop.png"
        self.utils.screenshot_and_compare("pixel50x50y_center.png")

    def test_pixel_centered_50x50_left_top_anchor(self):
        """Testa um pixel centralizado com âncora LEFT/TOP."""
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_TOP))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_pixel(pt)
        self.utils.pico.pico_output_present()
        # igual ao "/pixel50x50y_center.png"
        self.utils.screenshot_and_compare("pixel50x50y_lefttop.png")

    def test_pixel_centered_50x50_right_bottom_anchor(self):
        """Testa um pixel centralizado com âncora RIGHT/BOTTOM."""
        self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_BOTTOM))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_pixel(pt)
        self.utils.pico.pico_output_present()
        # 1 pixel para a esquerda e 1 para cima
        self.utils.screenshot_and_compare("pixel50x50y_rightbottom.png")

    # RECTS
    def test_rect_centered_exact_center_middle_anchor(self):
        """Testa um retângulo centralizado com âncora CENTER/MIDDLE."""
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        # Pico_Rect rct = { pt.x, pt.y, 4, 4 };
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        # no meio da janela
        self.utils.screenshot_and_compare("rect50x50y_center.png")

    def test_rect_centered_left_top_anchor(self):
        """Testa um retângulo centralizado com âncora LEFT/TOP."""
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_TOP))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        # Pico_Rect rct = { pt.x, pt.y, 4, 4 };
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        # Ancora no ponto superior esquerdo, então o quadrado fica à direita e para baixo
        self.utils.screenshot_and_compare("rect50x50y_lefttop.png")

    def test_rect_centered_right_bottom_anchor(self):
        """Testa um retângulo centralizado com âncora RIGHT/BOTTOM."""
        self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_BOTTOM))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        # Pico_Rect rct = { pt.x, pt.y, 4, 4 };
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        # Ancora no ponto inferior direito, então o quadrado fica à esquerda e para cima
        self.utils.screenshot_and_compare("rect50x50y_rightbottom.png")

    def test_rect_centered_right_middle_anchor(self):
        """Testa um retângulo centralizado com âncora RIGHT/MIDDLE."""
        self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_MIDDLE))
        pt = self.utils.pico.pico_pos((50, 50))
        self.utils.pico.pico_output_clear()
        # Pico_Rect rct = { pt.x, pt.y, 4, 4 };
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        # Ancora na direita no meio, então fica para a esquerda e centralizado verticalmente
        self.utils.screenshot_and_compare("rect50x50y_rightcenter.png")

    def test_rect_bottom_right_corner(self):
        """Testa um retângulo no canto inferior direito."""
        self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_BOTTOM))
        pt = self.utils.pico.pico_pos((100, 100)) # 100% da largura, 100% da altura
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("rect_bottom_right_corner.png")

    def test_rect_bottom_left_corner(self):
        """Testa um retângulo no canto inferior esquerdo."""
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_BOTTOM))
        pt = self.utils.pico.pico_pos((0, 100)) # 0% da largura, 100% da altura
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("rect_bottom_left_corner.png")

    def test_rect_top_right_corner(self):
        """Testa um retângulo no canto superior direito."""
        self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_TOP))
        pt = self.utils.pico.pico_pos((100, 0)) # 100% da largura, 0% da altura
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("rect_top_right_corner.png")

    def test_rect_top_left_corner(self):
        """Testa um retângulo no canto superior esquerdo."""
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_TOP))
        pt = self.utils.pico.pico_pos((0, 0)) # 0% da largura, 0% da altura
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_rect((pt[0], pt[1], 4, 4))
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("rect_top_left_corner.png")

    def test_nested_rectangles_bottom_left(self):
        """
        Testa o desenho de um retângulo maior no canto inferior esquerdo
        e dois retângulos menores dentro dele.
        """
        # Dimensões para o retângulo grande (ex: 20x20)
        large_rect_w, large_rect_h = 20, 20
        # Dimensões para o retângulo pequeno (ex: 4x4)
        small_rect_w, small_rect_h = 4, 4
        # Dimensões para o retângulo extra pequeno (ex: 2x2)
        extra_small_rect_w, extra_small_rect_h = 2, 2

        # Desenhar o retângulo grande no canto inferior esquerdo
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_BOTTOM))
        # pico_pos((0, 100)) dá as coordenadas do canto inferior esquerdo do mundo lógico
        pos_large_rect_corner = self.utils.pico.pico_pos((0, 100))
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 255, 255)) # Define a cor para branco
        self.utils.pico.pico_output_draw_rect(
            (pos_large_rect_corner[0], pos_large_rect_corner[1], large_rect_w, large_rect_h)
        )

        # Calcular o centro do retângulo grande
        # O 'y' de pos_large_rect_corner é a borda inferior.
        # Para encontrar o centro Y, subtraímos metade da altura do 'y' da borda inferior.
        # Para encontrar o centro X, adicionamos metade da largura ao 'x' da borda esquerda.
        center_x_large_rect = pos_large_rect_corner[0] + large_rect_w // 2
        center_y_large_rect = pos_large_rect_corner[1] - large_rect_h // 2
        
        # Desenhar o retângulo menor centralizado dentro do retângulo grande (VERMELHO)
        self.utils.pico.pico_set_color((255, 0, 0, 255)) # Define a cor para vermelho
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        self.utils.pico.pico_output_draw_rect(
            (center_x_large_rect, center_y_large_rect, small_rect_w, small_rect_h)
        )

        # Desenhar o retângulo extra pequeno centralizado dentro do retângulo menor (AZUL)
        # As coordenadas do centro do retângulo menor já são center_x_large_rect, center_y_large_rect
        self.utils.pico.pico_set_color((0, 0, 255, 255)) # Define a cor para azul
        self.utils.pico.pico_output_draw_rect(
            (center_x_large_rect, center_y_large_rect, extra_small_rect_w, extra_small_rect_h)
        )

        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("nested_rectangles_bottom_left.png")


    def test_combined_non_standard_anchors(self):
        """
        Testa múltiplos retângulos com âncoras de percentagens não padrão
        ao redor de um ponto central.
        """
        rect_w, rect_h = 4, 4
        # Ponto central de referência para todos os retângulos
        central_pt = self.utils.pico.pico_pos((50, 50))
        
        self.utils.pico.pico_output_clear()

        # Retângulo 1: Âncora central (referência) - será branco
        # Seu centro estará exatamente em central_pt
        self.utils.pico.pico_set_color((255, 255, 255, 255)) # Branco
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 2: Âncora (25, 25) - será vermelho
        # O ponto a 25% da largura e 25% da altura do retângulo se alinhará com central_pt.
        # Isso fará com que o retângulo se desloque ligeiramente para baixo e para a direita de central_pt.
        self.utils.pico.pico_set_color((255, 0, 0, 255)) # Vermelho
        self.utils.pico.pico_set_anchor_pos((25, 25))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 3: Âncora (75, 75) - será azul
        # O ponto a 75% da largura e 75% da altura do retângulo se alinhará com central_pt.
        # Isso fará com que o retângulo se desloque ligeiramente para cima e para a esquerda de central_pt.
        self.utils.pico.pico_set_color((0, 0, 255, 255)) # Azul
        self.utils.pico.pico_set_anchor_pos((75, 75))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("combined_non_standard_anchors.png")

    def test_combined_extreme_anchors(self):
        """
        Testa múltiplos retângulos com âncoras extremas (negativas e >100%)
        ao redor de um ponto central.
        """
        rect_w, rect_h = 4, 4
        # Ponto central de referência para todos os retângulos
        central_pt = self.utils.pico.pico_pos((50, 50))
        
        self.utils.pico.pico_output_clear()

        # Retângulo 1: Âncora central (referência) - será branco
        self.utils.pico.pico_set_color((255, 255, 255, 255)) # Branco
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 2: Âncora (-25, -25) - será vermelho
        # Deve aparecer deslocado para a direita e para baixo do central_pt
        self.utils.pico.pico_set_color((255, 0, 0, 255)) # Vermelho
        self.utils.pico.pico_set_anchor_pos((-25, -25))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 3: Âncora (125, 125) - será azul
        # Deve aparecer deslocado para a esquerda e para cima do central_pt
        self.utils.pico.pico_set_color((0, 0, 255, 255)) # Azul
        self.utils.pico.pico_set_anchor_pos((125, 125))
        self.utils.pico.pico_output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("combined_extreme_anchors.png")
