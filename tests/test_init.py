"""
Testes: inicialização do pico-sdl
"""

import sys
import os

# Adiciona o diretório raiz ao path para importar pico
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pico import pico_init, pico_output_clear, pico_output_present, pico_output_screenshot
from .utils import ensure_reference_image
import sdl2  # type: ignore


def test_init():
    """Testa a inicialização do pico-sdl"""
    # Inicializa o pico-sdl
    print("Inicializando pico-sdl...")
    pico_init(1)
    
    # Limpa a tela (já deve estar limpa, mas garantimos)
    pico_output_clear()
    
    # Apresenta a tela
    pico_output_present()
    print("Tela preta exibida. Aguardando 2 segundos...")
    
    # Aguarda 2 segundos
    sdl2.SDL_Delay(2000)
    
    # Termina o pico-sdl
    print("Finalizando pico-sdl...")
    pico_init(0)
    print("Teste concluído!")


def test_init_black_screen():
    """Testa a inicialização do pico-sdl e verifica se a tela está preta comparando com imagem de referência"""
    import tempfile
    
    # Caminho para a imagem de referência
    test_dir = os.path.dirname(os.path.abspath(__file__))
    expected_image = os.path.join(test_dir, "expected", "black_screen.png")
    
    # Inicializa o pico-sdl
    print("Inicializando pico-sdl...")
    pico_init(1)
    
    try:
        # Limpa a tela
        pico_output_clear()
        
        # Verifica se a imagem de referência existe (cria se não existir)
        if not ensure_reference_image(expected_image):
            return
        
        # Tira screenshot em arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        screenshot_path = pico_output_screenshot(tmp_path)
        assert screenshot_path is not None, "Falha ao salvar screenshot"
        
        # Compara as imagens diretamente
        with open(tmp_path, 'rb') as f1, open(expected_image, 'rb') as f2:
            output_data = f1.read()
            expected_data = f2.read()
            
            assert output_data == expected_data, "A imagem gerada não corresponde à imagem de referência preta"
        
        # Remove arquivo temporário
        os.unlink(tmp_path)
        
        print("✓ Verificação: Tela está preta (imagem corresponde à referência)")
        
        # Apresenta a tela
        pico_output_present()
        print("Tela preta exibida. Aguardando 1 segundo...")
        
        # Aguarda 1 segundo
        sdl2.SDL_Delay(1000)
        
    finally:
        # Termina o pico-sdl
        print("Finalizando pico-sdl...")
        pico_init(0)
        print("Teste concluído!")
