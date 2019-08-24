# -*- coding: utf-8 -*-

import traceback

from . import wikitokens

from ..thumbnails import Thumbnails
from outwiker.libs.pyparsing import NoMatch


class Parser(object):
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.error_template = u"<b>{error}</b>"
        self.customProps = page.customProps

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        # Массив строк-атрибутов, которые надо добавить в тег <html>
        self.__htmlAttrs = ['']

        self.__footers = []

        # Команды, которые обрабатывает парсер.
        # Формат команд:(:name params... :) content...(:nameend:)
        # Ключ - имя команды, значение - экземпляр класса команды
        self.commands = {}

        wikitokens.initTokens(self, all=True)

        # Common wiki tokens
        self.wikiTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.quote,
            self.preformat,
            self.noformat,
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.lists,
            self.definitionList,
            self.table,
            self.headings,
            self.wikistyle_block,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside links
        self.linkTokens = [
            self.thumb,
            self.attachImages,
            self.urlImage,
            self.text,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.underlined,
            self.code,
            self.small,
            self.big,
            self.mark,
            self.strike,
            self.command,
            self.lineBreak,
            self.lineJoin,
            self.noformat,
            # self.wikistyle_inline,  # disabled due to program hang in some cases
        ]

        # Tokens for using inside headings
        self.headingTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.small,
            self.big,
            self.mark,
            self.noformat,
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside text
        self.textLevelTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.noformat,
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.wikistyle_block,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside list items (bullets and numeric)
        self.listItemsTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.preformat,
            self.noformat,
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.subscript,
            self.superscript,
            self.quote,
            self.definitionList,
            self.attaches,
            self.wikistyle_inline,
            self.command,
        ]

        self._wikiMarkup = None
        self._listItemMarkup = None
        self._linkMarkup = None
        self._headingMarkup = None
        self._textLevelMarkup = None

    def _createMarkup(self, tokens_list):
        return Markup(tokens_list)

    @property
    def head(self):
        """
        Свойство возвращает строку из добавленных заголовочных элементов
        (то, что должно быть внутри тега <head>...</head>)
        """
        return u"".join(self.__headers)

    def appendToHead(self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append(header)

    @property
    def headItems(self):
        '''
        Return list of the strings for the <head> HTML tag.

        Added in outwiker.core 1.3
        '''
        return self.__headers

    @property
    def footer(self):
        '''
        Added in outwiker.core 1.3
        '''
        return u''.join(self.__footers)

    @property
    def footerItems(self):
        '''
        Added in outwiker.core 1.3
        '''
        return self.__footers

    def appendToFooter(self, footer):
        """
        Added in outwiker.core 1.3
        """
        self.__footers.append(footer)

    @property
    def htmlAttrs(self):
        """
        Свойство возвращает строку из добавленных атрибутов для тега <html>
        """
        return u" ".join(self.__htmlAttrs)

    def appendToHtmlTag(self, attr):
        """
        Добавить строку-атрибуты в тег <html>
        """
        self.__htmlAttrs.append(attr)

    def toHtml(self, text):
        """
        Сгенерить HTML без заголовков типа <HTML> и т.п.
        """
        thumb = Thumbnails(self.page)
        thumb.clearDir()

        return self.parseWikiMarkup(text)

    def parseWikiMarkup(self, text):
        if self._wikiMarkup is None:
            self._wikiMarkup = self._createMarkup(self.wikiTokens)

        try:
            return self._wikiMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseListItemMarkup(self, text):
        if self._listItemMarkup is None:
            self._listItemMarkup = self._createMarkup(self.listItemsTokens)

        try:
            return self._listItemMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseLinkMarkup(self, text):
        if self._linkMarkup is None:
            self._linkMarkup = self._createMarkup(self.linkTokens)

        try:
            return self._linkMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseHeadingMarkup(self, text):
        if self._headingMarkup is None:
            self._headingMarkup = self._createMarkup(self.headingTokens)

        try:
            return self._headingMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseTextLevelMarkup(self, text):
        if self._textLevelMarkup is None:
            self._textLevelMarkup = self._createMarkup(self.textLevelTokens)

        try:
            return self._textLevelMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def addCommand(self, command, name=None):
        if not name:
            name = command.name
        self.commands[name] = command

    def removeCommand(self, commandName):
        if commandName in self.commands:
            del self.commands[commandName]


class Markup(object):
    def __init__(self, tokens_list):
        self._markup = NoMatch()
        for token in tokens_list:
            self._markup |= token

    def transformString(self, text):
        return self._markup.transformString(text)
