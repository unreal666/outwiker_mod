# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart
from .utils import TagAttrsPattern


class TableFactory (object):
    @staticmethod
    def make (parser):
        return TableToken(parser).getToken()


class TableToken (object):
    """
    Токен для таблиц
    """
    def __init__ (self, parser):
        self.parser = parser
        self.unitEnd = "\n"


    def getToken (self):
        tableCell = Regex (r"(?P<text>(.|(?:\\\n))*?)(?:\\\n\s*)*(?P<end>\|\|\|?)" + TagAttrsPattern.value, re.UNICODE)
        tableCell.leaveWhitespace().setParseAction(self.__convertTableCell)

        tableRow = LineStart() + "||" + Regex (TagAttrsPattern.value, re.UNICODE) + OneOrMore (tableCell) + Optional (LineEnd())
        tableRow.setParseAction(self.__convertTableRow)

        table = LineStart() + Regex (r"\|\| *(?P<params>.+)?", re.UNICODE) + LineEnd() + OneOrMore (tableRow)
        table = table.setParseAction(self.__convertTable)("table")

        return table


    def __convertTableCell (self, s, loc, toks):
        text = toks["text"]

        leftAlign = text[-1] in u' \t'
        rightAlign = text[0] in u' \t'

        align = u''

        attrs = toks[TagAttrsPattern.name]
        attrs = u''.join([u' ', attrs]) if attrs else u''

        if leftAlign and rightAlign:
            align = u' align="center"'
        elif leftAlign:
            align = u' align="left"'
        elif rightAlign:
            align = u' align="right"'

        pattern =  u'<th%s%s>%s</th>' if toks["end"] == u'|||' else u'<td%s%s>%s</td>'

        return pattern % (align, attrs, self.parser.parseWikiMarkup (text.strip()))


    def __convertTableRow (self, s, l, t):
        if t[-1] == "\n":
            lastindex = len (t) - 1
        else:
            lastindex = len (t)
            self.unitEnd = ""

        attrs = t[TagAttrsPattern.name]
        attrs = u''.join([u' ', attrs]) if attrs else u''

        result = u''.join([u'<tr', attrs, u'>'])
        for element in t[2: lastindex]:
            result += element

        result += u'</tr>'

        return result


    def __convertTable (self, s, l, t):
        result = u'<table %s>' % t[0][2:].strip()
        for element in t[2:]:
            result += element

        result += u'</table>' + self.unitEnd

        return result
