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
    start_html = '<blockquote{var_part}>'
    end_html = '</blockquote>'
    name = 'quote'
    var_part_re = re.compile('^%s' % TagAttrsPattern.value)
    var_part_name = TagAttrsPattern.name
    var_part_pattern = ' %s'
    ignore = LineBreakToken().getToken()
