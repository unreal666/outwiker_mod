# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Forward, CharsNotIn, NotAny, ZeroOrMore, OneOrMore, Combine, Literal, Suppress, Regex
from .utils import TagAttrsPattern, getAttributes


class QuoteFactory (object):
    """
    Фабрика для создания токена для цитат
    """
    @staticmethod
    def make (parser):
        return QuoteToken(parser).getToken()


class QuoteToken(object):
    quoteStart = '[>'
    quoteEnd = '<]'

    def __init__(self, parser):
        self.parser = parser


    def getToken(self):
        anyExcept = Combine(ZeroOrMore(NotAny(Literal(QuoteToken.quoteStart) | Literal(QuoteToken.quoteEnd)) + CharsNotIn('', exact=1)))
        anyExcept = anyExcept.leaveWhitespace().setParseAction(self.__parseText)
        token = Forward()
        token << (Suppress(QuoteToken.quoteStart) + Regex(TagAttrsPattern.value) +
                  (OneOrMore(anyExcept + token) + anyExcept | anyExcept) +
                  Suppress(QuoteToken.quoteEnd)).leaveWhitespace().setParseAction(self.__parse)("quote")
        return token


    def __parse(self, s, loc, toks):
        text = u''.join(toks[1:len(toks)])
        attrs = getAttributes(toks)

        return '<blockquote%s>%s</blockquote>' % (attrs, text)


    def __parseText(self, s, loc, toks):
        return self.parser.parseWikiMarkup (u''.join(toks))
