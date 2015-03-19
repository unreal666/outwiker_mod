# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart, Literal, Suppress, FollowedBy


class DefinitionListFactory (object):
    @staticmethod
    def make (parser):
        return DefinitionListToken(parser).getToken()


class DefinitionListToken (object):
    """
    Токен для таблиц
    """
    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        term = Regex (r"(?P<text>(?:(?:\\\n)|.)*)\s*(?=\n)")
        term = LineStart() + Regex (r"\^\^") + term + LineEnd()
        term.setParseAction(self.__convertTerm).leaveWhitespace()

        description = Regex (r"(?P<text>(?:(?!(?<!\\)\n(?:<}}|\$\$.|\^\^.)).)*)", re.DOTALL)
        description = LineStart() + Regex (r"\$\$") + description + LineEnd()
        description.setParseAction(self.__convertDescription).leaveWhitespace()

        definitionList = LineStart() + Regex (r"{{> *(?P<params>.+)?\s*") + \
                         OneOrMore (term | description) + Suppress("<}}") + Optional (FollowedBy (LineEnd()))
        definitionList.setParseAction(self.__convertDefinitionList)("definitionlist").leaveWhitespace()

        return definitionList


    def __convertTerm (self, s, l, t):
        return u'<dt>%s</dt>' % (self.parser.parseTextLevelMarkup (t["text"].strip()))


    def __convertDescription (self, s, l, t):
        return u'<dd>%s</dd>' % (self.parser.parseWikiMarkup (t["text"].strip()))


    def __convertDefinitionList (self, s, l, t):
        result = u"<dl %s>" % t[0][3:].strip()
        for element in t[1:]:
            result += element

        result += "</dl>"

        return result
