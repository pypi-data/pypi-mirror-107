""" Модуль структур. Узлы Стандартных операторов: insert, if, else, for

Предупреждение:
    Все нижеописанные структуры работают с переменными Python.
    Если при обработки ваш код выдаст исключение, то rocshelf остановит компиляцию всего приложения (кроме default insert).
    Ошибки по типу SyntaxError будут обнаружены почти сразу же,
    а ошибки вида TypeError, могут обнаружиться в самой последней структуре самого последнего файла и сломать все...

"""

import re
import typing as _T
from copy import copy, deepcopy

import rlogging
from rcore.strpython import ReadValues, ReturnValue
from rocshelf import exception as ex
from rocshelf.template import areas
from rocshelf.template.basic import (FileSpan, Node, NodesList,
                                     ProcessingOutputNode, ProcessingParams,
                                     TextNode, registration)
from rocshelf.template.literals import (InLineOptionalStructureLiteral,
                                        InLineStructureLiteral,
                                        InTwoLineStructureLiteral, Literal,
                                        LiteralValue, StructureLiteral)

logger = rlogging.get_logger('mainLogger')

allowExceptions = (NameError, )


def check_python_string(string: str):
    """ Провкрка строки, которя в будущем будет передана компилятору python, на наличие явных проблем """

    logger.debug(f'Проверка строки: "{string}" на явные python ошибки')

    try:
        value = ReturnValue({}, string)

    # Разумеющиеся ошибки, такие как NameError, пропускаются
    except allowExceptions as exError:
        logger.warning(f'Выполнение строки: "{string}" выдало исключение: {exError}')
        return None

    # Если в передаваемой строке есть явные ошибки, выдавать исключение сразу
    except Exception as exError:
        logger.error(f'Выполнение строки: "{string}" выдало исключение: {exError}')
        raise exError

    else:
        logger.debug(f'Выполнение строки: "{string}" не выдало исключений')

    return value


class BaseOperatorNode(Node):
    """ Основа всех нод - опереторов """

    area = areas.CloseNodeArea

    @classmethod
    def create(cls, litValue: LiteralValue, literals: NodesList):
        return cls(litValue.content, litValue.fileSpan, literals)

    @staticmethod
    def read_python_string(contextVars: dict, string: str):

        callParameterValue = ReturnValue(contextVars, string)

        return callParameterValue

    def call_parameter_value(self, contextVars: dict) -> _T.Any:
        """ Получение пройденого обрабутку python значения.

        self.callParameterValue - значение, полученое пи инициализации

        """

        return self.read_python_string(contextVars, self.callParameter)


class InsertNode(BaseOperatorNode):
    """ Структура вставки переменной """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        for point in ['i', 'insert']:
            yield InLineOptionalStructureLiteral(
                'operators', cls,
                (point, None)
            )

    __slots__ = ('defaultValue', )
    defaultValue: str

    def deconstruct(self, defaultValue: _T.Optional[str] = None) -> None:
        self.defaultValue = defaultValue

    @classmethod
    def create(cls, literal: LiteralValue):

        try:
            option = literal.contentMath.group('option')

        except IndexError:
            option = None

        node = cls(literal.content, literal.fileSpan)
        node.deconstruct(option)

        return node

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        try:
            callParameterValue = self.call_parameter_value(
                proccParams.localVars
            )

        except Exception as exError:
            if self.defaultValue is None:
                raise exError

            callParameterValue = self.defaultValue

        textNode = TextNode(str(callParameterValue), self.fileSpan)
        textNode.deconstruct()

        self.subNodes = NodesList([textNode])

        return ProcessingOutputNode.from_node(self, proccParams)


