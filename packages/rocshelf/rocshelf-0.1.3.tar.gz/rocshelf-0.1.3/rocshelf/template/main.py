
from __future__ import annotations

import functools
import typing as _T

import rlogging
from rcore import utils
from rcore.rpath import rPath
from rocshelf import components
from rocshelf import exception as ex
from rocshelf import template

logger = rlogging.get_logger('mainLogger')


def context_generator(filePath: _T.Optional[rPath] = None) -> list[str]:
    """ Формирование контекста для обработки

    Returns:
        list[str]: context list

    """

    # Разделение входного текста на 'из файла' или нет
    if filePath is None:
        return [
            'operators'
        ]

    # Обрабатывается файл
    contextList = [
        'file'
    ]

    contextList.append('operators')

    # html file
    if filePath.extension == '.html':
        contextList.append('file-html')

        # Проверка инициализации шелфов
        if components.shelves.shelves:
            contextList.append('shelves')

        # Проверка инициализации маршутов
        if components.routes.routes:
            contextList.append('page-route')

        # !!!!!!!!!!!!!! Проверка инициализации медиа файлов !!!!!!!!!!!!!!
        # if components.media.saveMediaFiles:
        #     contextList.append('media')

        # Проверка инициализации локализации
        # if components.localization.localsData:
            # contextList.append('localization')

    # static file
    elif filePath.extension in ('.css', '.scss', '.sass', '.js'):

        # style file
        if filePath.extension in ('.css', '.scss', '.sass'):
            contextList.append('file-style')
            contextList.append('file-style-sass')

        # script file
        elif filePath.extension == '.js':
            contextList.append('file-script')

    logger.debug('Для файла "{0}" составлен список контекстов: {1}'.format(
        filePath, contextList
    ))

    return contextList


def registration_literal(literal: template.literals.Literal):
    """ Регистрация литерала

    Args:
        literal (literals.Literal): Литерал

    Raises:
        ValueError: Контекст, описанный в литерале, не прописан в списке CONTEXT_TYPES

    """

    logger.debug('Регистрация литерала "{0}" от узла "{1}" в контекст "{2}"'.format(
        literal.__class__.__name__,
        literal.node.__name__,
        literal.contextType
    ))

    if literal.contextType not in template.literals.CONTEXT_TYPES:
        raise ValueError('Неизвестный тип контекста: "{0}"'.format(
            literal.contextType
        ))

    template.literals.LITERALS[literal.contextType].append(literal)


def registration(node: template.nodes.Node):
    """ Регистрация узла

    Args:
        node (Node): Узел

    """

    logger.debug('Регистрация узла "{0}"'.format(
        node.__name__,
    ))

    literalRule = node.literal_rule()

    if isinstance(literalRule, _T.Iterable):
        for literal in literalRule:
            registration_literal(literal)

    else:
        registration_literal(literalRule)


class BaseNodesList(object):
    """ Класс для обработки списка литералов/узлов """

    __slots__ = ('nodes', )

    nodes: list[_T.Union[template.nodes.Node, template.literals.LiteralValue]]

    def __init__(self, nodes: _T.Union[list[template.nodes.Node], None] = None):
        self.nodes = []
        if nodes is not None:
            self.nodes = nodes

    def __str__(self):
        return '<Bricks: {0}>'.format(
            [str(i) for i in self.nodes]
        )

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, key):
        return self.nodes[key]

    def __iadd__(self, other):
        self.nodes += other
        return self


class NodesList(BaseNodesList):
    """ Класс для обработки списка литералов/узлов """

    def compile(self):
        """ Вызов метода компиляции и элементов спика """

    def tree2d(self) -> list[str]:
        """ Формирует 2d представление """

        brickNames = []

        for item in self.nodes:
            if isinstance(item, template.nodes.Node):
                brickNames.append(str(item))

                if item.subNodes is not None:
                    if not isinstance(item.subNodes, NodesList):
                        raise ex.ex.DeveloperIsShitError('У ноды {0} subNodes не NodesList, а {1}'.format(
                            item.__class__.__name__,
                            type(item.subNodes)
                        ))

                    brickNames += item.subNodes.tree2d()

            else:
                brickNames.append(str(item))

        return brickNames


class ProcessingParams(object):
    """ Параметры компиляции """

    localVars: dict[_T.Any, _T.Any]

    def __init__(self, localVars: _T.Optional[dict] = None) -> None:

        if localVars is None:
            localVars = {}

        self.localVars = localVars

    def add(self, proccParams: ProcessingParams):
        """ Слияние двух объектов параметризации компиляции """

        logger.debug('Слияние двух объектов {0}: {1} & {2}'.format(
            self.__class__.__name__,
            id(self),
            id(proccParams)
        ))

        self.localVars.update(
            proccParams.localVars
        )


class FileSpan(object):
    """ Класс для идентификации частей кода """

    __slots__ = ('fileId', 'span')

    fileId: _T.Union[int, None]
    span: tuple[int, int]

    def __str__(self):
        return '<{0} {1}:({2})>'.format(
            self.__class__.__name__,
            self.fileId,
            self.span
        )

    def __repr__(self) -> str:
        if self.fileId:
            return '<{0} {1}:{2} [{3}]>'.format(
                self.__class__.__name__,
                self.fileId,
                self.span,
                utils.file_span_separate(template.file.get_file(self.fileId), [self.span])[0]
            )

        return '<{0} {1}:{2}>'.format(
            self.__class__.__name__,
            self.fileId,
            self.span,
        )

    def __init__(self, fileId: _T.Union[int, None], span: tuple[int, int]):
        self.fileId = fileId
        self.span = span

    def generate_traceback(self) -> ex.ex.rTrFile:
        """ Создание трейсбека по файлу и span.

        Returns:
            ex.ex.rTrFile: [description]

        """

        return ex.ex.rTrFile(
            str(template.file.get_file(self.fileId)),
            self.span
        )
