#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import ConfigParser
import shutil

from controller import Controller
from core.config import Config
from core.bookmarks import Bookmarks
from core.search import TagsList
import core.exceptions


class RootWikiPage (object):
	"""
	Класс для корня вики
	"""

	pageConfig = u"__page.opt"
	contentFile = u"__page.text"
	attachDir = u"__attach"
	iconName = u"__icon"

	def __init__(self, path):
		"""
		Constructor.
		
		path -- путь до страницы относительно корня дерева
		"""
		# Путь до страницы
		self._path = path
		self._parent = None
		self._children = []

		self._params = self._readParams()

	
	def _readParams (self):
		return Config (os.path.join (self.path, RootWikiPage.pageConfig) )


	@property
	def params (self):
		return self._params


	@property
	def path (self):
		return self._path
	

	@property
	def parent (self):
		return self._parent


	@property
	def children (self):
		return self._children[:]


	@property
	def root (self):
		"""
		Найти корень дерева по странице
		"""
		result = self
		while result.parent != None:
			result = result.parent

		return result


	def getParameter (self, section, param):
		"""
		Получить значение параметра param из секции section
		"""
		return self._params.get (section, param)


	def setParameter (self, section, param, value):
		"""
		Установить значение параметра param секции section в value
		"""
		self._params.set (section, param, value)
		#self.save()


	def save (self):
		if not os.path.exists (self.path):
			os.mkdir (self.path)

		self._params.save()


	def __len__ (self):
		return len (self._children)


	def __getitem__ (self, path):
		"""
		Получить нужную страницу по относительному пути в дереве
		"""
		# Разделим путь по составным частям
		titles = path.split ("/")
		page = self

		for title in titles:
			found = False
			for child in page.children:
				if child.title.lower() == title.lower():
					page = child
					found = True

			if not found:
				page = None
				break

		return page


	def getChildren(self):
		"""
		Загрузить дочерние узлы
		"""
		try:
			entries = os.listdir (self.path)
		except OSError:
			raise IOError

		result = []

		for name in entries:
			fullpath = os.path.join (self.path, name)

			if not name.startswith ("__") and os.path.isdir (fullpath):
				try:
					page = WikiPage.load (fullpath, self)
				except Exception as e:
					#raise
					continue

				result.append (page)

		return result


	@staticmethod
	def testDublicate (parent, title):
		"""
		Проверить заголовок страницы на то, что в родителе нет страницы с таким заголовком
		"""
		return parent[title] == None
	

class WikiDocument (RootWikiPage):
	sectionHistory = u"History"
	paramHistory = u"LastViewedPage"

	def __init__ (self, path):
		RootWikiPage.__init__ (self, path)
		self._selectedPage = None
		self.bookmarks = Bookmarks (self, self._params)


	@staticmethod
	def load(path):
		"""
		Загрузить корневую страницу вики.
		Использовать этот метод вместо конструктора
		"""
		result = WikiDocument(path)
		result._children = result.getChildren()
		Controller.instance().onTreeUpdate(result)
		return result


	@staticmethod
	def create (path):
		"""
		Создать корень для вики
		"""
		root = WikiDocument (path)
		root.save()
		Controller.instance().onTreeUpdate(root)

		return root

	@property
	def selectedPage (self):
		return self._selectedPage

	@selectedPage.setter
	def selectedPage (self, page):
		self._selectedPage = page

		if page != None:
			self.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					page.subpath)

		Controller.instance().onPageSelect(self._selectedPage)
		self.save()
	

	@property
	def lastViewedPage (self):
		try:
			subpath = self.getParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory)
			return subpath
		except ConfigParser.NoSectionError:
			pass
		except ConfigParser.NoOptionError:
			pass

	


