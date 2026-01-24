import os
from tests.base_test import PicoTestBase

SKY_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "expected", "sky.png")


class TestDrawImage(PicoTestBase):
    """Classe de teste para operações de desenho de imagens."""
    
    def test_draw_simple_image_for_centralized_anchor(self):
        """Testa o desenho de uma imagem simples."""
        original_dim_window = self.utils.pico.pico_get_dim_window()
        original_dim_world = self.utils.pico.pico_get_dim_world()
        self.utils.pico.pico_set_dim_window((800, 600)) # Define um tamanho de janela maior para o teste
        self.utils.pico.pico_set_dim_world((800, 600))
        self.utils.pico.pico_set_zoom((100, 100))
        self.utils.pico.pico_output_clear()
        
        ####### Desenha a imagem com seu centrono canto superior esquerdo
        self.utils.pico.pico_output_draw_image((0, 0), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_top_left.png")
        self.utils.pico.pico_output_clear()

        ####### Desenha a imagem centralizada
        window_width, window_height = self.utils.pico.pico_get_dim_window()
        # Calcular a posição para centralizar a imagem
        center_x = window_width / 2
        center_y = window_height/ 2
        self.utils.pico.pico_output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center.png")
        self.utils.pico.pico_output_clear()

        ####### Desenha no canto esquerdo e centralizada na vertical
        # Parte da imagem fica a esquerda da janela
        self.utils.pico.pico_output_draw_image((0, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center_y.png")
        self.utils.pico.pico_output_clear()

        ####### Desenha no canto superior e centralizada na horizontal
        # Parte da imagem fica acima da janela
        self.utils.pico.pico_output_draw_image((center_x, 0), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center_x.png")
        # Restaura dimensões originais (a fixture fará o cleanup do pico_init)
        self.utils.pico.pico_set_dim_window(original_dim_window)
        self.utils.pico.pico_set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_200_200(self):
        """Testa o desenho de uma imagem com zoom de 200.
        A imagem deve ficar menor que a imagem sem zoom.
        """
        original_dim_window = self.utils.pico.pico_get_dim_window()
        original_dim_world = self.utils.pico.pico_get_dim_world()
        # 740x493
        x_dim = 740*2
        y_dim = 493*2
        self.utils.pico.pico_set_dim_window((x_dim, y_dim))
        self.utils.pico.pico_set_dim_world((x_dim, y_dim))
        # self.utils.pico.pico_output_clear()
        
        window_width, window_height = self.utils.pico.pico_get_dim_window()
        center_x = window_width / 2
        center_y = window_height/ 2
        # Desenho com zoom de 200%
        self.utils.pico.pico_set_zoom((200, 200))
        self.utils.pico.pico_output_clear() # limpa a nova textura com o preto
        self.utils.pico.pico_output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center_x_zoom_200.png")
        # Restaura dimensões originais
        self.utils.pico.pico_set_dim_window(original_dim_window)
        self.utils.pico.pico_set_dim_world(original_dim_world)

    def test_draw_image_without_zoom(self):
        """Testa o desenho de uma imagem sem zoom aplicado."""
        original_dim_window = self.utils.pico.pico_get_dim_window()
        original_dim_world = self.utils.pico.pico_get_dim_world()
        # 740x493
        x_dim = 740*2
        y_dim = 493*2
        self.utils.pico.pico_set_dim_window((x_dim, y_dim))
        self.utils.pico.pico_set_dim_world((x_dim, y_dim))
        self.utils.pico.pico_output_clear() # limpa a textura original com o preto
        # pico_output_clear() # removido, pois ao limpar o fundo da textura original ficaria preto.
        # no entanto, ao chamar a pico_set_zoom, uma nova textura é criada sem o fundo preto da textura original.
        
        window_width, window_height = self.utils.pico.pico_get_dim_window()
        center_x = window_width / 2
        center_y = window_height/ 2
        # Desenho com zoom de 100
        # pico_set_zoom((100, 100))
        self.utils.pico.pico_output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()

        self.utils.screenshot_and_compare("simple_image_center_x_zoom_100.png")
        # Restaura dimensões originais
        self.utils.pico.pico_set_dim_window(original_dim_window)
        self.utils.pico.pico_set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_100_100(self):
        """
        Testa o desenho de uma imagem com zoom de (100,100), que representa o zoom padrão.
        Portanto, a imagem gerada deve ser a mesma da imagem sem zoom aplicado.
        """
        original_dim_window = self.utils.pico.pico_get_dim_window()
        original_dim_world = self.utils.pico.pico_get_dim_world()
        x_dim = 740*2
        y_dim = 493*2
        self.utils.pico.pico_set_dim_window((x_dim, y_dim))
        self.utils.pico.pico_set_dim_world((x_dim, y_dim))
        # pico_output_clear() # removido, pois ao limpar o fundo da textura original ficaria preto.
        # no entanto, ao chamar a pico_set_zoom, uma nova textura é criada sem o fundo preto da textura original.
        
        window_width, window_height = self.utils.pico.pico_get_dim_window()
        center_x = window_width / 2
        center_y = window_height/ 2
        # Desenho com zoom de 100
        self.utils.pico.pico_set_zoom((100, 100))
        self.utils.pico.pico_output_clear() # limpa a nova textura com o preto
        # se essa linha for adicionada antes do pico_output_clear(),
        # a imagem gerada não terá o fundo preto.
        self.utils.pico.pico_output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center_x_zoom_100.png")
        # Restaura dimensões originais
        self.utils.pico.pico_set_dim_window(original_dim_window)
        self.utils.pico.pico_set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_60_60(self):
        """
        Testa o desenho de uma imagem com zoom de (60,60).
        A imagem deve ficar maior que a imagem sem zoom.
        """
        original_dim_window = self.utils.pico.pico_get_dim_window()
        original_dim_world = self.utils.pico.pico_get_dim_world()
        x_dim = 740*2
        y_dim = 493*2
        self.utils.pico.pico_set_dim_window((x_dim, y_dim))
        self.utils.pico.pico_set_dim_world((x_dim, y_dim))

        window_width, window_height = self.utils.pico.pico_get_dim_window()
        center_x = window_width / 2
        center_y = window_height/ 2
        # Desenho com zoom de 60
        self.utils.pico.pico_set_zoom((60, 60))
        self.utils.pico.pico_output_clear()
        self.utils.pico.pico_output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("simple_image_center_x_zoom_60.png")
        # Restaura dimensões originais
        self.utils.pico.pico_set_dim_window(original_dim_window)
        self.utils.pico.pico_set_dim_world(original_dim_world)

    def test_image_cache(self):
        """Verifica se o cache de imagens está funcionando."""
        self.utils.pico.pico_output_clear()
        assert self.utils.pico._pico_hash is not None
        self.utils.pico._pico_hash.clear()
        # Carrega a imagem pela primeira vez
        self.utils.pico.pico_output_draw_image((0, 0), SKY_IMAGE_PATH)
        assert SKY_IMAGE_PATH in self.utils.pico._pico_hash
        first_texture_id = id(self.utils.pico._pico_hash[SKY_IMAGE_PATH])
        # Carrega a mesma imagem novamente
        self.utils.pico.pico_output_draw_image((10, 10), SKY_IMAGE_PATH)
        second_texture_id = id(self.utils.pico._pico_hash[SKY_IMAGE_PATH])
        assert first_texture_id == second_texture_id # mesma textura
        self.utils.pico.pico_output_present()
        self.utils.screenshot_and_compare("image_cache_test.png")