class IfNode(BaseOperatorNode):
    """ Структура условия """

    @classmethod
    def literal_rule(cls):
        return InTwoLineStructureLiteral(
            'operators',
            cls,
            ('if', None),
            (None, 'if')
        )

    __slots__ = ('sections', )

    sections: dict[str, list]

    def deconstruct(self) -> None:
        self.sections = {
            'true': [],
            'else': []
        }

        for subNode in self.subNodes:
            if type(subNode) == ElseNode:
                self.sections['else'].append(subNode)

            else:
                self.sections['true'].append(subNode)

    @classmethod
    def create(cls, litValue: LiteralValue, litValues: NodesList):
        node = cls(litValue.content, litValue.fileSpan, litValues)
        node.deconstruct()
        return node

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        callParameterValue = self.call_parameter_value(
            proccParams.localVars
        )

        if callParameterValue:
            self.subNodes = NodesList(self.sections['true'])

        else:
            self.subNodes = NodesList(self.sections['else'])

        return ProcessingOutputNode.from_node(self, proccParams)


class ElseNode(IfNode):
    """ Структура условия else """

    @classmethod
    def literal_rule(cls):
        for point in ['else', 'elif']:
            yield InTwoLineStructureLiteral(
                'operators',
                cls,
                (point, None),
                (None, point)
            )

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        if self.callParameter is None:
            return ProcessingOutputNode.from_node(self, proccParams)

        return super()._processing(proccParams)


class ForNode(BaseOperatorNode):
    """ Структура цикла """

    __slots__ = ('iterableCondition', 'newVars')

    iterableCondition: str
    newVarsNames: tuple[str]

    @classmethod
    def literal_rule(cls):
        return InTwoLineStructureLiteral(
            'operators', cls,
            ('for', None),
            (None, 'for')
        )

    __slots__ = ('sections', )

    sections: dict[str, list]

    def deconstruct(self) -> None:
        self.parse_condition()

        self.sections = {
            'true': [],
            'else': []
        }

        for subNode in self.subNodes:
            if type(subNode) == ElseNode:
                self.sections['else'].append(subNode)

            else:
                self.sections['true'].append(subNode)

    @classmethod
    def create(cls, litValue: LiteralValue, litValues: NodesList):
        node = cls(litValue.content, litValue.fileSpan, litValues)
        node.deconstruct()
        return node

    def parse_condition(self):
        """ Разбивка условия цикла на подобный python синтаксис """

        logger.debug(f'Выборка переменных и итерируемого значения для ноды "{self.__class__.__name__}" из строки "{self.callParameter}"')

        try:
            (newVarsNames, self.iterableCondition) = [i.strip() for i in self.callParameter.split('in')]
            self.newVarsNames = re.split(r',\s*', newVarsNames)

            for i in self.newVarsNames:
                if i.find(' ') != -1:
                    raise ValueError

            logger.debug(f'Результат выборки. Новые переменные {self.newVarsNames} из итерируемой {self.iterableCondition}')

        except ValueError as exError:
            logger.warning(f'Заголовок структуры {self.__class__.__name__} при обработки выдал исключение: "{exError}"')
            raise SyntaxError('For structure must follow python syntax')

    @ProcessingParams.decorator
    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:

        iterVar = self.read_python_string(
            proccParams.localVars,
            self.iterableCondition
        )

        if len(iterVar) == 0:
            self.subNodes = NodesList(self.sections['else'])
            return ProcessingOutputNode.from_node(self, proccParams)

        newNodesList = []

        for anyItems in iterVar:

            localVars = {}

            if len(self.newVarsNames) == 1:
                localVars[self.newVarsNames[0]] = anyItems

            else:
                for (VarName, val) in zip(self.newVarsNames, anyItems):
                    localVars[VarName] = val

            localProccParams = deepcopy(proccParams)
            localProccParams.localVars.update(localVars)

            node = Node(fileSpan=self.fileSpan)
            node.subNodes = self.sections['true']
            node.proccParams = localProccParams
            newNodesList.append(node)

        self.subNodes = NodesList(newNodesList)

        return ProcessingOutputNode.from_node(self, proccParams)


# Регистрация узлов, которые могут быть вызваны в шаблонах
for node in [InsertNode, IfNode, ElseNode, ForNode]:
    registration(node)
