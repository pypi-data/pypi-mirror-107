""" Модуль компиляции страниц.

Компиляция зависит от следующих параметров:
    Маршруты (настройка route): каждый маршрут - это отдельная страница
    Файлы локализации (настройка path -> import -> localization):
        На каждый файл с расширением .lang будет производиться итерация компиляция страниц из пункта выше.
        Результат компиляции каждого файла локализации будет храниться в папке с именем файла локализации.

"""
from __future__ import annotations

import multiprocessing
import typing as _T
from chunk import Chunk

import rlogging
from bs4 import BeautifulSoup
from rcore import rthread
from rcore.rpath import rPath
from rocshelf import exception as ex
from rocshelf.compile import compile_static
from rocshelf.compile.params import TemplateCompilationMetaData
from rocshelf.components import localization, routes, shelves
from rocshelf.components.relations import relation
from rocshelf.components.routes import GetRoute
from rocshelf.config import cf
from rocshelf.frontend import chunks
from rocshelf.template.basic import ProcessingOutputNode, ProcessingParams
from rocshelf.template.shelves import ShelfNode, ShelfPageNode

logger = rlogging.get_logger('mainLogger')


def pre_analyze():
    """ Запуск анализатора шаблонов.

    Нужен для прочтения всех файлов, разбитие их на литералы и предварительную обработку.

    """

    logger.info('Анализ всех используемых shelf-страниц')

    for routeKey, route in GetRoute.walk():
        logger.debug('Анализ shelf-страницы "{0}" на которую ссылается маршрут "{1}"'.format(
            route.page,
            routeKey
        ))
        ShelfPageNode(route.page)


