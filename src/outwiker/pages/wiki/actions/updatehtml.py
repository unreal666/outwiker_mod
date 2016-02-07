# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.events import PageUpdateNeededParams


class WikiUpdateHtmlAction (BaseAction):
    """
    Обновить (пересоздать) код HTML
    """
    stringId = u"WikiUpdateHtml"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Update HTML Code")


    @property
    def description (self):
        return _(u"Update HTML code for wiki page")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        self._application.onPageUpdateNeeded (self._application.selectedPage,
                                              PageUpdateNeededParams(None))
