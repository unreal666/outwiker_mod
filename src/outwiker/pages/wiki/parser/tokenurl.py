# -*- coding: utf-8 -*-

import re

from outwiker.libs.pyparsing import Regex, NoMatch


class UrlFactory (object):
    @staticmethod
    def make(parser):
        return UrlToken(parser).getToken()


class UrlToken (object):
    def __init__(self, parser):
        self.parser = parser
        if not hasattr(parser, 'customProps'): parser.customProps = {}
        parser.customProps.setdefault('parsing', {}).setdefault('tokenurl', True)

    def getToken(self):
        if self.parser.customProps['parsing']['tokenurl'] is not False:
            token = Regex(
            r'((?# Начало разбора IP )(?<!\.)(?:25[0-5]|2[0-4]\d|1\d\d|0?[1-9]\d|0{,2}[1-9])(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d?\d)){3}(?!\.[0-9])(?!\w)(?# Конец разбора IP )|(((news|telnet|nttp|file|https?|gopher|ftp|page)://)|(www|ftp)\.)[-\w0-9\.]+[-\w0-9]+)(:[0-9]*)?(/([-\w0-9_,\$\.\+\!\*\(\):@|&=\?/~\#\%]*[-\w0-9_\$\+\!\*\(\):@|&=\?/~\#\%])?)?', re.IGNORECASE)("url")

            token.setParseAction(self.__convertToUrlLink)
        else:
            token = NoMatch()

        return token

    def __convertToUrlLink(self, s, l, t):
        """
        Преобразовать ссылку на интернет-адрес
        """
        if not re.search('^(?:https?|ftp|news|gopher|telnet|nttp|file|page)://', t[0]):
            return self.__getUrlTag("http://" + t[0], t[0])

        return self.__getUrlTag(t[0], t[0])

    def __getUrlTag(self, url, comment):
        return '<a href="%s">%s</a>' % (url, comment)
