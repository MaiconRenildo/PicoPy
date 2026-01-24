import pytest
from pico import PicoPy
from tests.utils import PicoTestUtils


@pytest.fixture
def utils():
    """
    Fixture que retorna os utilitários de teste, que já contêm acesso ao PicoPy.
    Garante que cada teste tenha um ambiente limpo e isolado.
    """
    pico = PicoPy()
    pico.pico_init(1)
    utils = PicoTestUtils(pico)
    yield utils
    pico.pico_init(0)
