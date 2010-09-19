#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты, связанные с созданием вики
"""

import os.path
import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from pages.html.htmlpage import HtmlPageFactory
from core.event import Event
from core.controller import Controller
from core.factory import FactorySelector
from test.utils import removeWiki
import core.exceptions

class TextPageAttachmentTest (unittest.TestCase):
	"""
	Тест для проверки работы с прикрепленными файлами
	"""
	def setUp (self):
		# Количество срабатываний особытий при обновлении страницы
		self.pageUpdateCount = 0
		self.pageUpdateSender = None

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
	

	def tearDown(self):
		removeWiki (self.path)


	def testEvent (self):
		self.pageUpdateCount = 0

		Controller.instance().onPageUpdate += self.onPageUpdate

		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		
		self.assertEqual (self.pageUpdateCount, 1)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page1])

		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )
		
		self.assertEqual (self.pageUpdateCount, 2)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page3])

		Controller.instance().onPageUpdate -= self.onPageUpdate


	def onPageUpdate (self, sender):
		self.pageUpdateCount += 1
		self.pageUpdateSender = sender


	def testRemoveAttaches (self):
		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]
		
		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )

		Controller.instance().onPageUpdate += self.onPageUpdate

		self.rootwiki[page1].removeAttach ([files[0]])

		self.assertEqual (len (self.rootwiki[page1].attachment), 2)
		self.assertEqual (self.pageUpdateCount, 1)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page1])


		self.rootwiki[page3].removeAttach ([files[0], files[1] ])
		
		self.assertEqual (len (self.rootwiki[page3].attachment), 0)
		self.assertEqual (self.pageUpdateCount, 2)
		self.assertEqual (self.pageUpdateSender, self.rootwiki[page3])
		
		Controller.instance().onPageUpdate -= self.onPageUpdate

	
	def testInvalidRemoveAttaches (self):
		"""
		Попытка удалить прикрепления, которого нет
		"""
		files = [u"accept.png", u"add.png", u"anchor.png"]
		page1 = u"Страница 1"

		self.assertRaises (IOError, self.rootwiki[page1].removeAttach, files)


	def testAttach (self):
		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )

		# Заново загрузим вики
		wiki = WikiDocument.load (self.path)

		# Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
		self.assertEqual (len (wiki[page1].attachment), 3)
		self.assertEqual (len (wiki[page3].attachment), 2)
		self.assertEqual (len (wiki[u"Страница 2"].attachment), 0)

		# Проверим пути до прикрепленных файлов
		attachPathPage1 = TextPageAttachmentTest.getFullAttachPath (wiki, page1, files)
		attachPathPage3 = TextPageAttachmentTest.getFullAttachPath (wiki, page3, files)

		#print attachPathPage1
		#print wiki[page1].attachment
		self.assertTrue (attachPathPage1[0] in wiki[page1].attachment)
		self.assertTrue (attachPathPage1[1] in wiki[page1].attachment)
		self.assertTrue (attachPathPage1[2] in wiki[page1].attachment)
		
		self.assertTrue (attachPathPage3[0] in wiki[page3].attachment)
		self.assertTrue (attachPathPage3[1] in wiki[page3].attachment)


	def testAttach2 (self):
		page1 = u"Страница 1"
		page3 = u"Страница 2/Страница 3"

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.rootwiki[page1].attach (fullFilesPath)
		self.rootwiki[page3].attach ( [fullFilesPath[0], fullFilesPath[1] ] )

		# Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
		self.assertEqual (len (self.rootwiki[page1].attachment), 3)
		self.assertEqual (len (self.rootwiki[page3].attachment), 2)
		self.assertEqual (len (self.rootwiki[u"Страница 2"].attachment), 0)

		# Проверим пути до прикрепленных файлов
		attachPathPage1 = TextPageAttachmentTest.getFullAttachPath (self.rootwiki, page1, files)
		attachPathPage3 = TextPageAttachmentTest.getFullAttachPath (self.rootwiki, page3, files)

		#print attachPathPage1
		#print wiki[page1].attachment
		self.assertTrue (attachPathPage1[0] in self.rootwiki[page1].attachment)
		self.assertTrue (attachPathPage1[1] in self.rootwiki[page1].attachment)
		self.assertTrue (attachPathPage1[2] in self.rootwiki[page1].attachment)
		
		self.assertTrue (attachPathPage3[0] in self.rootwiki[page3].attachment)
		self.assertTrue (attachPathPage3[1] in self.rootwiki[page3].attachment)


	@staticmethod
	def getFullAttachPath (wiki, pageSubpath, fnames):
		"""
		Сформировать список полных путей до прикрепленных файлов
		wiki -- загруженная вики
		pageSubpath -- путь до страницы
		fnames -- имена файлов
		"""
		attachPath = os.path.join (wiki[pageSubpath].path, RootWikiPage.attachDir)
		result = [os.path.join (attachPath, fname) for fname in fnames]

		return result


class TextPageCreationTest(unittest.TestCase):
	"""
	Класс тестов, связанных с созданием страниц вики
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

		self.rootwiki[u"Страница 1"].content = u"1234567"
		self.rootwiki[u"Страница 2/Страница 3"].content = u"Абырвалг"
		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = u"Тарам-пам-пам"
		self.rootwiki[u"Страница 1/Страница 5"].content = u"111111"

		self.rootwiki[u"Страница 1"].tags = [u"метка 1"]
		self.rootwiki[u"Страница 2/Страница 3"].tags = [u"метка 2", u"метка 3"]
		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags = [u"метка 1", u"метка 2", u"метка 4"]

		self.rootwiki[u"Страница 2/Страница 3/Страница 4"].icon = "../test/images/feed.gif"

	def tearDown(self):
		removeWiki (self.path)


	def testIcon (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (os.path.basename (wiki[u"Страница 2/Страница 3/Страница 4"].icon), 
				"__icon.gif")


	def testTags (self):
		wiki = WikiDocument.load (self.path)
		self.assertTrue (u"метка 1" in wiki[u"Страница 1"].tags)
		self.assertEqual (len (wiki[u"Страница 1"].tags), 1)

		self.assertTrue (u"метка 2" in wiki[u"Страница 2/Страница 3"].tags)
		self.assertTrue (u"метка 3" in wiki[u"Страница 2/Страница 3"].tags)
		self.assertEqual (len (wiki[u"Страница 2/Страница 3"].tags), 2)

		self.assertTrue (u"метка 1" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertTrue (u"метка 2" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertTrue (u"метка 4" in wiki[u"Страница 2/Страница 3/Страница 4"].tags)
		self.assertEqual (len (wiki[u"Страница 2/Страница 3/Страница 4"].tags), 3)



	def testCreation (self):
		self.assertTrue (os.path.exists (self.path))
		self.assertTrue (os.path.exists (os.path.join (self.path, RootWikiPage.pageConfig) ) )


	def testInvalidPageName (self):
		children = len (self.rootwiki.children)
		self.assertRaises (Exception, TextPageFactory.create, self.rootwiki, u"+*5name:/\0", [])
		self.assertEqual (len (self.rootwiki.children), children)
	

	def testInvalidPageName2 (self):
		self.assertRaises (core.exceptions.DublicateTitle, 
				TextPageFactory.create, self.rootwiki, u"страНица 1", [])

		self.assertRaises (core.exceptions.DublicateTitle, 
				TextPageFactory.create, self.rootwiki[u"Страница 1"], u"страНица 5", [])


	def testPageCreate (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].title, u"Страница 1")
		self.assertEqual (wiki[u"Страница 2"].title, u"Страница 2")
		self.assertEqual (wiki[u"Страница 2/Страница 3"].title, u"Страница 3")
	

	def testCreateTextContent (self):
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].content, u"1234567")
		self.assertEqual (wiki[u"Страница 2/Страница 3"].content, u"Абырвалг")
		self.assertEqual (wiki[u"Страница 2/Страница 3/Страница 4"].content, u"Тарам-пам-пам")
		self.assertEqual (wiki[u"Страница 1/Страница 5"].content, u"111111")
	

	def testLastViewedPage1 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		wiki = WikiDocument.load (self.path)
		section = u"History"
		param = u"LastViewedPage"

		wiki.selectedPage = wiki[u"Страница 1"]
		subpath = wiki.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		subpath = wiki.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 2/Страница 3")

		# Прверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath = wiki2.getParameter (section, param)
		self.assertEqual (subpath, u"Страница 2/Страница 3")

	
	def testLastViewedPage1 (self):
		"""
		Тест на то, что в настройках корня сохраняется ссылка на последнюю просмотренную страницу
		"""
		wiki = WikiDocument.load (self.path)
		section = u"History"
		param = u"LastViewedPage"

		self.assertEqual (wiki.lastViewedPage, None)

		wiki.selectedPage = wiki[u"Страница 1"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 1")

		wiki.selectedPage = wiki[u"Страница 2/Страница 3"]
		subpath = wiki.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")

		# Прверим, что параметр сохраняется в файл
		wiki2 = WikiDocument.load (self.path)

		subpath = wiki2.lastViewedPage
		self.assertEqual (subpath, u"Страница 2/Страница 3")



class ConfigPagesTest (unittest.TestCase):
	"""
	Тесты, связанные с настройками страниц и вики в целом
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])

		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])


	def testSetRootParams (self):
		self.rootwiki.setParameter (u"TestSection_1", u"value1", u"Значение 1")

		self.assertEqual (self.rootwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.create (self.path)
		self.assertEqual (wiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")


	def testSetPageParams (self):
		self.rootwiki[u"Страница 1"].setParameter (u"TestSection_1", u"value1", u"Значение 1")

		self.assertEqual (self.rootwiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")

		# Прочитаем вики и проверим установленный параметр
		wiki = WikiDocument.load (self.path)
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")


	def testSubwikiParams (self):
		"""
		Проверка того, что установка параметров страницы как полноценной вики не портит исходные параметры
		"""
		self.rootwiki[u"Страница 1"].setParameter (u"TestSection_1", u"value1", u"Значение 1")

		path = os.path.join (self.path, u"Страница 1")
		subwiki = WikiDocument.load (path)
		
		self.assertEqual (subwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")

		# Добавим новый параметр
		subwiki.setParameter (u"TestSection_2", u"value2", u"Значение 2")
		
		self.assertEqual (subwiki.getParameter (u"TestSection_1", u"value1"), u"Значение 1")
		self.assertEqual (subwiki.getParameter (u"TestSection_2", u"value2"), u"Значение 2")

		# На всякий случай прочитаем вики еще раз
		wiki = WikiDocument.load (self.path)
		
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_1", u"value1"), 
				u"Значение 1")
		
		self.assertEqual (wiki[u"Страница 1"].getParameter (u"TestSection_2", u"value2"), 
				u"Значение 2")


class BookmarksTest (unittest.TestCase):
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

		self.bookmarkCount = 0
		self.bookmarkSender = None


	def onBookmark (self, bookmarks):
		self.bookmarkCount += 1
		self.bookmarkSender = bookmarks
	

	def testAddToBookmarks (self):
		# По умолчанию закладок нет
		self.assertEqual (len (self.rootwiki.bookmarks), 0)

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

		self.assertEqual (len (self.rootwiki.bookmarks), 1)
		self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")

		# Проверим, что закладки сохраняются в конфиг
		wiki = WikiDocument.load (self.path)

		self.assertEqual (len (wiki.bookmarks), 1)
		self.assertEqual (wiki.bookmarks[0].title, u"Страница 1")
	

	def testManyBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.assertEqual (len (self.rootwiki.bookmarks), 3)
		self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
		self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2")
		self.assertEqual (self.rootwiki.bookmarks[2].subpath, u"Страница 2/Страница 3")
	

	def testRemoveBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])

		self.assertEqual (len (self.rootwiki.bookmarks), 2)
		self.assertEqual (self.rootwiki.bookmarks[0].subpath, u"Страница 1")
		self.assertEqual (self.rootwiki.bookmarks[1].subpath, u"Страница 2/Страница 3")
	

	def testBookmarkEvent (self):
		Controller.instance().onBookmarksChanged += self.onBookmark

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.assertEqual (self.bookmarkCount, 1)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)

		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.assertEqual (self.bookmarkCount, 2)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)


		self.rootwiki.bookmarks.remove (self.rootwiki[u"Страница 2"])
		self.assertEqual (self.bookmarkCount, 3)
		self.assertEqual (self.bookmarkSender, self.rootwiki.bookmarks)
	

	def testPageInBookmarks (self):
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 2/Страница 3"])

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1"]), 
				True)

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 2/Страница 3"]),
				True)

		self.assertEqual (self.rootwiki.bookmarks.pageMarked (self.rootwiki[u"Страница 1/Страница 5"]), 
				False)
	

	def testCloneBookmarks (self):
		"""
		Тест на повторное добавление одной и той же страницы
		"""
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])
		self.rootwiki.bookmarks.add (self.rootwiki[u"Страница 1"])

		self.assertEqual (len (self.rootwiki.bookmarks), 1)
		self.assertEqual (self.rootwiki.bookmarks[0].title, u"Страница 1")


class RemovePagesTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.treeUpdateCount = 0
		self.pageRemoveCount = 0


	def onTreeUpdate (self, bookmarks):
		"""
		Обработка события при удалении страницы (обновление дерева)
		"""
		self.treeUpdateCount += 1

	
	def onPageRemove (self, bookmarks):
		"""
		Обработка события при удалении страницы
		"""
		self.pageRemoveCount += 1

	
	def testRemove1 (self):
		Controller.instance().onTreeUpdate += self.onTreeUpdate
		Controller.instance().onPageRemove += self.onPageRemove

		# Удаляем страницу из корня
		page6 = self.rootwiki[u"Страница 6"]
		page6.remove()
		self.assertEqual (len (self.rootwiki), 2)
		self.assertEqual (self.rootwiki[u"Страница 6"], None)
		self.assertTrue (page6.isRemoved)
		self.assertEqual (self.treeUpdateCount, 1)
		self.assertEqual (self.pageRemoveCount, 1)

		# Удаляем подстраницу
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		page3.remove()

		self.assertEqual (len (self.rootwiki[u"Страница 2"]), 0)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3"], None)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3/Страница 4"], None)
		self.assertTrue (page3.isRemoved)
		self.assertTrue (page4.isRemoved)
		self.assertEqual (self.treeUpdateCount, 2)
		self.assertEqual (self.pageRemoveCount, 3)
		
		Controller.instance().onTreeUpdate -= self.onTreeUpdate
		Controller.instance().onPageRemove -= self.onPageRemove
	

	def testIsRemoved (self):
		"""
		Провкерка свойства isRemoved
		"""
		page6 = self.rootwiki[u"Страница 6"]
		page6.remove()
		self.assertTrue (page6.isRemoved)

		# Удаляем подстраницу
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		page3.remove()

		self.assertTrue (page3.isRemoved)
		self.assertTrue (page4.isRemoved)

		self.assertFalse (self.rootwiki[u"Страница 2"].isRemoved)

	def testRemoveSelectedPage1 (self):
		"""
		Удаление выбранной страницы
		"""
		# Если удаляется страница из корня, то никакая страница не выбирается
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 6"]
		self.rootwiki[u"Страница 6"].remove()

		self.assertEqual (self.rootwiki.selectedPage, None)

		# Если удаляется страница более глубокая, то выбранной страницей становится родитель
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		self.rootwiki.selectedPage.remove()
		self.assertEqual (self.rootwiki.selectedPage, self.rootwiki[u"Страница 2/Страница 3"])
	

	def testRemoveSelectedPage2 (self):
		"""
		Удаление выбранной страницы
		"""
		# Если удаляется страница более глубокая, то выбранной страницей становится родитель
		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]
		self.rootwiki.selectedPage.remove()
		self.assertEqual (self.rootwiki.selectedPage, self.rootwiki[u"Страница 2/Страница 3"])


	def testRemoveFromBookmarks1 (self):
		"""
		Проверка того, что страница удаляется из закладок
		"""
		page = self.rootwiki[u"Страница 6"]
		self.rootwiki.bookmarks.add (page)
		page.remove()

		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page))
	

	def testRemoveFromBookmarks2 (self):
		"""
		Проверка того, что подстраница удаленной страницы удаляется из закладок
		"""
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		self.rootwiki.bookmarks.add (page2)
		self.rootwiki.bookmarks.add (page3)
		self.rootwiki.bookmarks.add (page4)

		page2.remove()

		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page2))
		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page3))
		self.assertFalse (self.rootwiki.bookmarks.pageMarked (page4))


class RenameTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (self.rootwiki, u"Страница 6", [])

		self.treeUpdateCount = 0

	
	def testRename1 (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"Страница 1 new"

		self.assertEqual (page.title, u"Страница 1 new")
		self.assertEqual (self.rootwiki[u"Страница 1 new"], page)
		self.assertEqual (page.subpath, u"Страница 1 new")
		self.assertEqual (self.rootwiki[u"Страница 1"], None)

	
	def testInvalidRename (self):
		def rename (page, newtitle):
			page.title = newtitle

		self.assertRaises (core.exceptions.DublicateTitle, rename, 
				self.rootwiki[u"Страница 1"], u"СтраНица 6")
	

	def testRename2 (self):
		page = self.rootwiki[u"Страница 2/Страница 3"]
		page.title = u"Страница 3 new"

		self.assertEqual (page.title, u"Страница 3 new")
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3 new"], page)
		self.assertEqual (page.subpath, u"Страница 2/Страница 3 new")
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3"], None)
	

	def testRename3 (self):
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = page3[u"Страница 4"]

		page3.title = u"Страница 3 new"

		self.assertEqual (page3[u"Страница 4"], page4)
		self.assertEqual (self.rootwiki[u"Страница 2/Страница 3 new/Страница 4"], page4)
	

	def testRename4 (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"СтрАницА 1"

		self.assertEqual (page.title, u"СтрАницА 1")
		self.assertEqual (self.rootwiki[u"СтрАницА 1"], page)
		self.assertEqual (page.subpath, u"СтрАницА 1")

	
	def testLoad (self):
		page = self.rootwiki[u"Страница 1"]
		page.title = u"Страница 1 new"

		wiki = WikiDocument.load (self.path)
		self.assertNotEqual (wiki[u"Страница 1 new"], None)
		self.assertEqual (wiki[u"Страница 1"], None)
	

	def testBookmarks1 (self):
		page = self.rootwiki[u"Страница 6"]
		self.rootwiki.bookmarks.add (page)
		page.title = u"Страница 6 new"

		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page))
	

	def testBookmarks2 (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		self.rootwiki.bookmarks.add (page2)
		self.rootwiki.bookmarks.add (page3)
		self.rootwiki.bookmarks.add (page4)

		page2.title = u"Страница 2 new"

		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page2))
		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page3))
		self.assertTrue (self.rootwiki.bookmarks.pageMarked (page4))
	

	def testPath (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		page2.title = u"Страница 2 new"

		self.assertEqual (page2.path, os.path.join (self.path, u"Страница 2 new"))
		self.assertEqual (page3.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3"))
		self.assertEqual (page4.path, os.path.join (self.path, u"Страница 2 new", u"Страница 3", u"Страница 4"))
	

	def testConfig (self):
		page2 = self.rootwiki[u"Страница 2"]
		page3 = self.rootwiki[u"Страница 2/Страница 3"]
		page4 = self.rootwiki[u"Страница 2/Страница 3/Страница 4"]

		page2.title = u"Страница 2 new"

		page2.tags = [u"тег 1"]
		page3.tags = [u"тег 2"]
		page4.tags = [u"тег 3"]

		self.assertEqual (page2.tags[0], u"тег 1")
		self.assertEqual (page3.tags[0], u"тег 2")
		self.assertEqual (page4.tags[0], u"тег 3")
