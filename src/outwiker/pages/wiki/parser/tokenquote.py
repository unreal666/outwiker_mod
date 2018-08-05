# -*- coding: utf-8 -*-

import re

from .tokenblock import SimpleNestedBlock
from .tokenlinebreak import LineBreakToken
from .utils import TagAttrsPattern

class QuoteFactory(object):
    """
    Фабрика для создания токена для цитат
    """
    @staticmethod
    def make(parser):
        return QuoteToken(parser).getToken()


class QuoteToken(SimpleNestedBlock):
    start = '[>'
    end = '<]'
    start_html = '<blockquote{attrs}>'
    end_html = '</blockquote>'
    name = 'quote'
    attrs_re = re.compile('^%s' % TagAttrsPattern.value)
    attrs_name = TagAttrsPattern.name
    ignore = LineBreakToken().getToken()
