
import functools
import typing as _T

import rlogging
from rocshelf.components import localization, routes, shelves
from rocshelf.components.relations import relation
from rocshelf.components.routes import GetRoute
from rocshelf.frontend.chunks import Chunk
from rocshelf.template.basic import ProcessingParams

logger = rlogging.get_logger('mainLogger')


class SharedCompilationMetaData(object):
    """ Общая информация обо всей компиляции.

    Парметры:
      frameworks (list[str]):
        Список фреймворков для которых будет происходить компиляция

      locals (list[str]):
        Список локализаций компиляции

      locals (list[str]):
        Список компилируемых маршрутов

    Использование:
      В шаблон компиляции передается словарь данных, один из которых __meta__, у которого атрибут __shared__, в виде объекта данного класса

    """

    __slots__ = (
        'localizations', 'shelves', 'routes',
    )

    localizations: str
    shelves: str
    routes: str

    def __init__(self):
        self.localizations = tuple(localization.localsData.keys())
        self.routes = tuple(routes.routes.keys())

        self.shelves = {}
        for shelfType in shelves.SHELFTYPES:
            self.shelves[shelfType] = tuple(shelves.shelves[shelfType].keys())

    @classmethod
    @functools.cache
    def cached(cls):
        """ Кеширование создания класса

        Returns:
            [type]: Экземпляр класса SharedCompilationMetaData

        """

        return cls()


class TemplateCompilationMetaData(object):
    """ Информация о процессе компиляции.

    Использование:
      В шаблон компиляции передается словарь данных, один из которых __meta__ в виде объекта данного класса

    """

    __slots__ = (
        '__shared__', 'framework', 'localization', 'route', 'page', 'shelf', 'chunks'
    )

    __shared__: SharedCompilationMetaData

    framework: str
    localization: _T.Union[str, None]
    route: str
    page: str
    shelf: str

    chunks: _T.Optional[list[Chunk]]

    def __init__(self, localizationName: _T.Union[str, None], route: str, page: str, shelf: str):
        self.__shared__ = SharedCompilationMetaData.cached()

        self.framework = relation.framework
        self.localization = localizationName
        self.route = route
        self.page = page
        self.shelf = shelf

        self.chunks = None

    def add_chucks(self, chunks: list[Chunk]):
        """ Добавление в метаданные компиляции атрибута с чанками статики

        Args:
            chunks (list[Chunk]): Чанки статики

        """

        self.chunks = chunks

    @classmethod
    def processing_params(cls, routeKey: str, localizationName: _T.Union[str, None]) -> ProcessingParams:
        """ Создание объекта параметров компиляции

        Args:
            routeKey (str): Идентификатор маршрута
            localizationName (_T.Union[str, None]): Компилируемая локализация

        Returns:
            ProcessingParams: Параметры компиляции

        """

        route = GetRoute.route(routeKey)

        page = route.page
        localVars = route.localVars

        shelf = shelves.GetShelf.name('page', page)

        localVars['__meta__'] = cls(localizationName, routeKey, page, str(shelf))

        return ProcessingParams(localVars)


class StaticCompilationMetaData(object):
    """ Информация о процессе компиляции.

    Использование:
      В шаблон компиляции передается словарь данных, один из которых __meta__ в виде объекта данного класса

    """

    __slots__ = (
        '__shared__', 'framework', 'localizationName', 'staticType', 'loadTime', 'routeKeys', 'shelfSlugs', 'staticFileName'
    )

    __shared__: SharedCompilationMetaData

    framework: str

    localizationName: _T.Optional[str]
    staticType: str
    loadTime: str
    routeKeys: set[str]
    shelfSlugs: set[str]
    staticFileName: str

    def __init__(self,
                 localizationName: _T.Optional[str],
                 staticType: str,
                 loadTime: str,
                 routeKeys: set[str],
                 shelfSlugs: set[str],
                 staticFileName: str
                 ):

        self.__shared__ = SharedCompilationMetaData.cached()

        self.framework = relation.framework

        self.localizationName = localizationName
        self.staticType = staticType
        self.loadTime = loadTime
        self.routeKeys = routeKeys
        self.shelfSlugs = shelfSlugs
        self.staticFileName = staticFileName

    @classmethod
    def processing_params(cls,
                          localizationName: _T.Optional[str],
                          staticType: str,
                          loadTime: str,
                          chunk: Chunk,
                          staticFileName: str) -> ProcessingParams:
        """ Создание объекта параметров компиляции

        Args:
            localizationName (_T.Optional[str]): [description]
            staticType (str): [description]
            loadTime (str): [description]
            Chunk (Chunk): [description]
            staticFileName (str): [description]

        Returns:
            ProcessingParams: Параметры компиляции

        """

        localVars = {}

        localVars['__meta__'] = cls(
            localizationName,
            staticType,
            loadTime,
            chunk.routeKeys,
            chunk.shelfSlugs,
            staticFileName
        )

        return ProcessingParams(localVars)
