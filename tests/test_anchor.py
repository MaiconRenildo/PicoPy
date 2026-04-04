from tests.base_test import PicoTestBase

class TestAnchor(PicoTestBase):
    """Classe de teste para operações de ancoramento (anchor_pos)."""

    # PIXELS
    def test_pixel_centered_50x50_center_middle_anchor(self):
        """Testa um pixel centralizado com âncora CENTER/MIDDLE."""
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_pixel(pt)
        self.pico.output_present()
        # igual ao "/pixel50x50y_lefttop.png"
        self.screenshot_and_compare("pixel50x50y_center.png")

    def test_pixel_centered_50x50_left_top_anchor(self):
        """Testa um pixel centralizado com âncora LEFT/TOP."""
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_pixel(pt)
        self.pico.output_present()
        # igual ao "/pixel50x50y_center.png"
        self.screenshot_and_compare("pixel50x50y_lefttop.png")

    def test_pixel_centered_50x50_right_bottom_anchor(self):
        """Testa um pixel centralizado com âncora RIGHT/BOTTOM."""
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_BOTTOM))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_pixel(pt)
        self.pico.output_present()
        # 1 pixel para a esquerda e 1 para cima
        self.screenshot_and_compare("pixel50x50y_rightbottom.png")

    # RECTS
    def test_rect_centered_exact_center_middle_anchor(self):
        """Testa um retângulo centralizado com âncora CENTER/MIDDLE."""
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        # no meio da janela
        self.screenshot_and_compare("rect50x50y_center.png")

    def test_rect_centered_left_top_anchor(self):
        """Testa um retângulo centralizado com âncora LEFT/TOP."""
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        # Ancora no ponto superior esquerdo, então o quadrado fica à direita e para baixo
        self.screenshot_and_compare("rect50x50y_lefttop.png")

    def test_rect_centered_right_bottom_anchor(self):
        """Testa um retângulo centralizado com âncora RIGHT/BOTTOM."""
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_BOTTOM))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        # Ancora no ponto inferior direito, então o quadrado fica à esquerda e para cima
        self.screenshot_and_compare("rect50x50y_rightbottom.png")

    def test_rect_centered_right_middle_anchor(self):
        """Testa um retângulo centralizado com âncora RIGHT/MIDDLE."""
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_MIDDLE))
        pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        # Ancora na direita no meio, então fica para a esquerda e centralizado verticalmente
        self.screenshot_and_compare("rect50x50y_rightcenter.png")

    def test_rect_bottom_right_corner(self):
        """Testa um retângulo no canto inferior direito."""
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_BOTTOM))
        pt = self.pico.pos((self.pico.POS_RIGHT, self.pico.POS_BOTTOM)) # 100% da largura, 100% da altura
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        self.screenshot_and_compare("rect_bottom_right_corner.png")

    def test_rect_bottom_left_corner(self):
        """Testa um retângulo no canto inferior esquerdo."""
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_BOTTOM))
        pt = self.pico.pos((self.pico.POS_LEFT, self.pico.POS_BOTTOM)) # 0% da largura, 100% da altura
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        self.screenshot_and_compare("rect_bottom_left_corner.png")

    def test_rect_top_right_corner(self):
        """Testa um retângulo no canto superior direito."""
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_TOP))
        pt = self.pico.pos((self.pico.POS_RIGHT, self.pico.POS_TOP)) # 100% da largura, 0% da altura
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        self.screenshot_and_compare("rect_top_right_corner.png")

    def test_rect_top_left_corner(self):
        """Testa um retângulo no canto superior esquerdo."""
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        pt = self.pico.pos((self.pico.POS_LEFT, self.pico.POS_TOP)) # 0% da largura, 0% da altura
        self.pico.output_clear()
        self.pico.output_draw_rect((pt[0], pt[1], 4, 4))
        self.pico.output_present()
        self.screenshot_and_compare("rect_top_left_corner.png")

    def test_nested_rectangles_bottom_left(self):
        """
        Testa o desenho de um retângulo maior no canto inferior esquerdo
        e dois retângulos menores dentro dele.
        """
        # Dimensões para o retângulo grande (ex: 20x20)
        large_rect_w, large_rect_h = 20, 20
        # Dimensões para o retângulo pequeno (ex: 4x4)
        small_rect_w, small_rect_h = 4, 4
        extra_small_rect_w, extra_small_rect_h = 2, 2

        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_BOTTOM))
        pos_large_rect_corner = self.pico.pos((self.pico.POS_LEFT, self.pico.POS_BOTTOM))
        self.pico.output_clear()
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.output_draw_rect(
            (pos_large_rect_corner[0], pos_large_rect_corner[1], large_rect_w, large_rect_h)
        )

        self.pico.set_color(self.pico.COLOR_RED)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        center_x_target = pos_large_rect_corner[0] + large_rect_w / 2
        center_y_target = pos_large_rect_corner[1] - large_rect_h / 2
        self.pico.output_draw_rect(
            (center_x_target, center_y_target, small_rect_w, small_rect_h)
        )

        self.pico.set_color(self.pico.COLOR_BLUE)
        self.pico.output_draw_rect(
            (center_x_target, center_y_target, extra_small_rect_w, extra_small_rect_h)
        )

        self.pico.output_present()
        self.screenshot_and_compare("nested_rectangles_bottom_left.png")


    def test_combined_non_standard_anchors(self):
        """
        Testa múltiplos retângulos com âncoras de percentagens não padrão
        ao redor de um ponto central.
        """
        rect_w, rect_h = 4, 4
        # Ponto central de referência para todos os retângulos
        central_pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        
        self.pico.output_clear()

        # Retângulo 1: Âncora central (referência) - será branco
        # Seu centro estará exatamente em central_pt
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 2: Âncora (25, 25) - será vermelho
        # O ponto a 25% da largura e 25% da altura do retângulo se alinhará com central_pt.
        # Isso fará com que o retângulo se desloque ligeiramente para baixo e para a direita de central_pt.
        self.pico.set_color(self.pico.COLOR_RED)
        self.pico.set_anchor_pos((25, 25))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 3: Âncora (75, 75) - será azul
        # O ponto a 75% da largura e 75% da altura do retângulo se alinhará com central_pt.
        # Isso fará com que o retângulo se desloque ligeiramente para cima e para a esquerda de central_pt.
        self.pico.set_color(self.pico.COLOR_BLUE)
        self.pico.set_anchor_pos((75, 75))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        self.pico.output_present()
        self.screenshot_and_compare("combined_non_standard_anchors.png")

    def test_combined_extreme_anchors(self):
        """
        Testa múltiplos retângulos com âncoras extremas (negativas e >100%)
        ao redor de um ponto central.
        """
        rect_w, rect_h = 4, 4
        # Ponto central de referência para todos os retângulos
        central_pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        
        self.pico.output_clear()

        # Retângulo 1: Âncora central (referência) - será branco
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 2: Âncora (-25, -25) - será vermelho
        # Deve aparecer deslocado para a direita e para baixo do central_pt
        self.pico.set_color(self.pico.COLOR_RED)
        self.pico.set_anchor_pos((-25, -25))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 3: Âncora (125, 125) - será azul
        # Deve aparecer deslocado para a esquerda e para cima do central_pt
        self.pico.set_color(self.pico.COLOR_BLUE)
        self.pico.set_anchor_pos((125, 125))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        self.pico.output_present()
        self.screenshot_and_compare("combined_extreme_anchors.png")
   
    def test_anchor_with_different_object_sizes(self):
        """
        Testa a ancoragem com um pixel, um retângulo pequeno e um retângulo maior
        na mesma posição e com a mesma âncora (CENTER, MIDDLE).
        Todos os centros devem se alinhar no ponto central.
        """
        central_pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        
        self.pico.output_clear()
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))

        # Desenha um retângulo maior (20x20) - será azul
        self.pico.set_color(self.pico.COLOR_BLUE)
        self.pico.output_draw_rect((central_pt[0], central_pt[1], 20, 20))

        # Desenha um retângulo pequeno (4x4) - será vermelho
        self.pico.set_color(self.pico.COLOR_RED)
        self.pico.output_draw_rect((central_pt[0], central_pt[1], 4, 4))

        # Desenha um pixel (1x1) - será branco
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.output_draw_pixel(central_pt)

        self.pico.output_present()
        self.screenshot_and_compare("anchor_different_object_sizes.png")




    def test_anchor_with_camera_scroll(self):
        """
        Testa a ancoragem com um deslocamento da câmera (scroll).
        Desenha múltiplos retângulos com âncoras diferentes ao redor
        de um ponto central, com um scroll aplicado.
        """
        rect_w, rect_h = 10, 10
        central_pt = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE)) # Ponto de referência no mundo (400, 300)
        # Novo scroll_offset para mostrar apenas o quadrado azul em diante
        # (32 - 10, 18 - 10) = (22, 8) no mundo lógico.
        # O ponto (22, 8) aparece na tela em (0, 0).
        scroll_offset = (22, 8) # Deslocamento da câmera

        self.pico.output_clear()
        self.pico.set_scroll(scroll_offset) # Aplica o scroll

        # Retângulo 1: Âncora central (referência) - será branco
        # Seu centro lógico estará em central_pt, mas visualmente deslocado pelo scroll.
        self.pico.set_color(self.pico.COLOR_WHITE)
        self.pico.set_anchor_pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))

        # Retângulo 2: Âncora superior esquerda - será vermelho
        # Seu canto superior esquerdo lógico estará em central_pt, deslocado pelo scroll.
        self.pico.set_color(self.pico.COLOR_RED)
        self.pico.set_anchor_pos((self.pico.POS_LEFT, self.pico.POS_TOP))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))
        # Retângulo 3: Âncora inferior direita - será azul
        # Seu canto inferior direito lógico estará em central_pt, deslocado pelo scroll.
        self.pico.set_color(self.pico.COLOR_BLUE)
        self.pico.set_anchor_pos((self.pico.POS_RIGHT, self.pico.POS_BOTTOM))
        self.pico.output_draw_rect((central_pt[0], central_pt[1], rect_w, rect_h))
        
        # Retorna o scroll para (0,0) para não afetar outros testes
        self.pico.set_scroll((0, 0))

        self.pico.output_present()
        self.screenshot_and_compare("anchor_with_camera_scroll.png")