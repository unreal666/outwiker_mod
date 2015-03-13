# -*- coding: UTF-8 -*-

import wx
import wx.lib.newevent
import wx.stc

import threading

from .parser.tokenfonts import FontsFactory
from .parser.tokenheading import HeadingFactory
from .parser.tokencommand import CommandFactory
from .parser.tokenlink import LinkFactory
from .parser.tokenurl import UrlFactory
from .parser.tokenlinebreak import LineBreakFactory
from .parser.tokennoformat import NoFormatFactory
from .parser.tokenpreformat import PreFormatFactory
from .parser.tokentext import TextFactory
from .parser.utils import returnNone


ApplyStyleEvent, EVT_APPLY_STYLE = wx.lib.newevent.NewEvent()


class WikiColorizer (object):
    def __init__ (self, editor):
        self._editor = editor

        self.isFakeParser = True
        _returnNone = returnNone

        if not hasattr(self, 'text'): self.text = TextFactory.make (self)
        if not hasattr(self, 'bolded'): self.bolded = FontsFactory.makeBold (self).setParseAction(_returnNone)
        if not hasattr(self, 'italicized'): self.italicized = FontsFactory.makeItalic (self).setParseAction(_returnNone)
        if not hasattr(self, 'boldItalicized'): self.boldItalicized = FontsFactory.makeBoldItalic (self).setParseAction(_returnNone)
        if not hasattr(self, 'underlined'): self.underlined = FontsFactory.makeUnderline (self).setParseAction(_returnNone)
        if not hasattr(self, 'headings'): self.headings = HeadingFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'command'): self.command = CommandFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'link'): self.link = LinkFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'url'): self.url = UrlFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'lineBreak'): self.lineBreak = LineBreakFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'noformat'): self.noformat = NoFormatFactory.make (self).setParseAction(_returnNone)
        if not hasattr(self, 'preformat'): self.preformat = PreFormatFactory.make (self).setParseAction(_returnNone)

        self.colorParser = (
            self.url |
            self.text |
            self.lineBreak |
            self.link |
            self.noformat |
            self.preformat |
            self.command |
            self.boldItalicized |
            self.bolded |
            self.italicized |
            self.underlined |
            self.headings)

        self.insideBlockParser = (
            self.url |
            self.text |
            self.lineBreak |
            self.link |
            self.noformat |
            self.preformat |
            self.boldItalicized |
            self.bolded |
            self.italicized |
            self.underlined)

        self._thread = None


    def start (self, text):
        if (self._thread is None or
                not self._thread.isAlive()):
            self._thread = threading.Thread (None, self._threadFunc, args=(text,))
            self._thread.start()


    def _threadFunc (self, text):
        stylebytes = self._startColorize (text)
        event = ApplyStyleEvent (text=text, stylebytes=stylebytes)
        wx.PostEvent (self._editor, event)


    def _startColorize (self, text):
        textlength = self._editor.calcByteLen (text)
        stylelist = [wx.stc.STC_STYLE_DEFAULT] * textlength

        self._colorizeText (text, 0, textlength, self.colorParser, stylelist)

        stylebytes = "".join ([chr(byte) for byte in stylelist])
        return stylebytes


    def _colorizeText (self, text, start, end, parser, stylelist):
        tokens = parser.scanString (text[start: end])

        for token in tokens:
            pos_start = token[1] + start
            pos_end = token[2] + start

            tokenname = token[0].getName()
            # print tokenname

            if (tokenname == "text" or
                    tokenname == "linebreak" or
                    tokenname == "noformat" or
                    tokenname == "preformat"):
                continue

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self._editor.calcBytePos (text, pos_start)
            bytepos_end = self._editor.calcBytePos (text, pos_end)

            # Применим стиль
            if tokenname == "bold":
                self._addStyle (stylelist, self._editor.STYLE_BOLD_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, self.insideBlockParser, stylelist)

            elif tokenname == "italic":
                self._addStyle (stylelist, self._editor.STYLE_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 2, pos_end - 2, self.insideBlockParser, stylelist)

            elif tokenname == "bold_italic":
                self._addStyle (stylelist, self._editor.STYLE_BOLD_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 4, pos_end - 4, self.insideBlockParser, stylelist)

            elif tokenname == "underline":
                self._addStyle (stylelist, self._editor.STYLE_UNDERLINE_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 2, pos_end - 2, self.insideBlockParser, stylelist)

            elif tokenname == "heading":
                self._setStyle (stylelist, self._editor.STYLE_HEADING_ID, bytepos_start, bytepos_end)

            elif tokenname == "command":
                self._setStyle (stylelist, self._editor.STYLE_COMMAND_ID, bytepos_start, bytepos_end)

            elif tokenname == "link":
                self._addStyle (stylelist, self._editor.STYLE_LINK_ID, bytepos_start, bytepos_end)

            elif tokenname == "url":
                self._addStyle (stylelist, self._editor.STYLE_LINK_ID, bytepos_start, bytepos_end)


    def _addStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [styleid if style == wx.stc.STC_STYLE_DEFAULT else style | styleid for style in style_src]

        stylelist[bytepos_start: bytepos_end] = style_new


    def _setStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        stylelist[bytepos_start: bytepos_end] = [styleid] * (bytepos_end - bytepos_start)
