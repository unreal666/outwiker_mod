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


class QuoteToken (object):
    quoteStart = '[>'
    quoteEnd = '<]'
    anyExcept = Combine(ZeroOrMore(NotAny (Literal(quoteStart) | Literal(quoteEnd)) + CharsNotIn('', exact=1)))

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        token = Forward()
        token << (Suppress(QuoteToken.quoteStart) + Regex(TagAttrsPattern.value) +
                  (OneOrMore(QuoteToken.anyExcept + token) +
                   QuoteToken.anyExcept | QuoteToken.anyExcept) +
                  Suppress(QuoteToken.quoteEnd)).leaveWhitespace().setParseAction(self.__parse)("quote")
        return token


    def __parse (self, s, loc, toks):
        text = u''.join(toks[1:len(toks)])
        leftpos = text.find (u'<blockquote>')
        rightpos = text.rfind (u'</blockquote>')

        attrs = getAttributes(toks)

        if leftpos == -1 or rightpos == -1:
            return u''.join([u'<blockquote', attrs, u'>', self.parser.parseWikiMarkup (text), u'</blockquote>'])

        lefttext = text[:leftpos]
        righttext = text[rightpos:]
        centertext = text[leftpos:rightpos]

        return u''.join([
            u'<blockquote>',
            self.parser.parseWikiMarkup (lefttext),
            centertext,
            self.parser.parseWikiMarkup (righttext),
            u'</blockquote>'])