class WikiPage (RootWikiPage):
	"""
	Страница в дереве.
	"""

	def __init__(self, path, title, parent):
		"""
		Constructor.
		
		path -- путь до страницы
		"""
		if not RootWikiPage.testDublicate(parent, title):
			raise core.exceptions.DublicateTitle

		RootWikiPage.__init__ (self, path)
		self._title = title
		self._parent = parent
		parent._children.append (self)


	@property
	def title (self):
		return self._title

	
	@title.setter
	def title (self, newtitle):
		oldtitle = self.title
		oldpath = self.path
		oldsubpath = self.subpath

		if oldtitle == newtitle:
			return

		# Проверка на дубликат страниц, а также на то, что в заголовке страницы
		# может меняться только регинстр букв
		if not self.canRename(newtitle):
			raise core.exceptions.DublicateTitle

		newpath = os.path.join (os.path.dirname (oldpath), newtitle)
		os.renames (oldpath, newpath)
		self._title = newtitle

		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					self.subpath)

		Controller.instance().onPageRename (self, oldsubpath)
		Controller.instance().onTreeUpdate (self)
	

	def canRename (self, newtitle):
		return (self.title.lower() == newtitle.lower() or
				self.parent[newtitle] == None)
	

	@staticmethod
	def __renamePaths (page, newPath):
		"""
		Скорректировать пути после переименования страницы
		"""
		oldPath = page.path
		page._path = newPath
		page._params = page._readParams()

		for child in page.children:
			newChildPath = child.path.replace (oldPath, newPath, 1)
			WikiPage.__renamePaths (child, newChildPath)

	
	def moveTo (self, newparent):
		"""
		Переместить запись к другому родителю
		"""
		if self._parent == newparent:
			return

		# Проверка на то, что в новом родителе нет записи с таким же заголовком
		if newparent[self.title] != None:
			raise core.exceptions.DublicateTitle

		oldpath = self.path
		oldparent = self.parent

		# Новый путь для страницы
		newpath = os.path.join (newparent.path, self.title)

		try:
			shutil.move (oldpath, newpath)
		except shutil.Error:
			raise core.exceptions.TreeException

		self._parent = newparent
		oldparent._children.remove (self)
		newparent._children.append (self)
		
		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					self.subpath)

		Controller.instance().onTreeUpdate (self)


	@property
	def type (self):
		return self._type


	@property
	def icon (self):
		return self._getIcon()


	@icon.setter
	def icon (self, iconpath):
		name = os.path.basename (iconpath)
		dot = name.rfind (".")
		extension = name[dot:]

		newname = RootWikiPage.iconName + extension
		newpath = os.path.join (self.path, newname)

		if iconpath != newpath:
			shutil.copyfile (iconpath, newpath)

		Controller.instance().onPageUpdate (self)
		Controller.instance().onTreeUpdate (self)

		return newpath



	@property
	def tags (self):
		return self._tags

	@tags.setter
	def tags (self, tags):
		self._tags = tags[:]
		self.save()
		Controller.instance().onPageUpdate(self)


	@property
	def attachment (self):
		"""
		Возвращает список прикрепленных файлов.
		Пути до файлов полные
		"""
		return self._getAttachments()


	def _getAttachments(self):
		"""
		Найти все приаттаченные файлы
		Пути до файлов полные
		"""
		path = os.path.join (self.path, RootWikiPage.attachDir)

		if not os.path.exists (path):
			return []

		result = [os.path.join (path, fname) for fname in os.listdir (path)]

		return result


	def attach (self, files):
		"""
		Прикрепить файл к странице
		files -- список файлов, которые надо прикрепить
		"""
		attachPath = os.path.join (self.path, RootWikiPage.attachDir)
		
		if not os.path.exists (attachPath):
			os.mkdir (attachPath)

		for fname in files:
			shutil.copy (fname, attachPath)

		Controller.instance().onPageUpdate (self)
	

	def removeAttach (self, files):
		"""
		Удалить прикрепленные файлы
		"""
		attachPath = os.path.join (self.path, RootWikiPage.attachDir)

		for fname in files:
			path = os.path.join (attachPath, fname)
			try:
				os.remove (path)
			except OSError:
				Controller.instance().onPageUpdate (self)
				raise IOError (u"Can't remove %s" % fname)

		Controller.instance().onPageUpdate (self)


	def _getIcon (self):
		files = os.listdir (self.path)

		for file in files:
			if (file.startswith (RootWikiPage.iconName) and
					not os.path.isdir (file)):
				return os.path.join (self.path, file)
	

	def _load (self):
		"""
		Загрузить параметры страницы
		"""
		self._type = self._params.get ("General", "type")

		# Теги страницы
		self._tags = self._getTags (self._params)

		self._children = self.getChildren ()
	

	@staticmethod
	def load (path, parent):
		"""
		Загрузить страницу.
		Использовать этот метод вместо конструктора, когда надо загрузить страницу
		"""
		title = os.path.basename(path)
		page = WikiPage (path, title, parent)

		try:
			page._load ()
		except Exception:
			parent._children.remove (page)
			raise

		return page


	def save (self):
		"""
		Сохранить страницу
		"""
		if not os.path.exists (self.path):
			os.mkdir (self.path)

		attachPath = os.path.join (self.path, RootWikiPage.attachDir)

		if not os.path.exists (attachPath):
			os.mkdir (attachPath)

		try:
			text = self.content
		except IOError:
			text = u""

		with open (os.path.join (self.path, RootWikiPage.contentFile), "w") as fp:
			fp.write (text.encode ("utf-8"))

		self._saveOptions ()


	def _saveOptions (self):
		"""
		Сохранить настройки
		"""
		self._params.set (u"General", u"type", self.type)

		tags = reduce (lambda full, tag: full + ", " + tag, self._tags, "")

		# Удалим начальные ", "
		tags = tags[2: ]
		self._params.set (u"General", u"tags", tags)


	@staticmethod
	def create (parent, path, title, type, tags):
		"""
		Создать страницу. Вызывать этот метод вместо конструктора
		"""
		page = WikiPage (path, title, parent)

		try:
			page._create (title, type, tags)
		except Exception:
			parent._children.remove (page)
			raise

		return page


	def _create (self, title, type, tags):
		self._title = title
		self._tags = tags[:]
		self._type = type
		
		self.save()
		Controller.instance().onPageCreate(self)
		Controller.instance().onTreeUpdate(self)
	

	def _getTags (self, configParser):
		"""
		Выделить теги из строки конфигурационного файла
		"""
		try:
			tagsString = configParser.get ("General", "tags")
		except ConfigParser.NoOptionError:
			return []

		tags = TagsList.parseTagsList (tagsString)

		#tags = [tag.strip() for tag in tagsString.split (",") 
				#if len (tag.strip()) > 0]

		return tags

	
	@property
	def content(self):
		"""
		Прочитать файл-содержимое страницы
		"""
		text = ""

		try:
			with open (os.path.join (self.path, RootWikiPage.contentFile)) as fp:
				text = fp.read()
		except IOError:
			pass
		
		return unicode (text, "utf-8")


	@content.setter
	def content (self, text):
		path = os.path.join (self.path, RootWikiPage.contentFile)

		with open (path, "wb") as fp:
			fp.write (text.encode ("utf-8"))

		Controller.instance().onPageUpdate(self)
	

	@property
	def textContent (self):
		"""
		Получить контент в текстовом виде.
		Используется для поиска по страницам.
		В большинстве случаев достаточно вернуть просто content
		"""
		return self.content
	

	@property
	def subpath (self):
		result = self.title
		page = self.parent

		while page.parent != None:
			# Пока не дойдем до корня, у которого нет заголовка, и родитель - None
			result = page.title + "/" + result
			page = page.parent

		return result


	def remove (self):
		"""
		Удалить страницу
		"""
		self._removePageFromTree (self)

		try:
			shutil.rmtree (self.path)
		except OSError:
			raise IOError

		# Если выбранная страница была удалена
		if self.root.selectedPage != None and self.root.selectedPage.isRemoved:
			# Новая выбранная страница взамен старой
			newselpage = self.root.selectedPage
			while newselpage.parent != None and newselpage.isRemoved:
				newselpage = newselpage.parent

			# Если попали в корень дерева
			if newselpage.parent == None:
				newselpage = None

			self.root.selectedPage = newselpage
		
		Controller.instance().onTreeUpdate(self.root)
	

	def _removePageFromTree (self, page):
		page.parent._children.remove (page)
		Controller.instance().onPageRemove (page)

		for child in page.children:
			page._removePageFromTree (child)


	@property
	def isRemoved (self):
		"""
		Проверить, что страница удалена
		"""
		return self not in self.parent.children
	

