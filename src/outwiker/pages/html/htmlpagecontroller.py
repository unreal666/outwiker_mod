# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController
from outwiker.gui.pagedialogpanels.appearancepanel import (AppearancePanel,
                                                           AppearanceController)

from htmlpage import HtmlWikiPage


class HtmlPageController (BaseController):
    """GUI controller for HTML page"""
    def __init__(self, application):
        super(HtmlPageController, self).__init__()
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy


    def _addTab (self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel (dialog.getPanelsParent())
            dialog.addPanel (self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController (
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController (self._appearanceController)


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == HtmlWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController (self._appearanceController)
            params.dialog.removePanel (self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None


    def __onPageDialogDestroy (self, page, params):
        self._appearancePanel = None
        self._appearanceController = None
