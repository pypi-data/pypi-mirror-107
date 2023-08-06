""" Модуль с основными структурами

"""

from __future__ import annotations

import functools
import os
import typing as _T
from copy import deepcopy

import rlogging
from rcore import utils
from rcore.rpath import rPath
from rcore.utils import keyByValue, rDict, short_text
from rocshelf import components
from rocshelf import exception as ex
from rocshelf.template import areas, deconstruct, literals

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

    # html file
    if filePath.extension == '.html':
        contextList.append('file-html')
        contextList.append('operators')

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


class ProcessingParams(object):
    """ Параметры компиляции """

    localVars: dict[_T.Any, _T.Any]

    def __init__(self, localVars: _T.Optional[dict] = None) -> None:

        if localVars is None:
            localVars = {}

        self.localVars = localVars

    def add(self, proccParams: ProcessingParams):
        """ Слияние двух объектов параметризации компиляции """

        logger.debug(f'Слияние двух объектов {self.__class__.__name__}: {id(self)} & {id(proccParams)}')

        self.localVars.update(
            proccParams.localVars
        )

    @staticmethod
    def decorator(func):
        """ Декоратор для функций _processing и _compile """

        @functools.wraps(func)
        def wrapper(self: Node, proccParams: ProcessingParams, *args, **kwargs):

            if self.proccParams is not None:
                proccParams.add(
                    self.proccParams
                )

            return func(self, proccParams, *args, **kwargs)

        return wrapper


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
            from rocshelf.template.file import deconstructedFilesId

            return '<{0} {1}:{2} [{3}]>'.format(
                self.__class__.__name__,
                self.fileId,
                self.span,
                utils.file_span_separate(deconstructedFilesId[self.fileId].pathFile, [self.span])[0]
            )

        return '<{0} {1}:{2}>'.format(
            self.__class__.__name__,
            self.fileId,
            self.span,
        )

    def __init__(self, fileId: _T.Union[int, None], span: tuple[int, int]):
        self.fileId = fileId
        self.span = span


class NodesList(object):
    """ Класс для обработки списка литералов/узлов """

    __slots__ = ('nodes', )

    nodes: list[Node, literals.LiteralValue]

    def __init__(self, nodes: _T.Union[list[Node], None] = None):
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

    def compile(self):
        """ Вызов метода компиляции и элементов спика """

    def tree2d(self) -> list[str]:
        """ Формирует 2d представление """

        brickNames = []

        for item in self.nodes:
            if isinstance(item, Node):
                brickNames.append(str(item))

                if item.subNodes is not None:
                    if not isinstance(item.subNodes, NodesList):
                        raise ex.ex.DeveloperIsShitError(f'У ноды {item.__class__.__name__} subNodes не NodesList, а {type(item.subNodes)}')

                    brickNames += item.subNodes.tree2d()

            else:
                brickNames.append(str(item))

        return brickNames


class Node(object):
    """ Основа """

    __slots__ = ('callParameter', 'fileSpan', 'subNodes', 'proccParams')

    area = areas.NodeArea

    callParameter: _T.Optional[str]
    fileSpan: _T.Optional[FileSpan]
    subNodes: _T.Optional[NodesList]
    proccParams: ProcessingParams

    def __str__(self):
        return '<Node:{0} ({1})>'.format(
            self.__class__.__name__,
            self.callParameter
        )

    def __repr__(self) -> str:
        return '<Node:{0} ({1}) with [{2}]>'.format(
            self.__class__.__name__,
            self.callParameter,
            repr(self.subNodes),
        )

    def __init__(self, callParameter: _T.Optional[str] = None, fileSpan: _T.Optional[FileSpan] = None, subNodes: _T.Optional[_T.Union[NodesList, list]] = None) -> None:
        super().__init__()

        if callParameter is not None and callParameter.strip() == '':
            callParameter = None

        if isinstance(subNodes, list):
            subNodes = NodesList(subNodes)

        self.callParameter = callParameter
        self.fileSpan = fileSpan
        self.subNodes = subNodes
        self.proccParams = None

        logger.debug('Инициализация ноды: "{0}"'.format(
            repr(self)
        ))

    @classmethod
    def literal_rule(cls) -> _T.Union[literals.Literal, _T.Generator[literals.Literal]]:
        """ Формирование правила для разбиения строки """

        raise TypeError(f'Нода {cls.__name__} не поддерживает создание через использование литерала')

    @classmethod
    def create(cls, literal: literals.Literal):
        """ Инициализация объекта через литерал """

        raise TypeError(f'Нода {cls.__name__} не поддерживает создание через использование литерала')

    @classmethod
    def template(cls, *args, **kwargs):
        """ Инициализация объекта напрямую """

        raise TypeError(f'Нода {cls.__name__} не поддерживает создание напрямую')

    def deconstruct(self) -> None:
        """ Первостепенная обработка ноды происходящая в момент обработки файлов """
        ...

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        """ Обработка ноды """

        return ProcessingOutputNode.from_node(self, proccParams)

    @ProcessingParams.decorator
    def _compile(self, proccParams: ProcessingParams) -> str:
        """ Перевод ноды в текст """

        raise TypeError('Нода {0} не поддерживает компиляцию'.format(
            self.__class__.__name__
        ))

    def processing(self, proccParams: _T.Optional[ProcessingParams] = None) -> ProcessingOutputNode:
        """ Первая стадия компиляции нод - предварительная обработка нод:

        Удаление ненужных нод, преобразование статичных нод и т.д.

        Args:
            proccParams (_T.Optional[ProcessingParams], optional): Параметры компиляции. Defaults to None.
                Переменные, используемые при компиляции.

        Returns:
            ProcessingOutputNode: Нода предварительной стадии компиляции.
            Для завершения компиляции нужно вызвать метод compile()

        """

        logger.debug('Запуск обработки ноды "{0}"'.format(
            repr(self)
        ))

        if not isinstance(proccParams, ProcessingParams):
            proccParams = ProcessingParams(proccParams)

        return self._processing(proccParams)

    def compile(self, proccParams: _T.Union[ProcessingParams, dict, None] = None) -> str:
        """ Вторая стадия компиляции нод - перевод нод в текст.

        Args:
            proccParams (_T.Optional[ProcessingParams], optional): Параметры компиляции. Defaults to None.
                Переменные, используемые при компиляции.

        Returns:
            str: Итоговая строка

        """

        logger.debug('Запуск компиляции ноды "{0}"'.format(
            repr(self)
        ))

        if not isinstance(proccParams, ProcessingParams):
            proccParams = ProcessingParams(proccParams)

        return self._compile(proccParams)


