""" Описание всех уровней tracebacks,

Для указания пользователю на его ошибки.

"""

from __future__ import annotations
from argparse import ONE_OR_MORE
from copy import copy

import functools
import typing as _T

from rocshelf import exception as ex
from rocshelf.compile import routes
from rocshelf.components.routes import GetRoute


def main(targetFunc: _T.Callable,
         addTraceBackFun: _T.Callable[[ex.rExError, list[_T.Any], dict[str, _T.Any]], _T.Optional[ex.rExError]]
         ) -> _T.Any:
    """ Основной метод для добавления уровня трейсбека.

    Args:
        targetFunc (_T.Callable): Оборачиваямая функция
        addTraceBackFun (_T.Callable[[ex.rExError, list[_T.Any], dict[str, _T.Any]], _T.Optional[ex.rExError]]):
        Функция в которую передается ошибка и параметры вызова функции.

    Returns:
        _T.Any: Результат функции targetFunc

    """

    @functools.wraps(targetFunc)
    def wrapper(*args, **kwargs):
        try:
            return targetFunc(*args, **kwargs)

        except ex.rExError as exError:
            newError = addTraceBackFun(copy(exError), *args, **kwargs)
            if newError is None:
                raise exError
            raise newError

    return wrapper


class CompileTracebacks(object):
    """ Уровни tracebacks, которые появляются при компиляции маршрутов """

    @staticmethod
    def run(func: _T.Callable):
        def __add(exError: ex.rExError, *args, **kwargs):
            return None
        return main(func, __add)

    @staticmethod
    def analyze(func: _T.Callable):
        def __add(exError: ex.rExError, *args, **kwargs):
            return None
            exError.append_traceback(
                ex.ex.rTrText('Преанализ шаблонов')
            )
            raise exError
        return main(func, __add)

    @staticmethod
    def route_processing(func: _T.Callable):
        def __add(exError: ex.rExError, someSelf: routes.CompileRoute, *args, **kwargs):
            route = GetRoute.route(someSelf.routeKey)
            raise exError.append_traceback(
                ex.ex.rTrConfig(['route'] + someSelf.routeKey.split('.'), route.page)
            )
        return main(func, __add)

    @staticmethod
    def route_compile(func: _T.Callable):
        return CompileTracebacks.route_processing(func)

    @staticmethod
    def localization(func: _T.Callable):
        def __add(exError: ex.rExError, someSelf: routes.CompileRoutes, *args, **kwargs):
            return None
            exError.append_traceback(
                ex.ex.rTrText('Используемая локализация: "{0}"'.format(
                    someSelf.localizationName
                ))
            )
            raise exError
        return main(func, __add)


class TemplateTracebacks(object):
    """ Уровни tracebacks, которые появляются при компиляции маршрутов """  
    pass

    # @staticmethod
    # def file(func: _T.Callable):
    #     def __add(exError: ex.rExError, someSelf: routes.CompileRoutes, *args, **kwargs):
    #         exError.append_traceback(
    #             ex.ex.rTrFile(path, self.span)
    #         )
    #         raise exError
    #     return main(func, __add)