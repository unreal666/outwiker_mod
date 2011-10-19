# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Oct 27 21:24:33 2010

import wx

import ConfigElements
from outwiker.core.application import Application
from outwiker.gui.guiconfig import EditorConfig
from outwiker.core.config import FontOption

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class EditorPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: EditorPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.fontLabel = wx.StaticText(self, -1, _("Font"))
		self.fontPicker = wx.FontPickerCtrl(self, -1)
		self.lineNumbersCheckBox = wx.CheckBox(self, -1, _("Show line numbers"))
		self.tabWidthLabel = wx.StaticText(self, -1, _("Tab width"))
		self.tabWidthSpin = wx.SpinCtrl(self, -1, "4", min=1, max=100, style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade
		self.config = EditorConfig (Application.config)

		self.LoadState()

	def __set_properties(self):
		# begin wxGlade: EditorPanel.__set_properties
		self.SetSize((404, 254))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: EditorPanel.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_3 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_3.Add(self.fontLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_3.Add(self.fontPicker, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_3.AddGrowableRow(0)
		grid_sizer_3.AddGrowableCol(1)
		mainSizer.Add(grid_sizer_3, 1, wx.EXPAND, 0)
		mainSizer.Add(self.lineNumbersCheckBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_4.Add(self.tabWidthLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_4.Add(self.tabWidthSpin, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		grid_sizer_4.AddGrowableCol(1)
		mainSizer.Add(grid_sizer_4, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.AddGrowableCol(0)
		# end wxGlade


	def LoadState(self):
		# Показывать ли номера строк?
		self.lineNumbers = ConfigElements.BooleanElement (self.config.lineNumbersOption, self.lineNumbersCheckBox)

		# Шрифт для редактора
		fontOption = FontOption (self.config.fontFaceNameOption, 
				self.config.fontSizeOption, 
				self.config.fontIsBold, 
				self.config.fontIsItalic)

		self.fontEditor = ConfigElements.FontElement (fontOption, self.fontPicker)

		# Размер табуляции
		self.tabWidth = ConfigElements.IntegerElement (self.config.tabWidthOption, self.tabWidthSpin, 1, 100)
	

	def Save (self):
		self.lineNumbers.save()
		self.fontEditor.save()
		self.tabWidth.save()


# end of class EditorPanel

