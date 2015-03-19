# -*- coding: UTF-8 -*-

import traceback

from .tokenfonts import FontsFactory
from .tokennoformat import NoFormatFactory
from .tokenpreformat import PreFormatFactory
from .tokenthumbnail import ThumbnailFactory
from .tokenheading import HeadingFactory
from .tokenadhoc import AdHocFactory
from .tokenhorline import HorLineFactory
from .tokenlink import LinkFactory
from .tokenalign import AlignFactory
from .tokentable import TableFactory
from .tokenurl import UrlFactory
from .tokenurlimage import UrlImageFactory
from .tokenattach import AttachFactory, AttachImagesFactory
from .tokenlist import ListFactory
from .tokenlinebreak import LineBreakFactory
from .tokenlinejoin import LineJoinFactory
from .tokentex import TexFactory
from .tokencommand import CommandFactory
from .tokentext import TextFactory
from .tokenquote import QuoteFactory
from .tokendefinitionlist import DefinitionListFactory

from ..thumbnails import Thumbnails


class Parser (object):
    def __init__ (self, page, config):
        self.page = page
        self.config = config
        self.error_template = u"<B>{error}</B>"

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        # Команды, обрабатывает парсер.
        # Формат команд: (:name params... :) content... (:nameend:)
        # Ключ - имя команды, значение - экземпляр класса команды
        self.commands = {}

        if not hasattr(self, 'italicized'): self.italicized = FontsFactory.makeItalic (self)
        if not hasattr(self, 'bolded'): self.bolded = FontsFactory.makeBold (self)
        if not hasattr(self, 'boldItalicized'): self.boldItalicized = FontsFactory.makeBoldItalic (self)
        if not hasattr(self, 'underlined'): self.underlined = FontsFactory.makeUnderline (self)
        if not hasattr(self, 'strike'): self.strike = FontsFactory.makeStrike (self)
        if not hasattr(self, 'subscript'): self.subscript = FontsFactory.makeSubscript (self)
        if not hasattr(self, 'superscript'): self.superscript = FontsFactory.makeSuperscript (self)
        if not hasattr(self, 'quote'): self.quote = QuoteFactory.make (self)
        if not hasattr(self, 'code'): self.code = FontsFactory.makeCode (self)
        if not hasattr(self, 'small'): self.small = FontsFactory.makeSmall(self)
        if not hasattr(self, 'big'): self.big = FontsFactory.makeBig(self)
        if not hasattr(self, 'headings'): self.headings = HeadingFactory.make(self)
        if not hasattr(self, 'thumb'): self.thumb = ThumbnailFactory.make(self)
        if not hasattr(self, 'noformat'): self.noformat = NoFormatFactory.make(self)
        if not hasattr(self, 'preformat'): self.preformat = PreFormatFactory.make (self)
        if not hasattr(self, 'horline'): self.horline = HorLineFactory.make(self)
        if not hasattr(self, 'link'): self.link = LinkFactory.make (self)
        if not hasattr(self, 'align'): self.align = AlignFactory.make(self)
        if not hasattr(self, 'table'): self.table = TableFactory.make(self)
        if not hasattr(self, 'url'): self.url = UrlFactory.make (self)
        if not hasattr(self, 'urlImage'): self.urlImage = UrlImageFactory.make (self)
        if not hasattr(self, 'attaches'): self.attaches = AttachFactory.make (self)
        if not hasattr(self, 'attachImages'): self.attachImages = AttachImagesFactory.make (self)
        if not hasattr(self, 'adhoctokens'): self.adhoctokens = AdHocFactory.make(self)
        if not hasattr(self, 'lists'): self.lists = ListFactory.make (self)
        if not hasattr(self, 'definitionList'): self.definitionList = DefinitionListFactory.make (self)
        if not hasattr(self, 'lineBreak'): self.lineBreak = LineBreakFactory.make (self)
        if not hasattr(self, 'lineJoin'): self.lineJoin = LineJoinFactory.make (self)
        if not hasattr(self, 'tex'): self.tex = TexFactory.make (self)
        if not hasattr(self, 'command'): self.command = CommandFactory.make (self)
        if not hasattr(self, 'text'): self.text = TextFactory.make(self)

        self.listItemMarkup = (self.attaches |
                               self.urlImage |
                               self.url |
                               self.text |
                               self.lineBreak |
                               self.lineJoin |
                               self.link |
                               self.boldItalicized |
                               self.bolded |
                               self.italicized |
                               self.code |
                               self.small |
                               self.big |
                               self.preformat |
                               self.noformat |
                               self.thumb |
                               self.underlined |
                               self.strike |
                               self.subscript |
                               self.superscript |
                               self.quote |
                               self.definitionList |
                               self.attaches |
                               self.tex |
                               self.command
                               )


        self.wikiMarkup = (self.attaches |
                           self.urlImage |
                           self.url |
                           self.text |
                           self.lineBreak |
                           self.lineJoin |
                           self.link |
                           self.adhoctokens |
                           self.subscript |
                           self.superscript |
                           self.boldItalicized |
                           self.bolded |
                           self.italicized |
                           self.code |
                           self.small |
                           self.big |
                           self.quote |
                           self.preformat |
                           self.noformat |
                           self.thumb |
                           self.underlined |
                           self.strike |
                           self.horline |
                           self.align |
                           self.definitionList |
                           self.lists |
                           self.table |
                           self.headings |
                           self.tex |
                           self.command
                           )

        # Нотация для ссылок
        self.linkMarkup = (self.attachImages |
                           self.urlImage |
                           self.text |
                           self.adhoctokens |
                           self.subscript |
                           self.superscript |
                           self.boldItalicized |
                           self.bolded |
                           self.italicized |
                           self.underlined |
                           self.small |
                           self.big |
                           self.strike |
                           self.tex |
                           self.command |
                           self.lineBreak |
                           self.lineJoin |
                           self.noformat
                           )

        # Нотация для заголовков
        self.headingMarkup = (self.attaches |
                              self.urlImage |
                              self.url |
                              self.text |
                              self.lineBreak |
                              self.lineJoin |
                              self.link |
                              self.adhoctokens |
                              self.subscript |
                              self.superscript |
                              self.boldItalicized |
                              self.bolded |
                              self.italicized |
                              self.small |
                              self.big |
                              self.noformat |
                              self.thumb |
                              self.underlined |
                              self.strike |
                              self.horline |
                              self.align |
                              self.tex |
                              self.command
                              )

        # Нотация для форматированного текста
        self.textLevelMarkup = (self.attaches |
                                self.urlImage |
                                self.url |
                                self.text |
                                self.lineBreak |
                                self.lineJoin |
                                self.link |
                                self.adhoctokens |
                                self.subscript |
                                self.superscript |
                                self.boldItalicized |
                                self.bolded |
                                self.italicized |
                                self.code |
                                self.small |
                                self.big |
                                self.noformat |
                                self.thumb |
                                self.underlined |
                                self.strike |
                                self.horline |
                                self.tex |
                                self.command
                                )


    @property
    def head (self):
        """
        Свойство возвращает строку из добавленных заголовочных элементов (то, что должно быть внутри тега <HEAD>...</HEAD>)
        """
        return u"\n".join (self.__headers)


    def appendToHead (self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append (header)


    def toHtml (self, text):
        """
        Сгенерить HTML без заголовков типа <HTML> и т.п.
        """
        thumb = Thumbnails (self.page)
        thumb.clearDir()

        return self.parseWikiMarkup(text)


    def parseWikiMarkup (self, text):
        try:
            return self.wikiMarkup.transformString (text)
        except Exception:
            return self.error_template.format (error = traceback.format_exc())


    def parseListItemMarkup (self, text):
        try:
            return self.listItemMarkup.transformString (text)
        except Exception:
            return self.error_template.format (error = traceback.format_exc())


    def parseLinkMarkup (self, text):
        try:
            return self.linkMarkup.transformString (text)
        except Exception:
            return self.error_template.format (error = traceback.format_exc())


    def parseHeadingMarkup (self, text):
        try:
            return self.headingMarkup.transformString (text)
        except Exception:
            return self.error_template.format (error = traceback.format_exc())


    def parseTextLevelMarkup (self, text):
        try:
            return self.textLevelMarkup.transformString (text)
        except Exception:
            return self.error_template.format (error = traceback.format_exc())


    def addCommand (self, command):
        self.commands[command.name] = command
