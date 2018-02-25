# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex

from outwiker.core.thumbexception import ThumbException
from outwiker.core.defines import PAGE_ATTACH_DIR
from .pagethumbmaker import PageThumbmaker
from outwiker.core.attachment import Attachment
from ..wikiconfig import WikiConfig


class ThumbnailFactory (object):
    """
    Класс для создания токена ThumbnailToken
    """
    @staticmethod
    def make (parser):
        return ThumbnailToken(parser).getToken()


class ThumbnailToken (object):
    """
    Класс, содержащий все необходимое для разбора и создания превьюшек картинок на вики-странице
    """
    def __init__ (self, parser):
        self.parser = parser
        self.thumbmaker = PageThumbmaker()


    def getToken (self):
        result = Regex (r"""%\s*?
                        (?:
                            (?:thumb\s+)?
                            (?:width\s*?=\s*?(?P<width>\d+)
                            |height\s*?=\s*?(?P<height>\d+)
                            |maxsize\s*?=\s*?(?P<maxsize>\d+))\s*?
                            (?:px)?
                            |thumb\s*?
                        )
                        (?:\s+?(?P<mode>soft))?
                        \s*?
                        %\s*?
                        Attach:(?P<fname>.*?\.(?:jpe?g|bmp|gif|tiff?|png|svg))\s*?%%""",
                        re.IGNORECASE | re.VERBOSE)
        result = result.setParseAction (self.__convertThumb)("thumbnail")
        return result


    def __convertThumb (self, s, l, t):
        if t["mode"] == u"soft":
            template = u'<a href="{0}/{1}"><img src="{0}/{1}" style="{2}:{3}px"/></a>'
            template2 = u'<a href="{0}/{1}"><img src="{0}/{1}" style="max-width:{2}px;max-height:{2}px"/></a>'

        fname = t["fname"]

        if t["width"] is not None:
            size = int (t["width"])

            if t["mode"] == u"soft":
                return template.format (Attachment.attachDir, fname, u"width", size)

            func = self.thumbmaker.createThumbByWidth

        elif t["height"] is not None:
            size = int (t["height"])

            if t["mode"] == u"soft":
                return template.format (Attachment.attachDir, fname, u"height", size)

            func = self.thumbmaker.createThumbByHeight

        elif t["maxsize"] is not None:
            size = int (t["maxsize"])

            if t["mode"] == u"soft":
                return template2.format (Attachment.attachDir, fname, size)

            func = self.thumbmaker.createThumbByMaxSize

        else:
            config = WikiConfig (self.parser.config)
            size = config.thumbSizeOptions.value

            if t["mode"] == u"soft":
                return template2.format (Attachment.attachDir, fname, size)

            func = self.thumbmaker.createThumbByMaxSize

        try:
            thumb = func (self.parser.page, fname, size)

        except (ThumbException, IOError):
            return _(u"<b>Can't create thumbnail for \"{}\"</b>").format (fname)

        return u'<a href="%s/%s"><img src="%s"/></a>' % (PAGE_ATTACH_DIR, fname, thumb.replace ("\\", "/"))
