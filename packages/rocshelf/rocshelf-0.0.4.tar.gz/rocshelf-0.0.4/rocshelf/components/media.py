""" Модуль работы с медиа файлами

"""

import rlogging
from PIL import Image
from rcore.rpath import rPath
from rocshelf.components.relations import relation
from rocshelf.config import cf

logger = rlogging.get_logger('mainLogger')

image_extensions = ['.png', '.jpeg']
video_extensions = ['.mp4', ]

saveMediaFiles = 'rocshelf-media.json'

filesRelations: dict[str, str] = {}


def compression(path: str, percent: int):
    """ Сжатие фала

    Args:
        path (str): Путь до файла
        percent (int): Процент сжатия

    """


def add(fileName: str):
    """ Добавление нового файла """

    logger.info(f'Добавление нового медиа файла: "{fileName}"')


def add_link(link: str):
    """ Добавление нового файла по ссылке """

    logger.info(f'Добавление нового медиа файла по ссылке: "{link}"')


def init():
    """ Инициализация медиа файлами """

    logger.info('Инициализация медиа файлов')


class MediaFile(object):
    """ Интерфейс для управления медиа файлами """

    mediaFileName: str
    mediaFilePath: rPath

    def __init__(self, mediaFileName: str) -> None:
        self.mediaFileName = mediaFileName
        self.mediaFilePath = cf.path('import', 'media').merge(mediaFileName)

    def move_to_dist(self):
        """ Копирование медиа файла в папку экспорта """

        exportFolderPath = cf.path('export', 'media')
        exportFilePath = exportFolderPath.merge(self.mediaFileName)

        logger.debug('Копирование медиа файла "{0}" в "{1}"'.format(
            self.mediaFilePath,
            exportFilePath
        ))
        self.mediaFilePath.copy_file(exportFilePath)
