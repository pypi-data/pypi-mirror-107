import rlogging
from rocshelf import exception as ex
from rocshelf.compile import meta, routes, utils
from rocshelf.traceback import CompileTracebacks

logger = rlogging.get_logger('mainLogger')


@CompileTracebacks.run
def run():
    """ Полная компиляция исходников опираясь на конфигурацию приложения

    Raises:
        exError: Добавление к трейсбеку сообщения, что запущена компиляция.

    """

    logger.info('Запуск компиляции')

    utils.backuping_last_compilation()
    utils.delete_dist()

    routes.run()
    meta.run()
