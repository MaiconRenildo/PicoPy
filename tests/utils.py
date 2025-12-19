import os
import tempfile
from pico import pico_output_screenshot


def ensure_reference_image(expected_image_path):
    """Cria a imagem de referência se ela não existir"""
    if not os.path.exists(expected_image_path):
        print(f"Imagem de referência não encontrada: {expected_image_path}")
        print("Criando imagem de referência...")
        os.makedirs(os.path.dirname(expected_image_path), exist_ok=True)
        pico_output_screenshot(expected_image_path)
        print(f"Imagem de referência criada. Execute o teste novamente.")
        return False
    return True


def get_expected_image_path(image_filename):
    """Retorna o caminho completo da imagem de referência baseado no diretório tests/"""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(tests_dir, "expected", image_filename)


def capture_screenshot_for_comparison(expected_image_path):
    """Verifica/cria imagem de referência, captura screenshot e retorna o caminho do arquivo temporário"""
    # Verifica se a imagem de referência existe (cria se não existir)
    if not ensure_reference_image(expected_image_path):
        return None
    # Cria arquivo temporário para salvar o screenshot
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_path = tmp_file.name
    # Tira screenshot e salva no arquivo temporário
    screenshot_path = pico_output_screenshot(tmp_path)
    assert screenshot_path is not None, "Falha ao salvar screenshot"
    return tmp_path


def compare_images(actual_image_path, expected_image_path, error_message=None):
    """Compara duas imagens e lança AssertionError se forem diferentes"""
    with open(actual_image_path, 'rb') as f1, open(expected_image_path, 'rb') as f2:
        actual_data = f1.read()
        expected_data = f2.read()
        if error_message is None:
            error_message = f"A imagem gerada não corresponde à imagem de referência"
        assert actual_data == expected_data, error_message