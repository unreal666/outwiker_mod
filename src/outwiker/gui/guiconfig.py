#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import locale

import wx

from outwiker.core.config import StringOption, BooleanOption, IntegerOption, ListOption


class GeneralGuiConfig (object):
    """
    Класс для хранения основных настроек
    """
    GENERAL_SECTION = u"General"
    RECENT_SECTION = u"RecentWiki"

    ASK_BEFORE_EXIT_PARAM = u"AskBeforeExit"
    ASK_BEFORE_EXIT_DEFAULT = False

    AUTOSAVE_INTERVAL_PARAM = u"AutosaveInterval"
    AUTOSAVE_INTERVAL_DEFAULT = 3

    RECENT_WIKI_COUNT_PARAM = u"maxcount"
    RECENT_WIKI_COUNT_DEFAULT = 5

    RECENT_AUTOOPEN_PARAM = u"AutoOpen"
    RECENT_AUTOOPEN_DEFAULT = False

    DATETIME_FORMAT_PARAM = u"DateTimeFormat"
    DATETIME_FORMAT_DEFAULT = u"%c"


    def __init__ (self, config):
        self.config = config

        # Спрашивать подтверждение выхода?
        self.askBeforeExit = BooleanOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                GeneralGuiConfig.ASK_BEFORE_EXIT_PARAM, 
                GeneralGuiConfig.ASK_BEFORE_EXIT_DEFAULT)

        # Интервал, через которое происходит автосохранение страницы. Если значение <= 0, значит автосохранение отключено
        self.autosaveInterval = IntegerOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                GeneralGuiConfig.AUTOSAVE_INTERVAL_PARAM, 
                GeneralGuiConfig.AUTOSAVE_INTERVAL_DEFAULT)

        # Количество последних открытых вики
        self.historyLength = IntegerOption (self.config, 
                GeneralGuiConfig.RECENT_SECTION, 
                GeneralGuiConfig.RECENT_WIKI_COUNT_PARAM, 
                GeneralGuiConfig.RECENT_WIKI_COUNT_DEFAULT)

        # Открывать последнуюю открытую вики при старте?
        self.autoopen = BooleanOption (self.config, 
                GeneralGuiConfig.RECENT_SECTION, 
                GeneralGuiConfig.RECENT_AUTOOPEN_PARAM, 
                GeneralGuiConfig.RECENT_AUTOOPEN_DEFAULT)

        # Формат для представления даты и времени модификиции страниц
        self.dateTimeFormat = StringOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                GeneralGuiConfig.DATETIME_FORMAT_PARAM, 
                GeneralGuiConfig.DATETIME_FORMAT_DEFAULT)


class PluginsConfig (object):
    """
    Класс для хранения настроек, связанных с плагинами
    """

    PLUGINS_SECTION = u"Plugins"
    DISABLED_PARAM = u"Disabled"

    def __init__ (self, config):
        self.config = config

        self.disabledPlugins = ListOption (self.config, 
                PluginsConfig.PLUGINS_SECTION,
                PluginsConfig.DISABLED_PARAM,
                [],
                separator=u";")



class TrayConfig (object):
    """
    Класс для хранения настроек, связанных с иконками в трее
    """
    MINIMIZE_TO_TRAY_PARAM = u"MinimizeToTray"
    MINIMIZE_TO_TRAY_DEFAULT = True

    START_ICONIZED_PARAM = u"StartIconized"
    START_ICONIZED_DEFAULT = False

    ALWAYS_SHOW_TRAY_ICON_PARAM = u"AlwaysShowTrayIcon"
    ALWAYS_SHOW_TRAY_ICON_DEFAULT = False

    MINIMIZE_ON_CLOSE_PARAM = u"MinimizeOnClose"
    MINIMIZE_ON_CLOSE_DEFAULT = False


    def __init__ (self, config):
        self.config = config

        # Сворачивать в трей?
        self.minimizeToTray = BooleanOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                TrayConfig.MINIMIZE_TO_TRAY_PARAM, 
                TrayConfig.MINIMIZE_TO_TRAY_DEFAULT)

        # Запускаться свернутым?
        self.startIconized = BooleanOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                TrayConfig.START_ICONIZED_PARAM, 
                TrayConfig.START_ICONIZED_DEFAULT)

        # Всегда показывать иконку в трее?
        self.alwaysShowTrayIcon = BooleanOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                TrayConfig.ALWAYS_SHOW_TRAY_ICON_PARAM, 
                TrayConfig.ALWAYS_SHOW_TRAY_ICON_DEFAULT)

        # Сворачивать окно программы при закрытии главного окна
        self.minimizeOnClose = BooleanOption (self.config,
                GeneralGuiConfig.GENERAL_SECTION,
                TrayConfig.MINIMIZE_ON_CLOSE_PARAM,
                TrayConfig.MINIMIZE_ON_CLOSE_DEFAULT)



