# -*- coding: utf-8 -*-

import wx


class ThumbDialog (wx.Dialog):
    WIDTH = 0
    HEIGHT = 1
    MAX_SIZE = 2
    UNIT_ITEMS = [u"", u"%", u"ch", u"cm", u"em", u"ex", u"in", u"mm", u"pc",
                  u"pt", u"px", u"rem", u"vh", u"vmin", u"vw", 'vh']

    def __init__ (self, parent, filesList, selectedFile):
        """
        parent - родительское окно
        filesList - список файлов, отображаемых в диалоге
        selectedFile - файл выбранный по умолчанию. Если selectedFile == None, никакой файл по умолчанию не выбирается
        """
        super (ThumbDialog, self).__init__ (parent,
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                                            title=_("Thumbnails"))

        self.__filesList = filesList
        self.__selectedFile = selectedFile

        self.__createGui()
        self.filesListCombo.SetFocus()
        self.Center(wx.BOTH)


    @property
    def fileName (self):
        return self.filesListCombo.GetValue()


    @property
    def scaleType (self):
        return self.scaleCombo.GetSelection()


    @property
    def size (self):
        return self.sizeCtrl.GetValue()


    @property
    def softMode (self):
        return self.softmodeCheckBox.GetValue()


    @softMode.setter
    def softMode (self, value):
        return self.softmodeCheckBox.SetValue(value)


    @property
    def unit (self):
        return self.unitCombo.GetSelection()

    @property
    def nolink (self):
        return self.nolinkCheckBox.GetValue()


    def __createGui (self):
        # Элементы для выбор имени файла
        filenameLabel = wx.StaticText (self, label=_(u"File name"))
        self.filesListCombo = wx.ComboBox (self,
                                           choices=[u""] + self.__filesList,
                                           style=wx.CB_READONLY)
        self.filesListCombo.SetSelection (0)
        self.filesListCombo.SetMinSize ((250, -1))

        if len (self.__selectedFile) > 0:
            assert self.__selectedFile in self.__filesList
            self.filesListCombo.SetStringSelection (self.__selectedFile)

        # Элементы для выбора размера
        scaleLabel = wx.StaticText (self, label=_(u"Thumbnail size"))

        scaleItems = [_(u"Width"), _(u"Height"), _(u"Max size")]
        self.scaleCombo = wx.ComboBox (self,
                                       choices=scaleItems,
                                       style=wx.CB_READONLY)
        self.scaleCombo.SetSelection (0)
        self.scaleCombo.SetMinSize ((250, -1))

        self.sizeCtrl = wx.SpinCtrl (self, min=0, max=10000, initial=0)
        self.sizeCtrl.SetMinSize ((100, -1))
        sizeLabel = wx.StaticText (self, label=_(u"0 - default size"))

        # Элемент для установки soft-режима
        self.softmodeCheckBox = wx.CheckBox (self, label=_(u"Soft Mode"))

        # Элемент для установки режима "Без ссылки"
        self.nolinkCheckBox = wx.CheckBox (self, label=_(u"Without Link"))

        # Единицы измерения для soft-режима
        self.unitCombo = wx.ComboBox (self,
                                      choices=self.UNIT_ITEMS,
                                      style=wx.CB_READONLY,
                                      )

        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)

        # Расстановка элементов
        mainSizer = wx.FlexGridSizer(rows=0, cols=2, vgap=0, hgap=0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (6)

        mainSizer.Add (filenameLabel, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.Add (self.filesListCombo, 0, flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)

        mainSizer.Add (scaleLabel, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        mainSizer.AddStretchSpacer()

        mainSizer.Add (self.scaleCombo, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)
        mainSizer.Add (self.sizeCtrl, 0, flag=wx.ALL | wx.EXPAND, border=4)

        mainSizer.AddStretchSpacer()
        mainSizer.Add (sizeLabel, 0, flag=wx.ALL | wx.EXPAND, border=4)

        mainSizer.AddStretchSpacer()
        mainSizer.AddStretchSpacer()

        innerSizer = wx.FlexGridSizer(rows=0, cols=3, vgap=0, hgap=0)
        innerSizer.Add (self.softmodeCheckBox, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)
        innerSizer.Add (self.nolinkCheckBox, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)
        innerSizer.Add (self.unitCombo, 0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=4)
        mainSizer.Add (innerSizer, 0, flag=wx.ALL | wx.EXPAND, border=4)
        mainSizer.AddStretchSpacer()

        mainSizer.AddStretchSpacer()
        mainSizer.Add (okCancel, 0, flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border=4)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()
