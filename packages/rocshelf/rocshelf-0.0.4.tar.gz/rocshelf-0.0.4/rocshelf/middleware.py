""" Прослойка между интерфейсом взаимодействия и основным функционалом.

Объекты этого модуля могут использоваться другими python приложениями.

"""

import os
import typing as _T
from asyncio.log import logger
from copy import copy

from rcore.config import CfEditNamedFile
from rcore.rpath import rPath, rPathCopy
from rcore.utils import input_yes_no

from rocshelf import exception as ex
from rocshelf.compile import compile_routes
from rocshelf.components import localization, media, routes, shelves
from rocshelf.components.relations import relation
from rocshelf.components.routes import GetRoute
from rocshelf.config import cf


def path(name: str) -> str:
    """ Возвращает абсолютный путь до корневых директорий: template, static и media файлов

    Args:
        name (str): Запрашиваемая директория: template, static или media

    Returns:
        [str]: Путь до директории

    """

    try:
        return cf.get(['export', name])

    except ex.ex.ItemNotFound:
        raise KeyError


def view(name: str) -> str:
    """ Возвращает путь от корневой папки template к запрашиваемому шаблону

    Args:
        name (str): Идентификатор шаблона, из словаря route в файле конфигурации

    Returns:
        [str]: Путь до нужного шаблона

    """

    try:
        return cf.get(['template', name])

    except ex.ex.ItemNotFound:
        raise KeyError


def views() -> dict:
    """ Возвращает словарь всех доступных шаблонов.

    Returns:
        dict: Словарь маршрутов и соответствующих шаблонов

    """

    try:
        return cf.get(['template'])

    except ex.ex.ItemNotFound:
        raise KeyError


class rUI(object):
    """ Базовый класс для создания интерфейсов взаимодействия с компонентами приложения """

    output: str = "dict"
    counter: dict[str, int] = {}
    permission: dict[str, _T.Union[None, bool, int]] = {}

    def __init__(self):
        self.counter = {
            "edited": 0, "created": 0, "existing": 0, "missed": 0, "deleted": 0
        }
        self.permission = {
            'shelf': None, 'route': None
        }

    def get_permission(self, to: str, message: str) -> bool:
        """ Получение разрешения на замену файлов некого Объекта.

        Args:
            to (str): Объект: shelf, route
            message (str): Сообщение для запроса. Defaults to False.

        Returns:
            bool: Полученый ответ

        """

        if self.permission[to] is None:
            self.permission[to] = input_yes_no(message, False)

        return self.permission[to]

    def merge_counts(self, counter: dict[str, int]):
        """ Обновление значений счетчика.

        Args:
            counter (dict[str, int]): Счетчик, из которого берутся значения.

        """

        for i in counter:
            self.counter[i] += counter[i]


class UICompile(rUI):
    """ Интерфейс для работы с компиляцией """

    forFramework: str

    def __init__(self, forFramework: str = 'server'):
        """ Инициализация объекта

        Args:
            forFramework (str): Фреймвор, под который будет адаптированна компиляция.

        """

        self.forFramework = forFramework
        super().__init__()

    def init(self):
        """ Инициализация системы для компиляции """

        shelves.InitComponent.all_stages()
        routes.InitComponent.all_stages()
        localization.InitComponent.all_stages()

        media.init()
        relation.init(self.forFramework)

    def compile(self):
        """ Запуск компиляции всех страниц """
        
        self.init()
        compile_routes.start_compile()