class EditorConfig (object):
    """
    Класс для хранения настроек редактора
    """
    FONT_SECTION = u"Font"

    SHOW_LINE_NUMBERS_SECTION = u"ShowLineNumbers"
    SHOW_LINE_NUMBERS_DEFAULT = False

    TAB_WIDTH_SECTION = u"TabWidth"
    TAB_WIDTH_DEFAULT = 4

    FONT_SIZE_SECTION = u"size"
    FONT_SIZE_DEFAULT = 10

    FONT_NAME_SECTION = u"FaceName"
    FONT_NAME_DEFAULT = u""

    FONT_BOLD_SECTION = u"bold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = u"italic"
    FONT_ITALIC_DEFAULT = False

    # Поведение клавиш Home / End. 
    HOME_END_OF_LINE = 0
    HOME_END_OF_PARAGRAPH = 1

    HOME_END_KEYS_SECTION = u"HomeEndKeys"
    HOME_END_KEYS_DEFAULT = HOME_END_OF_LINE


    def __init__ (self, config):
        self.config = config

        # Показывать номера строк в редакторе?
        self.lineNumbers = BooleanOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                EditorConfig.SHOW_LINE_NUMBERS_SECTION, 
                EditorConfig.SHOW_LINE_NUMBERS_DEFAULT)

        # Размер табуляции
        self.tabWidth = IntegerOption (self.config, 
                GeneralGuiConfig.GENERAL_SECTION, 
                EditorConfig.TAB_WIDTH_SECTION, 
                EditorConfig.TAB_WIDTH_DEFAULT)
        
        # Размер шрифта
        self.fontSize = IntegerOption (self.config, 
                EditorConfig.FONT_SECTION, 
                EditorConfig.FONT_SIZE_SECTION, 
                EditorConfig.FONT_SIZE_DEFAULT)

        # Начертание шрифта
        self.fontName = StringOption (self.config, 
                EditorConfig.FONT_SECTION, 
                EditorConfig.FONT_NAME_SECTION, 
                EditorConfig.FONT_NAME_DEFAULT)

        self.fontIsBold = BooleanOption (self.config, 
                EditorConfig.FONT_SECTION, 
                EditorConfig.FONT_BOLD_SECTION, 
                EditorConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption (self.config, 
                EditorConfig.FONT_SECTION, 
                EditorConfig.FONT_ITALIC_SECTION, 
                EditorConfig.FONT_ITALIC_DEFAULT)

        # Поведение клавиш Home / End
        self.homeEndKeys = IntegerOption (self.config,
                GeneralGuiConfig.GENERAL_SECTION,
                EditorConfig.HOME_END_KEYS_SECTION,
                EditorConfig.HOME_END_KEYS_DEFAULT)


class HtmlRenderConfig (object):
    """
    Класс для хранения настроек HTML-рендера
    """
    # Название секции в конфиге для настроек HTML
    HTML_SECTION = u"HTML"

    FONT_FACE_NAME_PARAM = u"FontFaceName"
    FONT_NAME_DEFAULT = u"Verdana"

    FONT_SIZE_PARAM = u"FontSize"
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_PARAM = u"FontBold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_PARAM = u"FontItalic"
    FONT_ITALIC_DEFAULT = False

    USER_STYLE_PARAM = u"UserStyle"
    USER_STYLE_DEFAULT = u""

    def __init__ (self, config):
        self.config = config

        self.fontSize = IntegerOption (self.config, 
                HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.FONT_SIZE_PARAM, 
                HtmlRenderConfig.FONT_SIZE_DEFAULT)

        self.fontName = StringOption (self.config, 
                HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.FONT_FACE_NAME_PARAM, 
                HtmlRenderConfig.FONT_NAME_DEFAULT)

        self.fontIsBold = BooleanOption (self.config, 
                HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.FONT_BOLD_PARAM, 
                HtmlRenderConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption (self.config, 
                HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.FONT_ITALIC_PARAM, 
                HtmlRenderConfig.FONT_ITALIC_DEFAULT)

        self.userStyle = StringOption (self.config, 
                HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.USER_STYLE_PARAM, 
                HtmlRenderConfig.USER_STYLE_DEFAULT)


class TextPrintConfig (object):
    """
    Класс для хранения настроек печати текста
    """
    PRINT_SECTION = u"Print"

    FONT_NAME_SECTION = u"FontFaceName"
    FONT_NAME_DEFAULT = u"Arial"

    FONT_SIZE_SECTION = u"FontSize"
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_SECTION = u"FontBold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = u"FontItalic"
    FONT_ITALIC_DEFAULT = False

    PAPPER_SIZE_SECTION = u"PaperId"
    PAPPER_SIZE_DEFAULT = wx.PAPER_A4

    MARGIN_TOP_SECTION = u"MarginTop"
    MARGIN_TOP_DEFAULT = 20

    MARGIN_BOTTOM_SECTION = u"MarginBottom"
    MARGIN_BOTTOM_DEFAULT = 20

    MARGIN_LEFT_SECTION = u"MarginLeft"
    MARGIN_LEFT_DEFAULT = 20

    MARGIN_RIGHT_SECTION = u"MarginRight"
    MARGIN_RIGHT_DEFAULT = 20

    def __init__ (self, config):
        self.config = config

        # Настройки шрифта
        self.fontName = StringOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.FONT_NAME_SECTION, 
                TextPrintConfig.FONT_NAME_DEFAULT)

        self.fontSize = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.FONT_SIZE_SECTION,
                TextPrintConfig.FONT_SIZE_DEFAULT)

        self.fontIsBold = BooleanOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.FONT_BOLD_SECTION,
                TextPrintConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.FONT_ITALIC_SECTION,
                TextPrintConfig.FONT_ITALIC_DEFAULT)

        self.paperId = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.PAPPER_SIZE_SECTION,
                TextPrintConfig.PAPPER_SIZE_DEFAULT)

        self.marginTop = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.MARGIN_TOP_SECTION,
                TextPrintConfig.MARGIN_TOP_DEFAULT)

        self.marginBottom = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.MARGIN_BOTTOM_SECTION,
                TextPrintConfig.MARGIN_BOTTOM_DEFAULT)

        self.marginLeft = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.MARGIN_LEFT_SECTION,
                TextPrintConfig.MARGIN_LEFT_DEFAULT)
        
        self.marginRight = IntegerOption (self.config, 
                TextPrintConfig.PRINT_SECTION, 
                TextPrintConfig.MARGIN_RIGHT_SECTION,
                TextPrintConfig.MARGIN_RIGHT_DEFAULT)


