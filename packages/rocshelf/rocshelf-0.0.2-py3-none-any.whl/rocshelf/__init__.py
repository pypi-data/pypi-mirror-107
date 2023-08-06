""" rocshelf - препроцессор для компиляции веб-страниц из составляющих частей с параллельной модернизацией.

За основу взята идея максимального разделение кода на независимые части, которые сливаются в единое целое при компиляции.

"""

from rcore.utils import gen_user_workspace

from .main import set_config, set_path, start_cli
from .middleware import UICompile, UIRoute, UIShelves, path, view, views

__version__ = (0, 0, 2, 'alpha', 0)