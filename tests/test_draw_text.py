import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path para importações relativas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import PICO_BOTTOM, PICO_CENTER, PICO_LEFT, PICO_MIDDLE, PICO_RIGHT, PICO_TOP
from tests.base_test import PicoTestBase

class TestDrawText(PicoTestBase):
    """Classe de teste para operações de desenho de texto."""

    def test_draw_text_basic(self):
        """Testa o desenho de texto básico com a fonte padrão."""
        self.utils.pico.pico_set_font(None, 10) # Define uma altura específica para a fonte
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_TOP))
        self.utils.pico.pico_set_color((255, 255, 255, 255)) # Branco
        self.utils.pico.pico_output_draw_text((0,0), "PicoPy!")
        self.utils.screenshot_and_compare("draw_text_basic.png")

    def test_draw_text_centered(self):
        """Testa o desenho de texto centralizado no meio da janela."""
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size) # Define uma altura específica para a fonte
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 255, 255)) # Branco
        world_w, world_h = self.utils.pico.pico_get_dim_world() # Calcula o centro do mundo (espaço de desenho)
        center_x = world_w // 2
        center_y = world_h // 2
        # Define a posição de ancoragem para o centro (já é o padrão, mas explicitamos para clareza)
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))
        # Desenha o texto, passando o centro da janela como a posição
        self.utils.pico.pico_output_draw_text((center_x, center_y), "Centralized!")
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("draw_text_centered.png")

    def test_draw_text_in_top_and_centered_with_custom_color(self):
        """Testa o desenho de texto com uma cor personalizada, centralizado horizontalmente."""
        font_size = 10 # Use um tamanho de fonte que seja visível para o teste
        self.utils.pico.pico_set_font(None, font_size) # Define uma altura específica para a fonte
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((0, 255, 0, 255)) # Verde
        # Obtém as dimensões da janela
        world_w, _ = self.utils.pico.pico_get_dim_world()
        # print(f"window_width: {window_width}, window_height: {window_height}") # Mantenha para depuração se quiser
        # Calcula a posição X para centralizar horizontalmente
        # A posição Y será o topo do texto, digamos 50 pixels abaixo do topo da tela
        center_x_pos = world_w // 2
        # Define a posição de ancoragem: CENTRO horizontalmente, TOPO verticalmente
        # PICO_CENTER deve ser 50 e PICO_TOP deve ser 0 (verifique em constants.py)
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_TOP))
        # Desenha o texto. O centro horizontal do texto ficará em center_x_pos,
        # e o topo do texto ficará em top_y_pos.
        self.utils.pico.pico_output_draw_text((center_x_pos, 0), "Green Text!")
        
        # self.utils.pico.pico_output_present() # Não necessário, já é chamado internamente
        self.utils.screenshot_and_compare("draw_text_green_in_top_and_centered.png")


    def test_draw_text_in_bottom_and_centered_with_custom_color(self):
        """Testa o desenho de texto com uma cor personalizada, centralizado horizontalmente."""
        font_size = 10 # Use um tamanho de fonte que seja visível para o teste
        self.utils.pico.pico_set_font(None, font_size) # Define uma altura específica para a fonte
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((0, 255, 0, 255)) # Verde
        # Obtém as dimensões da janela
        world_w, world_h = self.utils.pico.pico_get_dim_world()
        # print(f"window_width: {window_width}, window_height: {window_height}") # Mantenha para depuração se quiser
        # Calcula a posição X para centralizar horizontalmente
        # A posição Y será o topo do texto, digamos 50 pixels abaixo do topo da tela
        center_x_pos = world_w // 2
        # Define a posição de ancoragem: CENTRO horizontalmente, TOPO verticalmente
        # PICO_CENTER deve ser 50 e PICO_TOP deve ser 0 (verifique em constants.py)
        self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_BOTTOM))
        # Desenha o texto. O centro horizontal do texto ficará em center_x_pos,
        # e o topo do texto ficará em top_y_pos.
        self.utils.pico.pico_output_draw_text((center_x_pos, world_h), "Green Text!")
        
        # self.utils.pico.pico_output_present() # Não necessário, já é chamado internamente
        self.utils.screenshot_and_compare("draw_text_green_in_bottom_and_centered.png")


    def test_draw_text_rotated(self):
        """Testa o desenho de texto rotacionado."""
        font_size = 10 # Mantendo um tamanho de fonte consistente
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 0, 255, 255)) # Cor para o texto rotacionado (Magenta)    
        world_w, world_h = self.utils.pico.pico_get_dim_world()
        draw_x = world_w // 2
        draw_y = world_h // 2
        # Salva o ângulo e anchor_rotate atuais para restaurar depois
        original_angle = self.utils.pico.pico_get_angle()
        original_anchor_rotate = self.utils.pico.pico_get_anchor_rotate()
        original_anchor_pos = self.utils.pico.pico_get_anchor_pos()
        # original_angle = self.utils.pico.S.angle
        # original_anchor_rotate = self.utils.pico.S.anchor_rotate
        # original_anchor_pos = self.utils.pico.S.anchor_pos # Também importante para o posicionamento

        try:
            # Define o ponto de rotação para o centro do objeto
            self.utils.pico.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            
            # Define a ancoragem para o texto ser desenhado centralizado no ponto (draw_x, draw_y)
            self.utils.pico.pico_set_anchor_pos((PICO_CENTER, PICO_MIDDLE))

            # Define o ângulo de rotação (ex: 45 graus)
            # Como não há pico_set_angle pública, acessamos diretamente o estado.
            # Idealmente, uma função pico_set_angle(angle_in_degrees) seria usada.
            # self.utils.pico.S.angle = 45 # Rotação de 45 graus
            self.utils.pico.pico_set_angle(45)

            self.utils.pico.pico_output_draw_text((draw_x, draw_y), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_rotated_45.png")
            
            # Testar outra rotação, por exemplo, 90 graus
            self.utils.pico.pico_output_clear() # Limpa para o próximo desenho
            # self.utils.pico.S.angle = 90
            self.utils.pico.pico_set_angle(90)
            self.utils.pico.pico_output_draw_text((draw_x, draw_y), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_rotated_90.png")

        finally:
            # Restaura o estado original
            self.utils.pico.S.angle = original_angle
            self.utils.pico.pico_set_anchor_rotate(original_anchor_rotate)
            self.utils.pico.pico_set_anchor_pos(original_anchor_pos)


    def test_draw_text_aligned_right_with_90_angle(self):
        """Testa o desenho de texto alinhado à borda direita da janela com ângulo de 90 graus."""
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 0, 255))

        # Use as dimensões do MUNDO (espaço de desenho), não da janela.
        # O desenho é feito na textura TEX com tamanho zoom_dim = dim_world (zoom 100%).
        world_w, world_h = self.utils.pico.pico_get_dim_world()

        # original_anchor_pos = self.utils.pico.S.anchor_pos
        original_anchor_pos = self.utils.pico.pico_get_anchor_pos()

        try:
            self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_MIDDLE))
            self.utils.pico.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            self.utils.pico.S.angle = 90

            # Borda direita do mundo = world_w; centro vertical = world_h // 2
            self.utils.pico.pico_output_draw_text((world_w+font_size, world_h // 2), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_aligned_right_90.png")
        finally:
            self.utils.pico.pico_set_anchor_pos(original_anchor_pos)

    def test_draw_text_aligned_right_with_minus_90_angle(self):
        """Testa o desenho de texto alinhado à borda direita da janela com ângulo de -90 graus."""
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 0, 255))

        # Use as dimensões do MUNDO (espaço de desenho), não da janela.
        # O desenho é feito na textura TEX com tamanho zoom_dim = dim_world (zoom 100%).
        world_w, world_h = self.utils.pico.pico_get_dim_world()

        # original_anchor_pos = self.utils.pico.S.anchor_pos
        original_anchor_pos = self.utils.pico.pico_get_anchor_pos()

        try:
            self.utils.pico.pico_set_anchor_pos((PICO_RIGHT, PICO_MIDDLE))
            self.utils.pico.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            self.utils.pico.S.angle = -90

            # Borda direita do mundo = world_w; centro vertical = world_h // 2
            self.utils.pico.pico_output_draw_text((world_w+font_size, world_h // 2), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_aligned_right_minus_90.png")
        finally:
            self.utils.pico.pico_set_anchor_pos(original_anchor_pos)


    def test_draw_text_aligned_left_with_90_angle(self):
        """Testa o desenho de texto alinhado à borda esquerda da janela com ângulo de 90 graus."""
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 0, 255))

        _, world_h = self.utils.pico.pico_get_dim_world()
        original_anchor_pos = self.utils.pico.pico_get_anchor_pos()

        try:
            self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_MIDDLE))
            self.utils.pico.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            self.utils.pico.S.angle = 90

            # Borda esquerda: x negativo compensa o padding da fonte para colar o texto
            self.utils.pico.pico_output_draw_text((-font_size, world_h // 2), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_aligned_left_90.png")
        finally:
            self.utils.pico.pico_set_anchor_pos(original_anchor_pos)

    def test_draw_text_aligned_left_with_minus_90_angle(self):
        """Testa o desenho de texto alinhado à borda esquerda da janela com ângulo de -90 graus."""
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 0, 255))

        _, world_h = self.utils.pico.pico_get_dim_world()
        original_anchor_pos = self.utils.pico.pico_get_anchor_pos()

        try:
            self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_MIDDLE))
            self.utils.pico.pico_set_anchor_rotate((PICO_CENTER, PICO_MIDDLE))
            self.utils.pico.S.angle = -90

            self.utils.pico.pico_output_draw_text((-font_size, world_h // 2), "PicoPy")
            self.utils.screenshot_and_compare("draw_text_aligned_left_minus_90.png")
        finally:
            self.utils.pico.pico_set_anchor_pos(original_anchor_pos)

    def test_draw_text_multiple_lines(self):
        """Testa o desenho de múltiplas linhas de texto em posições diferentes."""
        self.utils.pico.pico_output_clear()
        font_size = 10
        self.utils.pico.pico_set_font(None, font_size)
        self.utils.pico.pico_set_color((255, 255, 0, 255)) # Amarelo
        self.utils.pico.pico_set_anchor_pos((PICO_LEFT, PICO_TOP))
        self.utils.pico.pico_output_draw_text((0, 0), "First Line")
        self.utils.pico.pico_output_draw_text((0, font_size), "Second Line") # Ajuste Y para a próxima linha
        self.utils.pico.pico_output_draw_text((0, font_size*2), "Third Line")
        self.utils.screenshot_and_compare("draw_text_multiline.png")

    def test_draw_text_empty_string(self):
        """Testa o desenho de uma string vazia (não deve renderizar nada)."""
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_set_color((255, 255, 255, 255))
        self.utils.pico.pico_output_draw_text((10, 10), "") # String vazia
        self.utils.screenshot_and_compare("draw_text_empty_string.png")
        # Este teste exigiria uma imagem de referência "vazia" (apenas fundo limpo)
        # para verificar que nada foi desenhado.



