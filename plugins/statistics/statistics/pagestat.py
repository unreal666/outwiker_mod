#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import re

from outwiker.core.attachment import Attachment


class PageStat (object):
    """
    Класс для сбора статистики одиночной страницы
    """
    def __init__ (self, page):
        """
        page - страница, для которой показывается статистика
        """
        self._page = page

        # Типы страниц, по которым можно собрать статистику
        self._supportedPages = ['html', 'text', 'wiki']
        self._wordsRegExp = re.compile ('\w+', re.M | re.U)


    def _testPageType (self):
        if self._page.getTypeString() not in self._supportedPages:
            raise TypeError


    @property
    def symbols (self):
        self._testPageType ()
        return len (self._page.content)


    @property
    def symbolsNotWhiteSpaces (self):
        self._testPageType ()
        chars = [char for char in self._page.content if len (char.strip()) != 0]
        return len (chars)


    @property
    def lines (self):
        self._testPageType ()
        lines = [line for line in self._page.content.split ("\n") if len (line.strip()) != 0]
        return len (lines)


    @property
    def words (self):
        self._testPageType ()
        return len (self._wordsRegExp.findall (self._page.content))
        

    @property
    def attachmentsCount (self):
        attachment = Attachment (self._page)
        currentFiles = attachment.attachmentFull

        filesList = []
        self._getFilesListRecursive (currentFiles, filesList)

        return len (filesList)


    def _getFilesListRecursive (self, currentDirFiles, filesListFlat):
        for fname in currentDirFiles:
            if os.path.isfile (fname):
                filesListFlat.append (fname)
            elif os.path.isdir (fname):
                currentFiles = [os.path.join (fname, listItem) for listItem in os.listdir (fname)]
                self._getFilesListRecursive (currentFiles, filesListFlat)
