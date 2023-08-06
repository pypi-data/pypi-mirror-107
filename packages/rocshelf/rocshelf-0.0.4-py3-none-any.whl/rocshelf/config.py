""" Модуль конфигурирования приложения

"""

from __future__ import annotations

import typing as _T

from rcore import config
from rcore.rpath import rPath
from rcore.rtype import Validator

config_rules = [
    config.CfgRule(
        'Основные настройки компиляции',
        ['setting', 'settings'], Validator(dict, [], {}),
        [
            config.CfgRule(
                'Степень сжатия кода при компиляции',
                ['compression'], Validator(str, ['nested', 'expanded', 'compact', 'compressed'], 'nested'),
            ),
            config.CfgRule(
                'Сохранять предыдущие версии компиляции в папку cache/versions',
                ['backup'], Validator(bool, [False, True], False),
            ),
            config.CfgRule(
                'Очищать папку экспорта перед компиляцией',
                ['deldist'], Validator(bool, [False, True], False),
            ),
        ]
    ),

    config.CfgRule(
        'Инициализация маршрутов. Основываясь на этом словаре будут компилироваться страницы.',
        ['route', 'routes'], Validator(dict, [], {})
    ),

    config.CfgRule(
        'Инициализация путей.',
        ['path', 'paths'], Validator(dict, [], {}),
        [
            config.CfgRule(
                'Пути до экспорта файлов.',
                ['export', 'exports'], Validator(dict, [], {}),
                [
                    config.CfgRule(
                        'Для страниц.',
                        ['template'], Validator(str, [], 'template'),
                    ),
                    config.CfgRule(
                        'Для статики',
                        ['static'], Validator(str, [], 'static'),
                    ),
                    config.CfgRule(
                        'Для медиа файлов',
                        ['media'], Validator(str, [], 'media'),
                    ),
                ]
            ),

            config.CfgRule(
                'Пути для импорта файлов.',
                ['import', 'imports'], Validator(dict, [], {}),
                [
                    config.CfgRule(
                        'Файлы локализации',
                        ['local', 'localization'], Validator(str, [], 'localization'),
                    ),
                    config.CfgRule(
                        'Медиа файлы',
                        ['media'], Validator(str, [], 'media'),
                    ),
                    config.CfgRule(
                        'Файлы статики',
                        ['static'], Validator(str, [], 'static'),
                    ),
                    config.CfgRule(
                        'Папка для импорта групп шелфов.',
                        ['groups'], Validator(str, [], 'groups'),
                    ),

                    config.CfgRule(
                        'Шелфы страниц.',
                        ['page', 'pages', 'pg'],
                        Validator(dict, [], {})
                    ),
                    config.CfgRule(
                        'Шелфы оберток.',
                        ['wrapper', 'wrappers', 'wp'],
                        Validator(dict, [], {})
                    ),
                    config.CfgRule(
                        'Шелфы тегов.',
                        ['tag', 'tags', 'tg'],
                        Validator(dict, [], {})
                    ),
                    config.CfgRule(
                        'Шелфы блоков.',
                        ['block', 'blocks', 'bl'],
                        Validator(dict, [], {})
                    )
                ]
            )
        ]
    )
]


class WorkingConfig(config.ConfigEngine):

    rules = config_rules

    def preparation(self):
        self.merge()
        self.use_rule()
        self.path_common()
        self.save()
        self.prepared = True


class CompletedConfig(config.ConfigEngine):

    def preparation(self):
        self.init({
            'project.cache': ['rocshelf-compiled.json']
        })
        self.merge()

        self.save()
        self.prepared = True

    def save_compiled(self, pages: dict):
        """Сохранение необходимой информации для работы функционал интеграции с фреймворками python

        Args:
            pages (dict): Словарь, где ключ - идентификатор маршрута, а значение информация о странице

        """

        distConfig = {
            'export': self.config.get(['path', 'export']),
            'template': {key: pages[key].file for key in pages}
        }
        rPath('rocshelf-compiled.json', fromPath='project.cache').dump(distConfig)


class WorkingCf(config.CfEngine):

    def shelf(self, shelfType: str, shelfName: str) -> rPath:
        dictpath = ['shelves', shelfType, shelfName]
        return copy(self.get(dictpath))

    def shelves(self, shelfType: _T.Union[str, None] = None) -> dict:
        dictpath = ['shelves']

        if shelfType is not None:
            dictpath.append(shelfType)

        return self.get(dictpath)

    def route(self, route: _T.Union[str, bool] = False):
        if round:
            return self.get(['route', route])
        
        return self.get(['route'])


cf = WorkingCf(WorkingConfig())
cfCompleted = config.CfEngine(CompletedConfig())
