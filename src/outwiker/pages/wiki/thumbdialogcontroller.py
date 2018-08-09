# -*- coding: utf-8 -*-

from outwiker.core.attachment import Attachment

import wx

from .thumbdialog import ThumbDialog
from .parser.utils import isImage


class ThumbDialogController (object):
    def __init__ (self, parent, page, selectedText):
        """
        parent - родительское окно
        page - текущая страница (не может быть равна None)
        selectedText - текст, выбанный в редакторе
        """
        assert page is not None

        self._parent = parent
        self._page = page
        self._selectedText = selectedText.strip()

        # Строка, полученная из параметров, выбанных в диалоге
        self.result = u""


    def showDialog (self):
        filesList = list(filter (isImage, Attachment (self._page).getAttachRelative()))
        filesList.sort (key=lambda a: a.lower())

        if (self._selectedText.startswith (u"Attach:") and
                self._selectedText[len (u"Attach:"):] in filesList):
            selectedFile = self._selectedText[len (u"Attach:"):]
        else:
            selectedFile = u""

        self._dialog = self._createDialog (self._parent, filesList, selectedFile)
        self.__onStateChanged()
        resultDlg = self._dialog.ShowModal()

        self.result = self.__generateText (self._dialog)

        self._dialog.Destroy()

        return resultDlg


    def _createDialog (self, parent, filesList, selectedFile):
        dialog = ThumbDialog (parent, filesList, selectedFile)

        dialog.filesListCombo.Bind (wx.EVT_COMBOBOX, handler=self.__onfileSelected)
        dialog.softmodeCheckBox.Bind (wx.EVT_CHECKBOX, handler=self.__onStateChanged)

        return dialog


    def __generateText (self, dialog):
        size = dialog.size
        fname = dialog.fileName
        scaleType = dialog.scaleType
        softMode = dialog.softMode
        unit = dialog.unit
        nolink = dialog.nolink

        if size == 0:
            scaleText = u""
        elif scaleType == ThumbDialog.WIDTH:
            scaleText = u" width={size}".format (size = size)
        elif scaleType == ThumbDialog.HEIGHT:
            scaleText = u" height={size}".format (size = size)
        elif scaleType == ThumbDialog.MAX_SIZE:
            scaleText = u" maxsize={size}".format (size = size)
        else:
            raise NotImplementedError

        fileText = u"Attach:{fname}".format (fname=fname) if len (fname) > 0 else u""
        softModeText = u" soft" if softMode else u""
        nolinkText = u" nolink" if nolink else u""
        unitText = u"%s" % ThumbDialog.UNIT_ITEMS[unit] if softMode and unit else u""

        result = u"%thumb{scale}{unit}{softmode}{nolink}%{fname}%%".format (
                    scale=scaleText,
                    softmode=softModeText,
                    fname=fileText,
                    unit=unitText,
                    nolink=nolinkText)
        return result


    def __onfileSelected (self, event):
        if self._dialog.fileName.lower().endswith (u".svg"):
            self.__prevStateSoftMode = self._dialog.softMode
            self._dialog.softMode = True
            self._dialog.softmodeCheckBox.Enable(False)
        else:
            self._dialog.softMode = self.__prevStateSoftMode
            self._dialog.softmodeCheckBox.Enable(True)

        self.__changeStateUnit()


    def __onStateChanged (self, event=None):
        self.__prevStateSoftMode = self._dialog.softMode
        # self.__prevStateSoftMode = self._dialog.softMode = not self._dialog.softMode
        self.__changeStateUnit()


    def __changeStateUnit (self):
        if self._dialog.softMode:
            self._dialog.unitCombo.Enable(True)
        else:
            self._dialog.unitCombo.Enable(False)
