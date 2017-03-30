# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart, Literal, Suppress, FollowedBy
from .utils import TagAttrsPattern, getAttributes


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
        term = LineStart() + Regex (r"\^\^") + Regex(TagAttrsPattern.value) + term + LineEnd()
        term.setParseAction(self.__convertTerm).leaveWhitespace()

        description = Regex (r"(?P<text>(?:(?!(?<!\\)\n(?:<}}|\$\$.|\^\^.)).)*)", re.DOTALL)
        description = LineStart() + Regex (r"\$\$") + Regex(TagAttrsPattern.value) + description + LineEnd()
        description.setParseAction(self.__convertDescription).leaveWhitespace()

        definitionList = LineStart() + Regex (r"{{> *(?P<params>.+)?\s*") + \
                         OneOrMore (term | description) + Suppress("<}}") + Optional (FollowedBy (LineEnd()))
        definitionList.setParseAction(self.__convertDefinitionList)("definitionlist").leaveWhitespace()

        return definitionList


    def __convertTerm (self, s, loc, toks):
        text = u''.join(toks[2:len(toks)]).strip()
        attrs = getAttributes(toks)

        return u'<dt%s>%s</dt>' % (attrs, self.parser.parseWikiMarkup (text))


    def __convertDescription (self, s, loc, toks):
        text = u''.join(toks[2:len(toks)]).strip()
        attrs = getAttributes(toks)

        return u'<dd%s>%s</dd>' % (attrs, self.parser.parseWikiMarkup (text))


    def __convertDefinitionList (self, s, loc, toks):
        attrs = toks[0][3:].strip()
        attrs = u' %s' % attrs if attrs else ''
        result = []
        for element in toks[1:]:
            result.append(element)

        return u'<dl%s>%s</dl>' % (attrs, ''.join(result))
