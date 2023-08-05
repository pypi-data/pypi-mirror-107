from nonebot import get_driver

from .config import Config

try:
    global_config = get_driver().config
    config = Config(**global_config.dict())
    from .plugins import *
except ValueError:
    pass

from .version import __version__, VERSION