class CompileRoute(object):
    """ Класс в рамках которого происходит компиляция одного маршрута для одной локации """

    routeKey: str
    localizationName: str

    procParams: ProcessingParams
    shelfNode: ShelfNode

    processingNode: ProcessingOutputNode

    def __init__(self, routeKey: str, localizationName: str) -> None:
        self.routeKey = routeKey
        self.localizationName = localizationName

        route = GetRoute.route(routeKey)

        self.procParams = TemplateCompilationMetaData.processing_params(routeKey, localizationName)
        self.shelfNode = ShelfPageNode(route.page)

        self.processingNode = None

    def processing(self):
        """ Обработка маршрута """

        logger.info('Обработка маршрута "{0}" с локализацией "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        self.processingNode = self.shelfNode.processing(self.procParams)

    def compile(self) -> str:
        """ Компиляция маршрута

        Raises:
            ValueError: Маршрут не прошел обработку

        Returns:
            str: Скомпилированный текст

        """

        logger.info('Компиляция маршрута "{0}" в локализации "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        if self.processingNode is None:
            raise ValueError('Сначала нужно обработать узлы с помощью "CompileRoute.processing"')

        return self.processingNode.compile(self.procParams)


class CompileRoutes(rthread.OnAsyncMixin):
    """ Класс в рамках которого происходит компиляция всех маршрутов для одной локации """

    localizationName: _T.Optional[str]

    processingRoutes: dict[str, CompileRoute]
    chunks: Chunk

    def __init__(self, localizationName: _T.Optional[str] = None) -> None:
        self.processingRoutes = {}

        self.localizationName = localizationName
        relation.set_local(self.localizationName)

    def processing(self):
        """ Обработка.

        Raises:
            append_traceback: Во время компиляции что-то пошло не так

        """

        logger.info('Обработка инициализированных маршутов в локализации "{0}"'.format(
            self.localizationName
        ))

        for routeKey, route in GetRoute.walk():

            filePath = relation.template_path(routeKey)

            if not filePath.check():
                filePath.create()

            try:
                self.processingRoutes[routeKey] = CompileRoute(routeKey, self.localizationName)
                self.processingRoutes[routeKey].processing()

            except ex.rExError as exDeconstructError:
                raise exDeconstructError.append_traceback(
                    ex.ex.rTrConfig(['route'] + routeKey.split('.'), route.page)
                )

    def analyze_static(self):
        """ Передача собраных данных в анализатор статики """

        logger.info('Передача собраных, во время компиляции маршутов в локализации "{0}", данных в анализатор статики'.format(
            self.localizationName
        ))

        staticProcessingData = {
            'shelves': {}
        }

        for routeKey, compileRoute in self.processingRoutes.items():
            staticProcessingData['shelves'][routeKey] = set(compileRoute.processingNode.collectedData['shelves'])

        staticAnalyze = chunks.StaticAnalyze.all_stages(
            staticProcessingData
        )

        self.chunks = staticAnalyze.chunks

    def compile_static(self):
        """ Компиляция и сохранение групп статики """

        compile_static.start_compile(
            self.chunks,
            self.localizationName
        )

    def update_proc_params(self):
        """ Обнуление параметров компиляции после анализа статики """

        for routeKey, compileRoute in self.processingRoutes.items():
            targetChunks = [chunk for chunk in self.chunks if routeKey in chunk.routeKeys]

            # localbars -> __meta__ -> chunks
            compileRoute.procParams.localVars['__meta__'].add_chucks(targetChunks)

    def compile_templates(self):
        """ Компиляция и сохранение.

        Raises:
            append_traceback: Во время компиляции что-то пошло не так

        """

        logger.info('Компиляция всех инициализированных маршутов в локализации "{0}"'.format(
            self.localizationName
        ))

        for _, compileRoute in self.processingRoutes.items():
            compileRoute.compile()

        logger.info('Сохранение  всех инициализированных маршутов в локализации "{0}"'.format(
            self.localizationName
        ))

        for routeKey, compileRoute in self.processingRoutes.items():

            filePath = relation.template_path(routeKey)

            try:
                compiledText = compileRoute.compile()

            except ex.rExError as exDeconstructError:
                raise exDeconstructError.append_traceback(
                    ex.ex.rTrConfig(['route'] + routeKey.split('.'), GetRoute.route(routeKey).page)
                )

            filePath.write(compiledText, 'w')

    def normalize_html(self):
        """ Нормализация html страницы """

        logger.info('Нормализация Html страниц всех маршрутов')

        for routeKey in GetRoute.all():
            pageFile = relation.template_path(routeKey)

            logger.debug('Нормализация Html страницы "{0}" маршрута "{1}"'.format(
                pageFile, routeKey
            ))

            pageText = pageFile.read()

            soup = BeautifulSoup(pageText, 'html.parser')

            pageFile.write(
                soup.prettify(), 'w'
            )

    def on_process(self):
        self.processing()

        self.analyze_static()
        self.compile_static()

        self.update_proc_params()
        self.compile_templates()

        self.normalize_html()


def start_compile():
    """ Полная компиляция исходников опираясь на конфигурацию приложения """

    logger.info('Запуск компиляции')

    backuping_last_compilation()
    delete_dist()

    pre_analyze()

    if not localization.localsData:
        logger.info('Локализаций нет. Однопоточная компиляция')

        CompileRoutes(None).on_process()
        return

    # Реализация параллельной компиляции
    logger.info('Инициализированно несколько локализаций. Запущена параллельная компиляция в {0} процессов'.format(
        len(localization.localsData)
    ))

    processesPool = rthread.ProcessesPool()

    for local in localization.localsData:
        processesPool.append(CompileRoutes.run_process(local))

    processesPool.join()


def backuping_last_compilation():
    """ Создание backup`а прошлой компиляции.

    Архивирует прошлую версию скомпилированного приложения.
    Сохраняются все исходники и некоторые кеши.

    Делать бекап или нет решает настройка `setting->backup`

    """

    logger.info('Создание backup`а прошлой компиляции')

    if not cf.setting('backup'):
        logger.debug('Создание backup`а пропущено, так как настройка setting->backup имеет значение False')
        return

    latsCompilationDataFile = rPath('rocshelf-compilation.json', fromPath='project.cache')

    if not latsCompilationDataFile.check():
        logger.info('Создание backup`а пропущено, так как нет файла с информацией о прошлой компиляции')
        return

    latsCompilationData = latsCompilationDataFile.parse()


def delete_dist():
    """ Очистка папок, куда будет сохранен результат компиляции

    Очищать папки или нет решает настройка `setting->deldist`

    """

    logger.info('Очистка папок экспорта')

    if not cf.setting('deldist'):
        logger.debug('Очистка папок экспорта пропущено, так как настройка setting->deldist имеет значение False')
        return

    for exportFolderName in ['template', 'static', 'media']:
        exportFolderPath = cf.path('export', exportFolderName)

        logger.warning('Удаление папки экспорта "{0}" по пути "{1}"'.format(
            exportFolderName,
            exportFolderPath
        ))
        exportFolderPath.delete()
