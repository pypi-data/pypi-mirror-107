
import rlogging
from rcore.rpath import rPath
from rocshelf.components.relations import relation
from rocshelf.config import cf

logger = rlogging.get_logger('mainLogger')


class StaticFile(object):

    staticFileName: str
    staticFilePath: rPath

    def __init__(self, staticFileName: str) -> None:
        self.staticFileName = staticFileName
        self.staticFilePath = cf.path('import', 'static').merge(staticFileName)

    def move_to_dist(self):
        """ Копирование медиа файла в папку экспорта """

        exportFolderPath = cf.path('export', 'static')
        exportFilePath = exportFolderPath.merge(self.staticFileName)

        logger.debug('Копирование медиа файла "{0}" в "{1}"'.format(
            self.staticFilePath,
            exportFilePath
        ))
        self.staticFilePath.copy_file(exportFilePath)
