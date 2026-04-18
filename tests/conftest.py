import pytest
from picopy.pico import PicoPy

@pytest.fixture
def pico():
    """
    Fixture que retorna uma instância do PicoPy, garantindo um ambiente limpo.
    """
    pico = PicoPy()
    pico.init(True)
    pico.set_grid_world_unit(1)
    yield pico
    pico.init(False)
    PicoPy.reset_instance()