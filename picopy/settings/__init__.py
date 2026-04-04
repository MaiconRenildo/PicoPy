import sdl2
from .anchor_positions import AnchorPositions
from .graphics_settings import GraphicsSettings

from .mouse_buttons import MouseButtons
from .event_types import EventTypes
from .key_codes import KeyCodes
from .scan_codes import ScanCodes
from .colors import Colors

class Settings(GraphicsSettings, ScanCodes, AnchorPositions, MouseButtons, EventTypes, KeyCodes, Colors):
    pass