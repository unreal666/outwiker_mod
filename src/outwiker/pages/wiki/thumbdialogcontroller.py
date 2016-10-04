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
        filesList = filter (isImage, Attachment (self._page).getAttachRelative())
        filesList.sort (Attachment.sortByName)

        if (self._selectedText.startswith (u"Attach:") and
                self._selectedText[len (u"Attach:"):] in filesList):
            selectedFile = self._selectedText[len (u"Attach:"):]
        else:
            selectedFile = u""

        self._dialog = self._createDialog (self._parent, filesList, selectedFile)
        resultDlg = self._dialog.ShowModal()

        self.result = self.__generateText (self._dialog)

        self._dialog.Destroy()

        return resultDlg


    def _createDialog (self, parent, filesList, selectedFile):
        dialog = ThumbDialog (parent, filesList, selectedFile)

        self.__prevStateSoftMode = dialog.softMode
        dialog.filesListCombo.Bind (wx.EVT_COMBOBOX, handler=self.__onfileSelected)
        dialog.softmodeCheckBox.Bind (wx.EVT_CHECKBOX, handler=self.__onStateChanged)

        return dialog


    def __generateText (self, dialog):
        size = dialog.size
        fname = dialog.fileName
        scaleType = dialog.scaleType
        softMode = dialog.softMode

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

        if len (fname) > 0:
            fileText = u"Attach:{fname}".format (fname=fname)
        else:
            fileText = u""

        if softMode:
            softModeText = u" soft"
        else:
            softModeText = u""

        result = u"%thumb{scale}{softmode}%{fname}%%".format (scale=scaleText, softmode=softModeText, fname=fileText)
        return result


    def __onfileSelected (self, event):
        if self._dialog.fileName.lower().endswith (u".svg"):
            self._dialog.softMode = True
            self._dialog.softmodeCheckBox.Enable(False)
        else:
            self._dialog.softMode = self.__prevStateSoftMode
            self._dialog.softmodeCheckBox.Enable(True)


    def __onStateChanged (self, event):
        self.__prevStateSoftMode = self._dialog.softMode
        # self.__prevStateSoftMode = self._dialog.softMode = not self._dialog.softMode
