# -*- coding: utf-8 -*-

from outwiker.core.attachment import Attachment

import wx

from .thumbdialog import ThumbDialog
from .parser.utils import isImage


class ThumbDialogController (object):
    def __init__(self, parent, page, selectedText):
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
        self.result = ""

    def showDialog(self):
        filesList = [*
            filter(isImage, Attachment(self._page).getAttachRelative())]
        filesList.sort(key=lambda a: a.lower())

        if (self._selectedText.startswith("Attach:") and
                self._selectedText[len("Attach:"):] in filesList):
            selectedFile = self._selectedText[len("Attach:"):]
        else:
            selectedFile = ""

        dlg = self._dialog = self._createDialog(self._parent, filesList, selectedFile)
        self.__onStateChanged()
        resultDlg = dlg.ShowModal()

        self.result = self.__generateText(dlg)

        dlg.Destroy()

        return resultDlg

    def _createDialog(self, parent, filesList, selectedFile):
        dialog = ThumbDialog(parent, filesList, selectedFile)

        dialog.filesListCombo.Bind(wx.EVT_COMBOBOX, handler=self.__onfileSelected)
        dialog.softmodeCheckBox.Bind(wx.EVT_CHECKBOX, handler=self.__onStateChanged)

        return dialog

    def __generateText(self, dialog):
        size = dialog.size
        fname = dialog.fileName
        scaleType = dialog.scaleType
        softMode = dialog.softMode
        unit = dialog.unit
        nolink = dialog.nolink

        if size == 0:
            scaleText = ""
        elif scaleType == ThumbDialog.WIDTH:
            scaleText = " width={size}".format(size=size)
        elif scaleType == ThumbDialog.HEIGHT:
            scaleText = " height={size}".format(size=size)
        elif scaleType == ThumbDialog.MAX_SIZE:
            scaleText = " maxsize={size}".format(size=size)
        else:
            raise NotImplementedError

        fileText = "Attach:{fname}".format(fname=fname) if len(fname) > 0 else ""
        softModeText = " soft" if softMode else ""
        nolinkText = " nolink" if nolink else ""
        unitText = "%s" % ThumbDialog.UNIT_ITEMS[unit] if softMode and unit > 0 else ""

        result = "%thumb{scale}{unit}{softmode}{nolink}%{fname}%%".format(
                    scale=scaleText,
                    softmode=softModeText,
                    fname=fileText,
                    unit=unitText,
                    nolink=nolinkText)

        return result

    def __onfileSelected(self, event):
        dlg = self._dialog

        if dlgfileName.lower().endswith(".svg"):
            self.__prevStateSoftMode = dlg.softMode
            dlg.softMode = True
            dlg.softmodeCheckBox.Enable(False)
        else:
            dlg.softMode = self.__prevStateSoftMode
            dlg.softmodeCheckBox.Enable(True)

        self.__changeStateUnit()

    def __onStateChanged(self, event=None):
        dlg = self._dialog

        self.__prevStateSoftMode = dlg.softMode
        # self.__prevStateSoftMode = dlg.softMode = not dlg.softMode
        self.__changeStateUnit()

    def __changeStateUnit(self):
        dlg = self._dialog

        if dlg.softMode:
            dlg.unitCombo.Enable(True)
        else:
            dlg.unitCombo.Enable(False)
