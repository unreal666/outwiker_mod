#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Mar 23 21:59:58 2010

#import sys
import os
import wx

from core.config import Config
import core.system

from gui.MainWindow import MainWindow

class OutWiker(wx.App):
	def __init__(self, *args, **kwds):
		wx.App.__init__ (self, *args, **kwds)

		self._configFileName = os.path.join (core.system.getCurrentDir(), u"outwiker.ini")
		self.config = Config(self._configFileName)

	
	def getConfig (self):
		return self.config


	def OnInit(self):
		wx.InitAllImageHandlers()
		mainWnd = MainWindow(None, -1, "")
		self.SetTopWindow(mainWnd)
		mainWnd.Show()
		return 1

# end of class OutWiker

if __name__ == "__main__":
	#print sys.argv[0]
	outwiker = OutWiker(0)
	outwiker.MainLoop()