class TextNode(Node):
    """ Нода текста """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        return literals.TextLiteral(
            'text',
            cls
        )

    def deconstruct(self) -> None:
        if self.callParameter is None:
            self.callParameter = ''

    @classmethod
    def create(cls, literal: literals.LiteralValue):
        node = cls(literal.content, literal.fileSpan)
        node.deconstruct()
        return node

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        return ProcessingOutputNode.node(self, proccParams)

    def _compile(self, proccParams: ProcessingParams):
        logger.debug('Применение ноды: "{0}"'.format(
            repr(self)
        ))

        return self.callParameter


class ProcessingOutputNode(Node):
    """ Нода, которая будет использоваться при обработки других нод.

    Состоит только из нод текста. Все структуры должны выполнить свою обработку до вызова этой ноды.

    -!! Params:
    -!!    statistics: dict - некая статистика, собирающаяся при компиляции
    -!!    params: dict - некая параметры, собирающаяся при компиляции

    """

    __slots__ = ('collectedData', )

    collectedData: dict

    def __init__(self):
        super().__init__()

        self.collectedData = {}
        self.subNodes = NodesList()

    @classmethod
    def from_node(cls, node: Node, proccParams: ProcessingParams, collectedData: _T.Optional[dict] = None):
        """ Формирование ноды обработки из под нод обрабатываемой ноды.

        Подразумевается, что эта нода завешила свою работу.

        """

        logger.debug('Формирование ноды: "{0}" из subNodes у ноды "{1}"'.format(
            cls.__name__,
            repr(node)
        ))

        outputNode = cls()

        if collectedData is not None:
            outputNode.collectedData = collectedData

        if node.subNodes is not None:
            for subNode in node.subNodes:
                outputNode.add(
                    subNode.processing(proccParams)
                )

        logger.debug('Результат состоит из {0} нод'.format(
            len(outputNode.subNodes)
        ))

        return outputNode

    @classmethod
    def node(cls, node: Node, proccParams: ProcessingParams, collectedData: _T.Optional[dict] = None) -> ProcessingOutputNode:
        """ Формирование ноды обработки из обрабатываемой ноды.

        Подразумевается, что эта нода обработается до конца на этапе компиляции

        """

        logger.debug('Формирование ноды: "{0}" из ноды "{1}"'.format(
            cls.__name__,
            repr(node)
        ))

        outputNode = cls()

        if node.subNodes is not None:
            for subNode in node.subNodes:
                outputNode.add(
                    subNode.processing(proccParams)
                )

            node.subNodes = outputNode.subNodes

        outputNode.subNodes = NodesList([
            node
        ])
        return outputNode

    def add(self, outputNode: ProcessingOutputNode, mergeNodes: bool = True):
        """ Добавление к трейсеру новых значений """

        logger.debug('Слияние нод: "{0}" $ "{1}"'.format(
            repr(self),
            repr(outputNode)
        ))

        if mergeNodes:
            self.subNodes += outputNode.subNodes

        self.collectedData = rDict(self.collectedData).merge(outputNode.collectedData, True).attend

    def _compile(self, proccParams: ProcessingParams) -> str:
        """ Сборка ноды в текст """

        logger.debug('Сборка ноды: "{0}"'.format(
            repr(self)
        ))

        resultString = ''
        for subItem in self.subNodes:
            resultString += subItem.compile(proccParams)

        logger.debug('Результат сборки: "{0}"'.format(
            short_text(resultString)
        ))

        return resultString


class StringNode(Node):
    """ Нода текста для инициализации напрямую """

    def __init__(self, string: str):
        super().__init__(None, None, None)
        self.deconstruct(string)

    def deconstruct(self, string: rPath) -> None:
        context = context_generator()
        self.subNodes = deconstruct.analyze(
            string, None, context
        )


class DevNode(Node):
    """ Нода для реализации костылей """

    def __init__(self, string: str, context: list[str]):
        super().__init__(None, None, None)
        self.deconstruct(string, context)

    def deconstruct(self, string: rPath, context: list[str]) -> None:
        self.subNodes = deconstruct.analyze(
            string, None, context
        )


class CommentNode(Node):
    """ Нода закоментированного кода """

    area = areas.ThisNodeArea

    def deconstruct(self, litValue: literals.LiteralValue):
        # Добавить проверку необходимость компилировать комментарии
        if False:
            self.subNodes = NodesList([
                TextNode(litValue.content, litValue.fileSpan)
            ])

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        node = cls(litValue.content, litValue.fileSpan)
        node.deconstruct(litValue)
        return node


def registration_literal(literal: literals.Literal):
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

    if literal.contextType not in literals.CONTEXT_TYPES:
        raise ValueError('Неизвестный тип контекста: "{}"'.format(
            literal.contextType
        ))

    literals.LITERALS[literal.contextType].append(literal)


def registration(node: Node):
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
