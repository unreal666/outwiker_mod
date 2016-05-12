# -*- coding: utf-8 -*-

import os

import wx

from outwiker.core.commands import MessageBox, insertCurrentDate
from outwiker.core.application import Application
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style
from outwiker.core.system import readTextFile
from outwiker.core.events import (PreprocessingParams,
                                  PreHtmlImprovingParams,
                                  PostprocessingParams
                                  )

from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog

from outwiker.pages.html.htmltoolbar import HtmlToolBar
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel, EVT_PAGE_TAB_CHANGED
from outwiker.pages.html.tabledialogcontroller import (
    TableDialogController,
    TableRowsDialogController
)

from actions.autolinewrap import HtmlAutoLineWrap
from actions.link import insertLink
from actions.switchcoderesult import SwitchCodeResultAction
from outwiker.actions.polyactionsid import *



class HtmlPageView (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (HtmlPageView, self).__init__ (parent, *args, **kwds)
        self._application = Application

        self.__HTML_MENU_INDEX = 7
        self._htmlPanelName = "html"
        self._menuName = _(u"HTML")

        self.mainWindow.toolbars[self._htmlPanelName] = HtmlToolBar(self.mainWindow,
                                                                    self.mainWindow.auiManager)

        # Список используемых полиморфных действий
        self.__polyActions = [
            BOLD_STR_ID,
            ITALIC_STR_ID,
            BOLD_ITALIC_STR_ID,
            UNDERLINE_STR_ID,
            STRIKE_STR_ID,
            SUBSCRIPT_STR_ID,
            SUPERSCRIPT_STR_ID,
            ALIGN_LEFT_STR_ID,
            ALIGN_CENTER_STR_ID,
            ALIGN_RIGHT_STR_ID,
            ALIGN_JUSTIFY_STR_ID,
            HEADING_1_STR_ID,
            HEADING_2_STR_ID,
            HEADING_3_STR_ID,
            HEADING_4_STR_ID,
            HEADING_5_STR_ID,
            HEADING_6_STR_ID,
            PREFORMAT_STR_ID,
            CODE_STR_ID,
            ANCHOR_STR_ID,
            HORLINE_STR_ID,
            LINK_STR_ID,
            LIST_BULLETS_STR_ID,
            LIST_NUMBERS_STR_ID,
            LIST_DEFINITIONS_STR_ID,
            LINE_BREAK_STR_ID,
            HTML_ESCAPE_STR_ID,
            TABLE_STR_ID,
            TABLE_ROW_STR_ID,
            TABLE_CELL_STR_ID,
            QUOTE_STR_ID,
            IMAGE_STR_ID,
            CURRENT_DATE,
            MARK_STR_ID,
        ]

        # Список действий, которые нужно удалять с панелей и из меню.
        # А еще их надо дизаблить при переходе на вкладку просмотра результата
        # Не убираю пустой список, поскольку в будущем могут появиться нестандартные
        # действия, специфические только для HTML-страниц
        self.__htmlNotationActions = [
        ]

        self.__createCustomTools()
        self.mainWindow.UpdateAuiManager()

        self._application.onPageUpdate += self.__onPageUpdate

        self.Bind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)


    def getTextEditor(self):
        return HtmlTextEditor


    @property
    def toolsMenu (self):
        return self.__htmlMenu


    def onTabChanged (self, event):
        if self._currentpage is not None:
            if event.tab == self.RESULT_PAGE_INDEX:
                self._onSwitchToPreview()
            else:
                self._onSwitchToCode()

            self.savePageTab(self._currentpage)

        event.Skip()


    def Clear (self):
        self._application.onPageUpdate -= self.__onPageUpdate
        self.Unbind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

        self._removeActionTools()

        if self._htmlPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.updatePanesInfo()
            self.mainWindow.toolbars.destroyToolBar (self._htmlPanelName)

        super (HtmlPageView, self).Clear()


    def _removeActionTools (self):
        actionController = self._application.actionController

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId),
             self.__htmlNotationActions)

        # Удалим элементы меню полиморфных действий
        map (lambda strid: actionController.removeMenuItem (strid),
             self.__polyActions)

        self._application.actionController.removeMenuItem (HtmlAutoLineWrap.stringId)
        self._application.actionController.removeMenuItem (SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        if self._htmlPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId),
                 self.__htmlNotationActions)

            map (lambda strid: actionController.removeToolbarButton (strid),
                 self.__polyActions)

            self._application.actionController.removeToolbarButton (HtmlAutoLineWrap.stringId)
            self._application.actionController.removeToolbarButton (SwitchCodeResultAction.stringId)

        # Обнулим функции действия в полиморфных действиях
        map (lambda strid: actionController.getAction (strid).setFunc (None),
             self.__polyActions)


    def _enableActions (self, enabled):
        actionController = self._application.actionController

        map (lambda action: actionController.enableTools (action.stringId, enabled),
             self.__htmlNotationActions)

        # Активируем / дизактивируем полиморфные действия
        map (lambda strid: actionController.enableTools (strid, enabled),
             self.__polyActions)


    def __onPageUpdate (self, sender, **kwargs):
        if sender == self._currentpage:
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self._updateResult()


    def UpdateView (self, page):
        self.__updateLineWrapTools()
        BaseHtmlPanel.UpdateView (self, page)


    def __createLineWrapTools (self):
        """
        Create button and menu item to enable / disable lines wrap.
        """
        image = os.path.join (self.imagesDir, "linewrap.png")
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]

        self._application.actionController.appendMenuCheckItem (HtmlAutoLineWrap.stringId, self.__htmlMenu)
        self._application.actionController.appendToolbarCheckButton (HtmlAutoLineWrap.stringId,
                                                                     toolbar,
                                                                     image,
                                                                     fullUpdate=False)

        self.__updateLineWrapTools()


    def __updateLineWrapTools (self):
        if self._currentpage is not None:
            self._application.actionController.check (HtmlAutoLineWrap.stringId,
                                                      self._currentpage.autoLineWrap)


    def __createCustomTools (self):
        """
        Создать кнопки и меню для данного типа страниц
        """
        assert self.mainWindow is not None

        self.__htmlMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__tableMenu = wx.Menu()

        self.__createLineWrapTools ()
        self.toolsMenu.AppendSeparator()

        self.__htmlMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__htmlMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__htmlMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__htmlMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__htmlMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__htmlMenu.AppendSubMenu (self.__tableMenu, _(u"Tables"))

        self.__addFontTools()
        self._addSeparator()

        self.__addAlignTools()
        self._addSeparator()

        self.__addHTools()
        self._addSeparator()

        self.__addTableTools()
        self._addSeparator()

        self.__addListTools()
        self._addSeparator()

        self.__addFormatTools()
        self._addSeparator()

        self.__addOtherTools()
        self._addRenderTools()

        self.mainWindow.mainMenu.Insert (self.__HTML_MENU_INDEX,
                                         self.__htmlMenu,
                                         self._menuName)


    def _addRenderTools (self):
        self._application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        self._application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId,
                                                                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                                                                os.path.join (self.imagesDir, "render.png"),
                                                                fullUpdate=False)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__fontMenu

        # Полужирный шрифт
        self._application.actionController.getAction (BOLD_STR_ID).setFunc (lambda param: self.turnText (u"<b>", u"</b>"))

        self._application.actionController.appendMenuItem (BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold.png"),
                                                                fullUpdate=False)


        # Курсивный шрифт
        self._application.actionController.getAction (ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"<i>", u"</i>"))

        self._application.actionController.appendMenuItem (ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_italic.png"),
                                                                fullUpdate=False)

        # Полужирный курсивный шрифт
        self._application.actionController.getAction (BOLD_ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"<b><i>", u"</i></b>"))

        self._application.actionController.appendMenuItem (BOLD_ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold_italic.png"),
                                                                fullUpdate=False)


        # Подчеркнутый шрифт
        self._application.actionController.getAction (UNDERLINE_STR_ID).setFunc (lambda param: self.turnText (u"<u>", u"</u>"))

        self._application.actionController.appendMenuItem (UNDERLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (UNDERLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_underline.png"),
                                                                fullUpdate=False)


        # Зачеркнутый шрифт
        self._application.actionController.getAction (STRIKE_STR_ID).setFunc (lambda param: self.turnText (u"<strike>", u"</strike>"))

        self._application.actionController.appendMenuItem (STRIKE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (STRIKE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_strikethrough.png"),
                                                                fullUpdate=False)


        # Нижний индекс
        self._application.actionController.getAction (SUBSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"<sub>", u"</sub>"))

        self._application.actionController.appendMenuItem (SUBSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUBSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_subscript.png"),
                                                                fullUpdate=False)


        # Верхний индекс
        self._application.actionController.getAction (SUPERSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"<sup>", u"</sup>"))

        self._application.actionController.appendMenuItem (SUPERSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUPERSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_superscript.png"),
                                                                fullUpdate=False)



    def __addAlignTools (self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__alignMenu

        # Выравнивание по левому краю
        self._application.actionController.getAction (ALIGN_LEFT_STR_ID).setFunc (lambda param: self.turnText (u'<div align="left">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_LEFT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_LEFT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_left.png"),
                                                                fullUpdate=False)


        # Выравнивание по центру
        self._application.actionController.getAction (ALIGN_CENTER_STR_ID).setFunc (lambda param: self.turnText (u'<div align="center">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_CENTER_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_CENTER_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_center.png"),
                                                                fullUpdate=False)


        # Выравнивание по правому краю
        self._application.actionController.getAction (ALIGN_RIGHT_STR_ID).setFunc (lambda param: self.turnText (u'<div align="right">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_RIGHT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_RIGHT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_right.png"),
                                                                fullUpdate=False)


        # Выравнивание по ширине
        self._application.actionController.getAction (ALIGN_JUSTIFY_STR_ID).setFunc (lambda param: self.turnText (u'<div align="justify">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_JUSTIFY_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_JUSTIFY_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_justify.png"),
                                                                fullUpdate=False)



    def __addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__tableMenu

        # Вставить таблицу
        self._application.actionController.getAction (TABLE_STR_ID).setFunc (
            self._insertTable
        )

        self._application.actionController.appendMenuItem (TABLE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table.png"),
                                                                fullUpdate=False)


        # Вставить строку таблицы
        self._application.actionController.getAction (TABLE_ROW_STR_ID).setFunc (
            self._insertTableRows
        )

        self._application.actionController.appendMenuItem (TABLE_ROW_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_ROW_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table_insert_row.png"),
                                                                fullUpdate=False)


        # Вставить ячейку таблицы
        self._application.actionController.getAction (TABLE_CELL_STR_ID).setFunc (lambda param: self.turnText (u'<td>', u'</td>'))

        self._application.actionController.appendMenuItem (TABLE_CELL_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_CELL_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table_insert_cell.png"),
                                                                fullUpdate=False)



    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__listMenu

        # Ненумерованный список
        self._application.actionController.getAction (LIST_BULLETS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'))

        self._application.actionController.appendMenuItem (LIST_BULLETS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_BULLETS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_bullets.png"),
                                                                fullUpdate=False)

        # Нумерованный список
        self._application.actionController.getAction (LIST_NUMBERS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'))

        self._application.actionController.appendMenuItem (LIST_NUMBERS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_NUMBERS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_numbers.png"),
                                                                fullUpdate=False)


        # Список определений
        self._application.actionController.getAction (LIST_DEFINITIONS_STR_ID).setFunc (lambda param: self._turnDefinitionList())

        self._application.actionController.appendMenuItem (LIST_DEFINITIONS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_DEFINITIONS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_definition.png"),
                                                                fullUpdate=False)



    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__headingMenu

        self._application.actionController.getAction (HEADING_1_STR_ID).setFunc (lambda param: self.turnText (u"<h1>", u"</h1>"))
        self._application.actionController.getAction (HEADING_2_STR_ID).setFunc (lambda param: self.turnText (u"<h2>", u"</h2>"))
        self._application.actionController.getAction (HEADING_3_STR_ID).setFunc (lambda param: self.turnText (u"<h3>", u"</h3>"))
        self._application.actionController.getAction (HEADING_4_STR_ID).setFunc (lambda param: self.turnText (u"<h4>", u"</h4>"))
        self._application.actionController.getAction (HEADING_5_STR_ID).setFunc (lambda param: self.turnText (u"<h5>", u"</h5>"))
        self._application.actionController.getAction (HEADING_6_STR_ID).setFunc (lambda param: self.turnText (u"<h6>", u"</h6>"))

        self._application.actionController.appendMenuItem (HEADING_1_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_1_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_1.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_2_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_2_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_2.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_3_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_3_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_3.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_4_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_4_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_4.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_5_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_5_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_5.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_6_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_6_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_6.png"),
                                                                fullUpdate=False)


    def __addFormatTools (self):
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__formatMenu

        # Preformat
        self._application.actionController.getAction (PREFORMAT_STR_ID).setFunc (lambda param: self.turnText (u"<pre>", u"</pre>"))
        self._application.actionController.appendMenuItem (PREFORMAT_STR_ID, menu)

        # Цитирование
        self._application.actionController.getAction (QUOTE_STR_ID).setFunc (lambda param: self.turnText (u"<blockquote>", u"</blockquote>"))

        self._application.actionController.appendMenuItem (QUOTE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (QUOTE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "quote.png"),
                                                                fullUpdate=False)


        # Mark
        self._application.actionController.getAction (MARK_STR_ID).setFunc (lambda param: self.turnText (u"<mark>", u"</mark>"))

        self._application.actionController.appendMenuItem (MARK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (MARK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "mark.png"),
                                                                fullUpdate=False)

        # Код
        self._application.actionController.getAction (CODE_STR_ID).setFunc (lambda param: self.turnText (u'<code>', u'</code>'))

        self._application.actionController.appendMenuItem (CODE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (CODE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "code.png"),
                                                                fullUpdate=False)


    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__htmlMenu

        # Вставить картинку
        self._application.actionController.getAction (IMAGE_STR_ID).setFunc (lambda param: self.turnText (u'<img src="', u'"/>'))

        self._application.actionController.appendMenuItem (IMAGE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (IMAGE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "image.png"),
                                                                fullUpdate=False)


        # Вставить ссылку
        self._application.actionController.getAction (LINK_STR_ID).setFunc (lambda param: insertLink (self._application))

        self._application.actionController.appendMenuItem (LINK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "link.png"),
                                                                fullUpdate=False)


        # Вставить якорь
        self._application.actionController.getAction (ANCHOR_STR_ID).setFunc (lambda param: self.turnText (u'<a name="', u'"></a>'))

        self._application.actionController.appendMenuItem (ANCHOR_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ANCHOR_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "anchor.png"),
                                                                fullUpdate=False)


        # Вставить горизонтальную линию
        self._application.actionController.getAction (HORLINE_STR_ID).setFunc (lambda param: self.replaceText (u"<hr>"))

        self._application.actionController.appendMenuItem (HORLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HORLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                                                                fullUpdate=False)


        # Вставка разрыва страницы
        self._application.actionController.getAction (LINE_BREAK_STR_ID).setFunc (lambda param: self.replaceText (u"<br>\n"))

        self._application.actionController.appendMenuItem (LINE_BREAK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINE_BREAK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "linebreak.png"),
                                                                fullUpdate=False)

        # Текущая дата
        self._application.actionController.getAction (CURRENT_DATE).setFunc (lambda param: insertCurrentDate (self.mainWindow,
                                                                                                              self.codeEditor))

        self._application.actionController.appendMenuItem (CURRENT_DATE, menu)
        self._application.actionController.appendToolbarButton (CURRENT_DATE,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "date.png"),
                                                                fullUpdate=False)


        self.__htmlMenu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        self._application.actionController.getAction (HTML_ESCAPE_STR_ID).setFunc (lambda param: self.escapeHtml ())
        self._application.actionController.appendMenuItem (HTML_ESCAPE_STR_ID, menu)


    def _addSeparator (self):
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        toolbar.AddSeparator()


    def generateHtml (self, page):
        path = self.getHtmlPath ()

        if page.readonly and os.path.exists (path):
            # Если страница открыта только для чтения и html-файл уже существует, то покажем его
            return readTextFile (path)

        style = Style()
        stylepath = style.getPageStyle (page)

        try:
            tpl = HtmlTemplate (readTextFile (stylepath))
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)

            tpl = HtmlTemplate (readTextFile (style.getDefaultStyle()))

        content = self._changeContentByEvent (self.page,
                                              PreprocessingParams (page.content),
                                              Application.onPreprocessing)

        if page.autoLineWrap:
            content = self._changeContentByEvent (self.page,
                                                  PreHtmlImprovingParams (content),
                                                  Application.onPreHtmlImproving)

            config = HtmlRenderConfig (Application.config)
            improverFactory = HtmlImproverFactory (Application)
            text = improverFactory[config.HTMLImprover.value].run (content)
        else:
            text = content

        userhead = u"<title>{}</title>".format (page.title)
        result = tpl.substitute (content = text,
                                 userhead = userhead)

        result = self._changeContentByEvent (self.page,
                                             PostprocessingParams (result),
                                             Application.onPostprocessing)
        return result


    def removeGui (self):
        super (HtmlPageView, self).removeGui ()
        mainMenu = self._application.mainWindow.mainMenu
        index = mainMenu.FindMenu (self._menuName)
        assert index != wx.NOT_FOUND

        mainMenu.Remove (index)


    def _turnDefinitionList (self):
        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        lefttext = u"<dl>\n<dt> "
        righttext = u"</dt>\n<dd></dd>\n</dl>"
        selectedText = editor.GetSelectedText()

        if len (selectedText) is 0:
            selectedText = u"term"

        newtext = lefttext + selectedText + righttext
        editor.replaceText (newtext)

        currPos = editor.GetSelectionEnd()
        newpos = currPos - 10
        editor.SetSelection (newpos, newpos)


    def _changeContentByEvent (self, page, params, event):
        event (page, params)
        return params.result


    def _insertTable (self, param):
        editor = self.codeEditor
        parent = Application.mainWindow

        with TableDialog (parent) as dlg:
            controller = TableDialogController (dlg, Application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText (result)


    def _insertTableRows (self, param):
        editor = self.codeEditor
        parent = Application.mainWindow

        with TableRowsDialog (parent) as dlg:
            controller = TableRowsDialogController (dlg, Application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText (result)
