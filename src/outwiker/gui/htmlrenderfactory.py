#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os


def getHtmlRender (parent):
    """
    Возвращает используемый HTML-рендер
    """
    if os.name == "nt":
        from htmlrenderie import HtmlRenderIE as HtmlRenderEngine
    else:
        from htmlrenderwebkit import HtmlRenderWebKit as HtmlRenderEngine

    return HtmlRenderEngine (parent)
