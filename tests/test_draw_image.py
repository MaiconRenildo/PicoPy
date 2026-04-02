import os
from tests.base_test import PicoTestBase

SKY_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "expected", "sky.png")


class TestDrawImage(PicoTestBase):
    """Classe de teste para operações de desenho de imagens."""
    
    def test_draw_simple_image_for_centralized_anchor(self):
        """Testa o desenho de uma imagem simples."""
        self.pico.set_grid(False)
        self.pico.set_dim_window((800, 600)) # Define um tamanho de janela maior para o teste
        self.pico.set_dim_world((800, 600))
        self.pico.set_zoom((100, 100))
        self.pico.output_clear()
        
        ####### Desenha a imagem com seu centro no canto superior esquerdo
        self.pico.output_draw_image((0, 0), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_top_left.png")
        self.pico.output_clear()

        ####### Desenha a imagem centralizada
        center_x, center_y = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        self.pico.output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center.png")
        self.pico.output_clear()

        ####### Desenha no canto esquerdo e centralizada na vertical
        # Parte da imagem fica a esquerda da janela
        self.pico.output_draw_image((0, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center_y.png")
        self.pico.output_clear()

        ####### Desenha no canto superior e centralizada na horizontal
        # Parte da imagem fica acima da janela
        self.pico.output_draw_image((center_x, 0), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center_x.png")
        # self.pico.set_dim_window(original_dim_window)
        # self.pico.set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_50_50(self):
        """Testa o desenho de uma imagem com zoom de 50.
        A imagem deve ficar menor que a imagem sem zoom.
        """
        # 740x493
        x_dim = 740*2
        y_dim = 493*2
        self.pico.set_dim_window((x_dim, y_dim))
        self.pico.set_dim_world((x_dim, y_dim))
        self.pico.set_grid(False)
        # self.pico.output_clear()
        
        center_x, center_y = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        # Desenho com zoom de 200%
        self.pico.set_zoom((50, 50))
        self.pico.output_clear() # limpa a nova textura com o preto
        self.pico.output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center_x_zoom_50.png")
        # self.pico.set_dim_window(original_dim_window)
        # self.pico.set_dim_world(original_dim_world)

    def test_draw_image_without_zoom(self):
        """Testa o desenho de uma imagem sem zoom aplicado."""
        # 740x493
        x_dim = 740*2
        y_dim = 493*2
        self.pico.set_dim_window((x_dim, y_dim))
        self.pico.set_dim_world((x_dim, y_dim))
        self.pico.set_grid(False)
        self.pico.output_clear() # limpa a textura original com o preto
        # pico_output_clear() # removido, pois ao limpar o fundo da textura original ficaria preto.
        # no entanto, ao chamar a pico_set_zoom, uma nova textura é criada sem o fundo preto da textura original.
        
        center_x, center_y = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        # Desenho com zoom de 100
        self.pico.output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()

        self.screenshot_and_compare("simple_image_center_x_zoom_100.png")
        # self.pico.set_dim_window(original_dim_window)
        # self.pico.set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_100_100(self):
        """
        Testa o desenho de uma imagem com zoom de (100,100), que representa o zoom padrão.
        Portanto, a imagem gerada deve ser a mesma da imagem sem zoom aplicado.
        """
        x_dim = 740*2
        y_dim = 493*2
        self.pico.set_dim_window((x_dim, y_dim))
        self.pico.set_dim_world((x_dim, y_dim))
        self.pico.set_grid(False)
        # pico_output_clear() # removido, pois ao limpar o fundo da textura original ficaria preto.
        # no entanto, ao chamar a pico_set_zoom, uma nova textura é criada sem o fundo preto da textura original.
        
        center_x, center_y = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        # Desenho com zoom de 100
        self.pico.set_zoom((100, 100))
        self.pico.output_clear() # limpa a nova textura com o preto
        # se essa linha for adicionada antes do pico_output_clear(),
        # a imagem gerada não terá o fundo preto.
        self.pico.output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center_x_zoom_100.png")
        # self.pico.set_dim_window(original_dim_window)
        # self.pico.set_dim_world(original_dim_world)

    def test_draw_image_with_zoom_160_160(self):
        """
        Testa o desenho de uma imagem com zoom de (160,160).
        A imagem deve ficar maior que a imagem sem zoom.
        """
        x_dim = 740*2
        y_dim = 493*2
        self.pico.set_dim_window((x_dim, y_dim))
        self.pico.set_dim_world((x_dim, y_dim))
        self.pico.set_grid(False)

        center_x, center_y = self.pico.pos((self.pico.POS_CENTER, self.pico.POS_MIDDLE))
        # Desenho com zoom de 60
        self.pico.set_zoom((167, 167))
        self.pico.output_clear()
        self.pico.output_draw_image((center_x, center_y), SKY_IMAGE_PATH)
        self.pico.output_present()
        self.screenshot_and_compare("simple_image_center_x_zoom_160.png")

    def test_image_cache(self):
        """Verifica se o cache de imagens está funcionando."""
        self.pico.output_clear()
        assert self.pico._hash is not None
        self.pico._hash.clear()
        # Carrega a imagem pela primeira vez
        self.pico.output_draw_image((0, 0), SKY_IMAGE_PATH)
        assert SKY_IMAGE_PATH in self.pico._hash
        first_texture_id = id(self.pico._hash[SKY_IMAGE_PATH])
        # Carrega a mesma imagem novamente
        self.pico.output_draw_image((10, 10), SKY_IMAGE_PATH)
        second_texture_id = id(self.pico._hash[SKY_IMAGE_PATH])
        assert first_texture_id == second_texture_id # mesma textura
        self.pico.output_present()
        self.screenshot_and_compare("image_cache_test.png")