class UIShelves(rUI):
    """ Интерфейс для работы с шелфами.

    Для редактирования файла конфигурации нужно указать его с ключом "shelf" при использовании функции set_config.

    """

    initComponent: shelves.InitComponent

    shelf: shelves.ShelfItem

    restpath: str
    dictpath: list[str]

    def __init__(self, shelfType: str, shelfName: str):
        """ Инициализация Объекта

        Args:
            shelfType (str): Тип шелфа
            shelfName (str): Имя/путь директори шелфа.

        """

        super().__init__()

        self.initComponent = shelves.InitComponent()
        self.initComponent.all_stages()

        (self.shelfPath, shelfName) = os.path.split(shelfName)

        self.shelf = shelves.GetShelf.create(shelfType, shelfName)
        self.dictpath = ['path', 'import', shelfType] + shelfName.split('.')

        self.shelfPath = '/'.join([i for i in [self.shelfPath, shelfName.split('.')[-1]] if i])

    def __create_shelf(self, layout: bool):
        logger.info('Создание шелфа "{0}" по пути "{1}" {2}используя шаблон'.format(
            self.shelf,
            self.shelf.path,
            '' if layout else 'не '
        ))

        if layout:
            targetFolder = self.shelf.path
            layoutFolder = cf.path('layout', self.shelf)
            rPathCopy.mergedir(
                str(targetFolder),
                [str(layoutFolder)]
            )

        else:
            self.shelf.get_path('html').create()

    def __create(self, layout: bool):
        """ Создание директори шелфа

        Args:
            layout (bool): Использовать шаблон

        """

        needCreate = True
        shelfFound = self.shelf.check()

        if shelfFound:
            needCreate = self.get_permission('shelf', 'По адресу "{0}" есть файлы шелфа. Пересоздать их?'.format(
                self.shelf.path
            ))

        if needCreate:
            self.__create_shelf(layout)

        if needCreate and shelfFound:
            self.counter['edited'] += 1

        elif needCreate:
            self.counter['created'] += 1

        elif shelfFound:
            self.counter['existing'] += 1

        else:
            self.counter['missed'] += 1

    def create(self, layout: bool = False):
        """ Создание шелфа

        Args:
            layout (bool): Использовать шаблон

        """

        try:
            shelves.GetShelf.name(self.shelf.type, self.shelf.name)

        except ex.ShelfNotFoundError:
            with CfEditNamedFile(cf, 'shelf') as config:
                config.set(self.shelfPath, self.dictpath)
            self.initComponent.parse()
            self.initComponent.construct()

        self.shelf = shelves.GetShelf.name(
            self.shelf.type,
            self.shelf.name,
        )
        self.__create(layout)
        self.initComponent.all_stages()

    def __delete(self):
        paths = self.shelf.get_paths()
        self.counter['deleted'] += 1

        # Удаление основных файлов шелфа
        for shelfFile in paths.values():
            shelfFile.delete(True)

    def delete(self):
        """ Удаление шелфа """

        try:
            shelves.GetShelf.name(self.shelf.type, self.shelf.name)

        except ex.ShelfNotFoundError:
            self.counter['missed'] += 1
            return

        self.__delete()

        with CfEditNamedFile(cf, 'shelf') as config:
            config.delete(self.dictpath)

        self.initComponent.all_stages()

    def get(self):
        """ Получение информацию о шелфе """

    def sync(self, layout: bool = False):
        """ Создание недостающих шелфов из файла конфигурации

        Args:
            layout (bool): Использовать шаблон

        """

        for shelfType, shelfName, _ in shelves.GetShelf.walk():
            ui = UIShelves(shelfType, shelfName)
            ui.permission['shelf'] = 0
            ui.create(layout)
            self.merge_counts(ui.counter)


class UIRoute(rUI):
    """ Интерфейс для работы с маршрутами.

    Для редактирования файла конфигурации нужно указать его с ключом "route" при использовании функции set_config.

    """

    def __init__(self, route: str):
        """ Инициализация Объекта.

        Args:
            route (str): Идентификатор маршрута

        """

        super().__init__()
        self.route = route

        routes.check_name_route(route)

    def init(self):
        """ Инициализация компонента """

        logger.debug('Инициализация компонента "routes" через "UIRoute" интерфейс')
        routes.InitComponent.all_stages()

    def create(self, page: str, layout: bool = False):
        """ Создание маршрута

        Args:
            page (str): Путь до директории шелфа-page
            layout (bool, optional): Использовать шаблон

        """

        with CfEditNamedFile(cf, 'route') as config:
            config.set(
                {'page': page, 'data': {}},
                ['route'] + self.route.replace('/', '.').split('.')
            )

        ui = UIShelves('page', page)
        ui.permission['shelf'] = 0
        ui.create(layout)
        self.merge_counts(ui.counter)

    def delete(self):
        """ Удаление маршрута """

        with CfEditNamedFile(cf, 'route') as config:
            config.delete(
                ['route'] + self.route.replace('/', '.').split('.') + ['page']
            )
            config.delete(
                ['route'] + self.route.replace('/', '.').split('.') + ['data']
            )

    def get(self):
        """ Получение информации о маршруте """

    def sync(self, layout: bool = False):
        """ Создание недостающих шелфов-page из файла конфигурации

        Args:
            layout (bool): Использовать шаблон

        """

        for _, route in GetRoute.walk():
            ui = UIShelves('page', route.page)
            ui.permission['shelf'] = 0
            ui.create(layout)
            self.merge_counts(ui.counter)
