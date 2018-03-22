# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


class TitleCommand(Command):
    """
    Команда для вставки тега <title>
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'title'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        title = '<title>{}</title>'.format(params)
        self.parser.appendToHead(title)
        return ''


class DescriptionCommand(Command):
    """
    Команда для вставки тега <meta name="description">
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'description'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        head = '<meta name="description" content="{}"/>'.format(params)
        self.parser.appendToHead(head)
        return ''


class KeywordsCommand(Command):
    """
    Команда для вставки тега <meta name="keywords">
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'keywords'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        head = '<meta name="keywords" content="{}"/>'.format(params)
        self.parser.appendToHead(head)
        return ''


class CustomHeadsCommand(Command):
    """
    Команда для вставки любых заголовков в тег <head>...</head>
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'htmlhead'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        [self.parser.appendToHead(head.strip()) for head in content.split('\n')]

        return ''


class HtmlAttrsCommand(Command):
    """
    Команда для вставки любых атрибутов в тег <html>.
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'htmlattrs'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        self.parser.appendToHtmlTag(params)
        return ''


class StyleCommand(Command):
    """
    Команда для вставки любых атрибутов в тег <html>.
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return 'style'

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        if params:
            params = ' %s' % params
        head = '<style{}>{}</style>'.format(params, content)
        self.parser.appendToHead(head)
        return ''


commands = (TitleCommand, DescriptionCommand,
            KeywordsCommand, CustomHeadsCommand,
            HtmlAttrsCommand, StyleCommand)
