# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction

from .i18n import get_
from . import defines


class BaseHeadAction(BaseAction):
    """
    Базовый класс действий для вставки команд
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    def _getEditor(self):
        """
        Возвращает указатель на редактор
        """
        return self._application.mainWindow.pagePanel.pageView.codeEditor


class TitleAction(BaseHeadAction):
    """
    Вставить команду (:title:)
    """
    stringId = '%sInsertTitle' % defines.PREFIX_ID

    @property
    def title(self):
        return _('Title (:title ...:)')

    @property
    def description(self):
        return _(defines.ACTION_DESCRIPTION) % 'title'

    def run(self, params):
        self._getEditor().turnText('(:title ', ':)')


class DescriptionAction(BaseHeadAction):
    """
    Вставить команду (:description:)
    """
    stringId = '%sInsertDescription' % defines.PREFIX_ID

    @property
    def title(self):
        return _('Description (:description ...:)')

    @property
    def description(self):
        return _(defines.ACTION_DESCRIPTION) % 'description'

    def run(self, params):
        self._getEditor().turnText('(:description ', ':)')


class KeywordsAction(BaseHeadAction):
    """
    Вставить команду (:keywords:)
    """
    stringId = '%sInsertKeywords' % defines.PREFIX_ID

    @property
    def title(self):
        return _('Keywords (:keywords ...:)')

    @property
    def description(self):
        return _(defines.ACTION_DESCRIPTION) % 'keywords'

    def run(self, params):
        self._getEditor().turnText('(:keywords ', ':)')


class CustomHeadsAction(BaseHeadAction):
    """
    Вставить команду (:htmlhead:)
    """
    stringId = '%sInsertHtmlHead' % defines.PREFIX_ID

    @property
    def title(self):
        return _('Custom head (:htmlhead:)')

    @property
    def description(self):
        return _(defines.ACTION_DESCRIPTION) % 'htmlhead'

    def run (self, params):
        self._getEditor().turnText('(:htmlhead:)\n', '\n(:htmlheadend:)')


class HtmlAttrsAction(BaseHeadAction):
    """
    Вставить команду (:htmlattrs:)
    """
    stringId = '%sInsertHtmlAttrs' % defines.PREFIX_ID


    @property
    def title (self):
        return _('<html> tag attributes (:htmlattrs ...:)')


    @property
    def description (self):
        return _(defines.ACTION_DESCRIPTION) % 'htmlattrs'


    def run (self, params):
        self._getEditor().turnText('(:htmlattrs ', ':)')
