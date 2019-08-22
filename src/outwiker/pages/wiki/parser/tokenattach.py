# -*- coding: utf-8 -*-

import os.path
from abc import ABCMeta, abstractmethod

from outwiker.core.attachment import Attachment
from outwiker.core.commands import isImage
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.libs.pyparsing import Literal

from .utils import concatenate


class AttachFactory (object):
    @staticmethod
    def make(parser):
        return AttachAllToken(parser).getToken()


class AttachImagesFactory (object):
    @staticmethod
    def make(parser):
        return AttachImagesToken(parser).getToken()


class AttachToken (object, metaclass=ABCMeta):
    attachString = u"Attach:"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        """
        Создать элементы из прикрепленных файлов.
        Отдельно картинки, отдельно все файлы
        """
        attachesAll = []

        attaches = Attachment(self.parser.page).attachmentFull
        attaches.sort(key=len, reverse=True)

        for attach in attaches:
            fname = os.path.basename(attach)
            if self.filterFile(fname):
                attach = Literal(fname)
                attachesAll.append(attach)

        finalToken = Literal(self.attachString) + concatenate(attachesAll)
        finalToken = finalToken.setParseAction(self.convertToLink)("attach")
        return finalToken

    def convertToLink(self, s, l, t):
        fname = t[1]

        if isImage(fname):
            return '<img src="%s/%s"/>' % (PAGE_ATTACH_DIR, fname)
        else:
            return '<a href="%s/%s">%s</a>' % (PAGE_ATTACH_DIR, fname, fname)

    @abstractmethod
    def filterFile(self, fname):
        """
        Должен возвращать True, если файл подходит для токена и False в противном случае
        """


class AttachAllToken (AttachToken):
    def filterFile(self, fname):
        return True


class AttachImagesToken (AttachToken):
    def filterFile(self, fname):
        return isImage(fname)
