# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex

from outwiker.core.thumbexception import ThumbException
from outwiker.core.defines import PAGE_ATTACH_DIR
from .pagethumbmaker import PageThumbmaker
from ..wikiconfig import WikiConfig


class ThumbnailFactory(object):
    """
    Класс для создания токена ThumbnailToken
    """
    @staticmethod
    def make(parser):
        return ThumbnailToken(parser).getToken()


class ThumbnailToken(object):
    """
    Класс, содержащий все необходимое для разбора и создания превьюшек картинок на вики-странице
    """
    def __init__(self, parser):
        self.parser = parser
        self.thumbmaker = PageThumbmaker()

    def getToken(self):
        result = Regex(r"""%\s*?
                           (?:
                             (?:thumb\s+)?
                             (?:width\s*?=\s*?(?P<width>\d+(?:\.\d+)?)
                               (?P<unit2>px|in|[cm]m|p[tc]|e[mx]|ch|rem|v[wh]|vmin|vmax|%)?
                               (
                                 \s+height\s*?=\s*?(?P<height2>\d+(?:\.\d+)?)
                               )?
                             |height\s*?=\s*?(?P<height>\d+(?:\.\d+)?)
                             |maxsize\s*?=\s*?(?P<maxsize>\d+(?:\.\d+)?))\s*?
                             (?P<unit>px|in|[cm]m|p[tc]|e[mx]|ch|rem|v[wh]|vmin|vmax|%)?
                             |thumb\s*?
                           )
                           (?P<soft>\s+?soft)?
                           (?P<nolink>\s+?nolink)?
                           \s*?
                           %\s*?
                           Attach:(?P<fname>.*?\.(?:jpe?g|bmp|gif|tiff?|png|svg))\s*?%%""",
                           re.IGNORECASE | re.VERBOSE)
        result = result.setParseAction(self.__convertThumb)("thumbnail")
        return result

    def __convertThumb(self, s, l, t):
        if t["soft"]:
            unit = t["unit"] or 'px'
            if not t["nolink"]:
                template = '<a href="{0}/{1}"><img src="{0}/{1}" style="{4}:{2}{3}"/></a>'
                template2 = '<a href="{0}/{1}"><img src="{0}/{1}" style="max-width:{2}{3};max-height:{2}{3}"/></a>'
                template3 = '<a href="{0}/{1}"><img src="{0}/{1}" style="width:{2}{3};height:{4}{5}"/></a>'
            else:
                template = '<img src="{0}/{1}" style="{4}:{2}{3}"/>'
                template2 = '<img src="{0}/{1}" style="max-width:{2}{3};max-height:{2}{3}"/>'
        else:
            template = '<img src="{0}"/>' if t["nolink"] else '<a href="{1}/{2}"><img src="{0}"/></a>'

        fname = t["fname"]

        if t["width"] is not None:
            size = self.__convertSize(t["width"])

            if t["soft"]:

                if t["height2"] is not None:
                    height = self.__convertSize(t["height2"])
                    unit2 = t["unit2"] or 'px'

                    return template3.format(PAGE_ATTACH_DIR, fname, size, unit2, height, unit)

                return template.format(PAGE_ATTACH_DIR, fname, size, unit, "width")

            func = self.thumbmaker.createThumbByWidth

        elif t["height"] is not None:
            size = self.__convertSize(t["height"])

            if t["soft"]:
                return template.format(PAGE_ATTACH_DIR, fname, size, unit, "height")

            func = self.thumbmaker.createThumbByHeight

        else:
            if t["maxsize"] is not None:
                size = self.__convertSize(t["maxsize"])
            else:
                config = WikiConfig(self.parser.config)
                size = config.thumbSizeOptions.value

            if t["soft"]:
                return template2.format(PAGE_ATTACH_DIR, fname, size, unit)

            func = self.thumbmaker.createThumbByMaxSize

        try:
            thumb = func(self.parser.page, fname, size)

        except (ThumbException, IOError):
            return _("<b>Can't create thumbnail for \"{}\"</b>").format(fname)

        return template.format(thumb.replace("\\", "/"), PAGE_ATTACH_DIR, fname)

    def __convertSize(self, text):
        float_value = float(text)
        int_value = int(float_value)

        return int_value if float_value == int_value else float_value
