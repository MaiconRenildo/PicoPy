import pytest
from tests.utils import PicoTestUtils


@pytest.mark.usefixtures("utils")
class PicoTestBase:
    """
    Classe base para todos os testes do PicoPy.
    Fornece acesso automático ao utils através de self.utils.
    Todas as classes de teste devem herdar desta classe.
    """
    utils: PicoTestUtils  # Type hint para o atributo
    
    @pytest.fixture(autouse=True)
    def _inject_utils(self, utils):
        """
        Fixture automática que injeta utils na instância da classe.
        O parâmetro utils recebe o valor da fixture utils do conftest.py.
        """
        self.utils = utils
        yield
