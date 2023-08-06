""" Работа с мета файломи """

import shutil

import rlogging
from rocshelf.config import cf

logger = rlogging.get_logger('mainLogger')


def move_files():
    """ Перенос файлов корневой директории """

    logger.info('Перемещение мата файлов из "import->meta" в "export->meta"')

    sourceFolderPath = cf.path('import', 'meta')
    targetFolderPath = cf.path('export', 'meta')

    if not sourceFolderPath.check():
        logger.warning('Перемещение мата файлов остановлено, так как папка "import->meta" не существует')
        return

    shutil.copytree(
        str(sourceFolderPath),
        str(targetFolderPath)
    )


def run():
    """ Запуск компиляции мета файлов """

    logger.info('Компиляция мета файлов')

    move_files()
