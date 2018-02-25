# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart, Suppress, Empty, OnlyOnce
from .utils import TagAttrsPattern, getAttributes


class TableFactory(object):
    @staticmethod
    def make(parser):
        return TableToken(parser).getToken()


class TableToken(object):
    """
    Токен для таблиц
    """
    rowGroupsLabels = {'|||': 'thead', '||||': 'tfoot'}

    def __init__(self, parser):
        self.parser = parser


    def getToken(self):
        emptyToken = Empty().setParseAction(self.__initVars)

        tableCell = Regex(r'(?P<text>(.|(?:\\\n))*?)(?:\\\n\s*)*(?P<end>\|\|\|?)' + TagAttrsPattern.value)
        tableCell.leaveWhitespace().setParseAction(self.__convertTableCell)

        tableRow = LineStart() + Regex(r'\|{2,4}(?!\|)' + TagAttrsPattern.value) + \
                   OneOrMore(tableCell) + Optional(LineEnd())
        tableRow.leaveWhitespace().setParseAction(self.__convertTableRow)

        tableCaption = LineStart() + Regex(r'(?P<start>\|{5})' + TagAttrsPattern.value +
                                            r'(?P<text>(.|(?:\\\n))*)(?:\\\n\s*)*') + Optional(LineEnd())
        tableCaption.leaveWhitespace().setParseAction(self.__convertTableCaption)

        table = LineStart() + Regex(r'\|\| *(?P<params>.+)?') + Suppress(LineEnd()) + emptyToken + \
                Suppress(Optional(tableCaption)) + OneOrMore(tableRow)
        table = table.setParseAction(self.__convertTable)('table')

        return table

    def __initVars(self):
        self.unitEnd = '\n'
        self.rowGroups = {'thead': u'', 'tfoot': u'', 'caption': u''}


    def __convertTableCell(self, s, loc, toks):
        text = toks['text']

        isTh = False if toks['end'] != u'|||' else True

        leftAlign = text[-1] in u' \t'
        rightAlign = text[0] in u' \t'

        align = u''

        attrs = getAttributes(toks)

        if leftAlign and rightAlign:
            align = u' align="center"'
        elif isTh and leftAlign:
            align = u' align="left"'
        elif rightAlign:
            align = u' align="right"'

        pattern = u'<th%s%s>%s</th>' if isTh else u'<td%s%s>%s</td>'

        return pattern % (align, attrs, self.parser.parseWikiMarkup(text.strip()))


    def __convertTableRow(self, s, loc, toks):
        rowStart = toks[0]

        if toks[-1] == '\n':
            lastindex = len(toks) - 1
        else:
            lastindex = len(toks)
            self.unitEnd = ''

        attrs = getAttributes(toks)

        result = u''.join([u'<tr', attrs, u'>']) + u''.join(toks[1: lastindex]) + u'</tr>'

        if rowStart in TableToken.rowGroupsLabels:
            self.rowGroups[TableToken.rowGroupsLabels[rowStart]] += result
            return u''
        else:
            return result


    def __convertTableCaption(self, s, loc, toks):
        attrs = getAttributes(toks)

        self.rowGroups['caption'] = u'<caption%s>%s</caption>' % (attrs, self.parser.parseWikiMarkup(toks['text'].strip()))

        return None


    def __convertTable(self, s, loc, toks):
        thead = self.rowGroups['thead']
        tfoot = self.rowGroups['tfoot']
        caption = self.rowGroups['caption']

        if thead != u'':
            thead = u''.join([u'<thead>', thead, u'</thead>'])
        if tfoot != u'':
            tfoot = u''.join([u'<tfoot>', tfoot, u'</tfoot>'])

        return u'<table %s>' % toks[0][2:].strip() + caption + thead + tfoot + u''.join(toks[1:]) + u'</table>' + self.unitEnd
