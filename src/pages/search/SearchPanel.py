# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat May 08 19:50:04 2010

import ConfigParser

import wx

import pages.search.searchpage
from core.search import Searcher, HtmlReport, TagsList, AllTagsSearchStrategy, AnyTagSearchStrategy
from gui.htmlview import HtmlView

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class SearchPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self._page = None
		self._allTags = None

		# Секция для хранения найденных результатов (кэш)
		self._resultsSection = u"SearchResults"

		self._resultOptionTemplate = u"page_%d"

		self._strategyList = [AnyTagSearchStrategy, AllTagsSearchStrategy]

		# begin wxGlade: SearchPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.wordsLabel = wx.StaticText(self, -1, "Search words: ")
		self.wordsTextCtrl = wx.TextCtrl(self, -1, "")
		self.tagsLabel = wx.StaticText(self, -1, "Tags: ")
		self.tagsList = wx.CheckListBox(self, -1, choices=[])
		self.tagsStrategy = wx.RadioBox(self, -1, "Tags", choices=["Any tag", "All tags"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
		self.clearTagsBtn = wx.Button(self, -1, "Clear all tags")
		self.searchBtn = wx.Button(self, -1, "Find")
		self.resultWindow = HtmlView(self, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.onClear, self.clearTagsBtn)
		self.Bind(wx.EVT_BUTTON, self.onFind, self.searchBtn)
		# end wxGlade

		self.Bind (wx.EVT_CLOSE, self.onClose)
	

	def onClose (self, event):
		self.save()


	def updatePageInfo (self):
		"""
		Обновить интерфейс, чтобы он соответствовал настройкам страницы
		"""
		assert self._page != None

		self.updateSearchPhrase()
		self.updateTagsList()
	

	def updateTagsList (self):
		"""
		Обновить список тегов
		"""
		assert self._page != None

		# заполним список тегов
		list_items = [u"%s (%d)" % (tag, len (self._allTags[tag] ) ) for tag in self._allTags ]
		self.tagsList.InsertItems (list_items, 0)

		tags = pages.search.searchpage.getTags (self._page)

		# Поставим галки, где нужно
		n = 0
		for tag in self._allTags:
			if tag in tags:
				self.tagsList.Check (n)
			n += 1

		# Установим стратегию поиска по тегам
		strategy = pages.search.searchpage.getStrategy (self._page)
		strategyIndex = self._strategyList.index (strategy)

		self.tagsStrategy.SetSelection(strategyIndex)

		
	def updateSearchPhrase (self):
		phrase = pages.search.searchpage.getPhrase (self._page)
		self.wordsTextCtrl.SetValue (phrase)
	

	def save (self):
		"""
		Сохранить настройки страницы
		"""
		if self._page != None and not self._page.isRemoved:
			self._saveSearchPhrase()
			self._saveSearchTags()
			self._saveSearchTagsStrategy()
	

	def _saveSearchPhrase (self):
		"""
		Сохранить искомую фразу в настройки страницы
		"""
		phrase = self.wordsTextCtrl.GetValue()
		pages.search.searchpage.setPhrase (self._page, phrase)
	

	def _saveSearchTags (self):
		"""
		Сохранить искомые теги в настройке страницы
		"""
		tags = self._getSearchTags()
		pages.search.searchpage.setTags (self._page, tags)
	

	def _saveSearchTagsStrategy (self):
		"""
		Сохранить стратегию поиска по тегам (все теги или любой тег)
		"""
		strategyIndex = self.tagsStrategy.GetSelection()
		strategy = self._strategyList[strategyIndex]
		pages.search.searchpage.setStrategy (self._page, strategy)


	@property
	def page (self):
		return self._page

	@page.setter
	def page (self, value):
		self._page = value
		self.resultWindow.page = value
		self._allTags = TagsList (self._page.root)

		self.updatePageInfo()

		resultPages = self._loadResults ()
		self._showResults (resultPages)


	def __set_properties(self):
		# begin wxGlade: SearchPanel.__set_properties
		self.tagsList.SetMinSize((250, 150))
		self.tagsStrategy.SetSelection(0)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: SearchPanel.__do_layout
		mainSizer = wx.FlexGridSizer(4, 1, 0, 0)
		tagsSizer = wx.FlexGridSizer(1, 3, 0, 0)
		tagsButtons = wx.FlexGridSizer(2, 1, 0, 0)
		phraseSizer = wx.FlexGridSizer(1, 2, 0, 0)
		phraseSizer.Add(self.wordsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
		phraseSizer.Add(self.wordsTextCtrl, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		phraseSizer.AddGrowableCol(1)
		mainSizer.Add(phraseSizer, 1, wx.EXPAND, 0)
		tagsSizer.Add(self.tagsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
		tagsSizer.Add(self.tagsList, 0, wx.ALL|wx.EXPAND, 2)
		tagsButtons.Add(self.tagsStrategy, 0, wx.EXPAND, 0)
		tagsButtons.Add(self.clearTagsBtn, 0, wx.ALL|wx.EXPAND, 2)
		tagsButtons.AddGrowableRow(0)
		tagsButtons.AddGrowableCol(0)
		tagsSizer.Add(tagsButtons, 1, wx.EXPAND, 0)
		tagsSizer.AddGrowableCol(1)
		mainSizer.Add(tagsSizer, 1, wx.EXPAND, 0)
		mainSizer.Add(self.searchBtn, 0, wx.ALL|wx.EXPAND, 2)
		mainSizer.Add(self.resultWindow, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(3)
		mainSizer.AddGrowableCol(0)
		# end wxGlade


	def onFind(self, event): # wxGlade: SearchPanel.<event_handler>
		assert self._page != None
		
		self.save()

		phrase = self.wordsTextCtrl.GetValue ()
		tags = self._getSearchTags()

		strategy = pages.search.searchpage.getStrategy(self._page)

		searcher = Searcher (phrase, tags, strategy)
		resultPages = searcher.find (self.page.root)

		self._saveResults (resultPages)
		self._showResults (resultPages)
	

	def _getSearchTags (self):
		n = 0

		tags = []

		for tag in self._allTags:
			if self.tagsList.IsChecked (n):
				tags.append (tag)

			n += 1

		return tags

	

	def _showResults (self, resultPages):
		html = HtmlReport.generate (resultPages)
		self.resultWindow.SetPage (html)
	

	def _saveResults (self, resultPages):
		assert self._page != None

		self._page.params.remove_section (self._resultsSection)

		for n in range (len (resultPages)):
			option = self._resultOptionTemplate % n
			self._page.params.set (self._resultsSection, option, resultPages[n].subpath)

	
	def _loadResults (self):
		assert self._page != None

		n = 0
		resultPages = []

		try:
			while True:
				option = self._resultOptionTemplate % n
				subpath = self._page.params.get (self._resultsSection, option)

				page = self._page.root[subpath]
				if page != None:
					resultPages.append (page)

				n += 1
		except:
			pass

		return resultPages


	def initGui (self, mainWindow):
		"""
		Добавить элементы управления в главное окно
		"""
		pass


	def removeGui (self):
		"""
		Убрать за собой элементы управления
		"""
		pass


	def onClear(self, event): # wxGlade: SearchPanel.<event_handler>
		for n in range (self.tagsList.GetCount()):
			self.tagsList.Check (n, False)

# end of class SearchPanel


