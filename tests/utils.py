import os
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