class MainWindowConfig (object):
    """
    Класс для хранения настроек главного окна
    """
    MAIN_WINDOW_SECTION = u"MainWindow"

    TITLE_FORMAT_SECTION = u"Title"
    TITLE_FORMAT_DEFAULT = u"{page} - {file} - OutWiker"

    WIDTH_SECTION = u"width"
    WIDTH_DEFAULT = 800

    HEIGHT_SECTION = u"height"
    HEIGHT_DEFAULT = 680

    XPOS_SECTION = u"xpos"
    XPOS_DEFAULT = 0

    YPOS_SECTION = u"ypos"
    YPOS_DEFAULT = 0

    FULLSCREEN_SECTION = u"fullscreen"
    FULLSCREEN_DEFAULT = False

    MAXIMIZED_SECTION = u"maximized"
    MAXIMIZED_DEFAULT = False


    def __init__ (self, config):
        self.config = config

        self.titleFormat = StringOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.TITLE_FORMAT_SECTION,
                self.TITLE_FORMAT_DEFAULT)

        self.width = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.WIDTH_SECTION,
                self.WIDTH_DEFAULT)

        self.height = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.HEIGHT_SECTION,
                self.HEIGHT_DEFAULT)

        self.xPos = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.XPOS_SECTION,
                self.XPOS_DEFAULT)

        self.yPos = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.YPOS_SECTION,
                self.YPOS_DEFAULT)

        self.fullscreen = BooleanOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.FULLSCREEN_SECTION,
                self.FULLSCREEN_DEFAULT)

        self.maximized = BooleanOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.MAXIMIZED_SECTION,
                self.MAXIMIZED_DEFAULT)



