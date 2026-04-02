import pytest
from pico import PicoPy

@pytest.fixture
def pico():
    """
    Fixture que retorna uma instância do PicoPy, garantindo um ambiente limpo.
    """
    pico = PicoPy()
    pico.init(1)
    pico.set_grid_world_unit(1)
    yield pico
    pico.init(0)