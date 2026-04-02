import pytest
from picopy.pico import PicoPy
import os
import tempfile

@pytest.mark.usefixtures("pico")
class PicoTestBase:
    pico: PicoPy

    @pytest.fixture(autouse=True)
    def _inject_pico(self, pico):
        self.pico = pico
        yield

    def get_expected_image_path(self, image_filename: str) -> str:
        """Retorna o caminho completo da imagem de referência baseado no diretório tests/"""
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(tests_dir, "expected", image_filename)

    def ensure_reference_image(self, expected_image_path: str) -> bool:
        """Cria a imagem de referência se ela não existir"""
        if not os.path.exists(expected_image_path):
            print(f"Imagem de referência não encontrada: {expected_image_path}")
            print("Criando imagem de referência...")
            os.makedirs(os.path.dirname(expected_image_path), exist_ok=True)
            self.pico.output_screenshot(expected_image_path)
            print(f"Imagem de referência criada. Execute o teste novamente.")
            return False
        return True

    def capture_screenshot_for_comparison(self, expected_image_path: str) -> str | None:
        """Verifica/cria imagem de referência, captura screenshot e retorna o caminho do arquivo temporário"""
        if not self.ensure_reference_image(expected_image_path):
            return None
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        screenshot_path = self.pico.output_screenshot(tmp_path)
        assert screenshot_path is not None, "Falha ao salvar screenshot"
        return tmp_path

    def compare_images(self, actual_image_path: str, expected_image_path: str, error_message: str | None = None) -> None:
        """Compara duas imagens e lança AssertionError se forem diferentes"""
        with open(actual_image_path, 'rb') as f1, open(expected_image_path, 'rb') as f2:
            actual_data = f1.read()
            expected_data = f2.read()
            if error_message is None:
                error_message = f"A imagem gerada não corresponde à imagem de referência"
            assert actual_data == expected_data, error_message

    def screenshot_and_compare(self, image_filename: str, error_message: str | None = None) -> bool:
        """
        Função auxiliar que captura screenshot, compara com imagem de referência e limpa arquivo temporário.
        """
        expected_image_path = self.get_expected_image_path(image_filename)
        tmp_path = self.capture_screenshot_for_comparison(expected_image_path)
        if tmp_path is None:
            return False
        try:
            self.compare_images(tmp_path, expected_image_path, error_message)
            return True
        finally:
            os.unlink(tmp_path)