class TreeConfig (object):
    """
    Класс для хранения настроек панели с деревом
    """
    WIDTH_SECTION = u"TreeWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u"TreeHeight"
    HEIGHT_DEFAULT = 250

    PANE_OPTIONS_SECTION = u"TreePane"
    PANE_OPTIONS_DEFAULT = ""

    def __init__ (self, config):
        self.config = config

        self.width = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                TreeConfig.WIDTH_SECTION,
                TreeConfig.WIDTH_DEFAULT)

        self.height = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                TreeConfig.HEIGHT_SECTION,
                TreeConfig.HEIGHT_DEFAULT)

        # Параметры панели с деревом
        self.pane = StringOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                TreeConfig.PANE_OPTIONS_SECTION,
                TreeConfig.PANE_OPTIONS_DEFAULT)



class AttachConfig (object):
    """
    Класс для хранения настроек панели с вложенными файлами
    """
    WIDTH_SECTION = u"AttachesWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u"AttachesHeight"
    HEIGHT_DEFAULT = 150

    PANE_OPTIONS_SECTION = u"AttachesPane"
    PANE_OPTIONS_DEFAULT = u""

    def __init__ (self, config):
        self.config = config

        self.width = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.WIDTH_SECTION,
                self.WIDTH_DEFAULT)

        self.height = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.HEIGHT_SECTION,
                self.HEIGHT_DEFAULT)

        self.pane = StringOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.PANE_OPTIONS_SECTION,
                self.PANE_OPTIONS_DEFAULT)



class TagsCloudConfig (object):
    """
    Класс для хранения настроек панели с облагом тегов
    """
    WIDTH_SECTION = u"TagsCloudWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u"TagsCloudHeight"
    HEIGHT_DEFAULT = 170

    PANE_OPTIONS_SECTION = u"TagsCloudPane"
    PANE_OPTIONS_DEFAULT = ""

    def __init__ (self, config):
        self.config = config

        self.width = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.WIDTH_SECTION,
                self.WIDTH_DEFAULT)

        self.height = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.HEIGHT_SECTION,
                self.HEIGHT_DEFAULT)

        # Параметры панели с деревом
        self.pane = StringOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.PANE_OPTIONS_SECTION,
                self.PANE_OPTIONS_DEFAULT)


class PageDialogConfig (object):
    WIDTH_SECTION = u"PageDialogWidth"
    WIDTH_DEFAULT = 500

    HEIGHT_SECTION = u"PageDialogHeight"
    HEIGHT_DEFAULT = 350

    def __init__ (self, config):
        self.config = config

        self.width = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.WIDTH_SECTION,
                self.WIDTH_DEFAULT)

        self.height = IntegerOption (self.config, 
                MainWindowConfig.MAIN_WINDOW_SECTION, 
                self.HEIGHT_SECTION,
                self.HEIGHT_DEFAULT)

