""" Модуль для предварительной обработки текста

"""

from __future__ import annotations

import re
import typing as _T
from pprint import pprint

import rlogging
from rcore.utils import short_text, split_list_by_indexes
from rocshelf import exception as ex
from rocshelf.template import basic, literals

logger = rlogging.get_logger('mainLogger')

textNodeLiteral: _T.Optional[literals.TextLiteral] = None


class LiteralMask(object):
    """ Маска некого совпадения с литералами """

    isEmpty: bool

    literal: literals.Literal
    patternIndex: int
    position: tuple[int, int]

    def __init__(self):
        self.isEmpty = True

    def check(self, literal: literals.Literal, patternIndex: int, math: re.Match):
        """ Сравнение совпадения сохраненного в маске с новым

        Args:
            literal (literals.Literal): Литерал, по которому нашлось совпадение
            patternIndex (int): Индекс паттерна из литреала
            math (re.Match): Результат совпадения

        Raises:
            ex.ex.DeveloperIsShitError: Я где то накосячил

        """

        position = math.span()

        def update():
            self.literal = literal
            self.patternIndex = patternIndex
            self.position = position
            self.math = math

        if self.isEmpty:
            self.isEmpty = False
            update()
            return

        if self.position[0] > position[0]:
            update()

        elif self.position[0] == position[0] and self.position[1] > position[1]:
            update()

        elif self.position[0] == position[0] and self.position[1] == position[1] and self.literal.weight < literal.weight:
            update()

        elif self.position[0] == position[0] and self.position[1] == position[1] and self.literal.weight == literal.weight:
            pprint([
                (self.literal, self.math),
                (literal, math)
            ])
            raise ex.ex.DeveloperIsShitError('print')

    def literal_value(self, onFileId: _T.Union[int, None]) -> literals.LiteralValue:
        """ Формированеи Значения литерала сохраненного в маске

        Args:
            onFileId (_T.Union[int, None]): Идентификатор файла в котором найдено совпадение

        Returns:
            literals.LiteralValue: Объект значения литерала

        """

        return literals.LiteralValue(
            self.literal,
            self.patternIndex,
            basic.FileSpan(onFileId, self.position),
            self.math
        )

    @staticmethod
    def text_literal(string: str, onFileId: _T.Union[int, None], position: tuple[int, int]):
        """ Формирование литерала """

        global textNodeLiteral
        if textNodeLiteral is None:
            textNodeLiteral = basic.TextNode.literal_rule()

        # 50/50
        string = re.sub(r'^\s+|\s+$', ' ', string)
        if string == ' ':
            string = ''

        return literals.LiteralValue(
            textNodeLiteral,
            0,
            basic.FileSpan(onFileId, position),
            re.search(r'(?P<content>[\s\S]*)', string)
        )


def explore(string: str, onFileId: _T.Union[int, None] = None, contextsList: list[str] = []) -> basic.NodesList:
    """ Разбор строки на составляющие литералы """

    logger.debug(f'Разбиение строки "{short_text(string)}"')

    literalsList = []

    textPointer = 0
    textLength = len(string)

    while string:

        match = LiteralMask()

        for contextType in contextsList:
            for literal in literals.LITERALS[contextType]:

                # Вставить разделение на файлы
                for patternIndex in range(len(literal.patterns)):
                    pattern = literal.patterns[patternIndex]

                    newMatch = pattern.search(string)

                    if newMatch:
                        match.check(literal, patternIndex, newMatch)

        if match.isEmpty:
            literalsList.append(
                LiteralMask.text_literal(
                    string, onFileId, (textPointer, textLength)
                )
            )
            string = None

        else:
            if match.position[0] != 0:
                preString = string[:match.position[0]]
                literalsList.append(
                    LiteralMask.text_literal(
                        preString, onFileId, (textPointer, match.position[0])
                    )
                )

            literalsList.append(
                match.literal_value(onFileId)
            )
            string = string[(match.position[1]):]

    # В конец всех обработаных сток/файлов добавляется нода текста,
    # Чтобы адаптироваться случайные обработки (исключить возможность появления других нод в конце списка)
    literalsList.append(
        LiteralMask.text_literal('', None, (-1, -1))
    )

    literalsList = basic.NodesList(literalsList)

    logger.debug(f'Результат состоит из {len(literalsList)} литералов: {literalsList}')

    return literalsList


def juxtaposition_core(litValues: list[_T.Union[literals.LiteralValue, basic.Node]]):

    newLiterals = []

    literalsLength = len(litValues)

    for litValueIndex in range(literalsLength):
        litValue = litValues[litValueIndex]

        logger.debug(f'Сопоставление литерала {litValue}')

        if isinstance(litValue, basic.Node):
            newLiterals.append(litValue)
            continue

        node = litValue.literal.node

        arealizeResult = node.area.arealize(litValues, litValueIndex)

        if arealizeResult is None:
            continue

        elif isinstance(arealizeResult, tuple):
            if isinstance(arealizeResult[0], range) and isinstance(arealizeResult[1], basic.Node):
                _, _, postLitValue = split_list_by_indexes(litValues, [arealizeResult[0].start, arealizeResult[0].stop])

                newLiterals.append(arealizeResult[1])
                newLiterals += postLitValue

                return juxtaposition_core(newLiterals)

            else:
                print(arealizeResult, type(arealizeResult))
                raise ex.ex.DeveloperIsShitError()

        elif isinstance(arealizeResult, basic.Node):
            newLiterals.append(arealizeResult)

        elif isinstance(arealizeResult, int) and litValueIndex == arealizeResult:
            newLiterals.append(
                node.create(litValue)
            )

        elif isinstance(arealizeResult, int) and arealizeResult == -1:
            return [
                node.create(litValue, newLiterals + litValues[litValueIndex + 1:])
            ]

        elif isinstance(arealizeResult, range):

            _, nowLitValue, postLitValue = split_list_by_indexes(litValues, [arealizeResult.start, arealizeResult.stop])

            nowLitValue = juxtaposition_core(nowLitValue)

            newLiterals.append(
                node.create(
                    litValue,
                    nowLitValue
                )
            )
            newLiterals += postLitValue

            return juxtaposition_core(newLiterals)

        elif isinstance(arealizeResult, basic.NodesList):
            return juxtaposition_core(arealizeResult.nodes)

        else:
            print(arealizeResult, type(arealizeResult))
            raise ex.ex.DeveloperIsShitError('qwerty')

    return newLiterals


def juxtaposition(litValues: basic.NodesList) -> basic.NodesList:
    """ Сопоставление литералов NodesList с зарегистрированными нодами """

    logger.debug(f'Сопоставление литералов "{litValues}"')

    newLiterals = juxtaposition_core(
        litValues.nodes
    )

    return basic.NodesList(newLiterals)


def analyze(string: str, onFileId: _T.Union[int, None] = None, contextsList: _T.Optional[list[str]] = None):
    """ Разбиение строки на """

    if contextsList is None:
        raise ValueError('analyze need contexts list')

    litValues = explore(string, onFileId, contextsList)
    bricks = juxtaposition(litValues)

    return bricks
