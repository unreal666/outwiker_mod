# -*- coding: utf-8 -*-

from .tokenfonts import FontsFactory
from .tokennoformat import NoFormatFactory
from .tokenpreformat import PreFormatFactory
from .tokenthumbnail import ThumbnailFactory
from .tokenheading import HeadingFactory
from .tokenadhoc import AdHocFactory
from .tokenhorline import HorLineFactory
from .tokenlink import LinkFactory
from .tokenalign import AlignFactory
from .tokentable import TableFactory
from .tokenurl import UrlFactory
from .tokenurlimage import UrlImageFactory
from .tokenattach import AttachFactory, AttachImagesFactory
from .tokenlist import ListFactory
from .tokenlinebreak import LineBreakFactory
from .tokenlinejoin import LineJoinFactory
from .tokencommand import CommandFactory
from .tokentext import TextFactory
from .tokenquote import QuoteFactory
from .tokendefinitionlist import DefinitionListFactory
from .tokenwikistyle import WikiStyleInlineFactory, WikiStyleBlockFactory
from .tokencomment import CommentFactory

tokens = {
    'italicized': FontsFactory.makeItalic,
    'bolded': FontsFactory.makeBold,
    'boldItalicized': FontsFactory.makeBoldItalic,
    'underlined': FontsFactory.makeUnderline,
    'strike': FontsFactory.makeStrike,
    'subscript': FontsFactory.makeSubscript,
    'superscript': FontsFactory.makeSuperscript,
    'quote': QuoteFactory.make,
    'code': FontsFactory.makeCode,
    'mark': FontsFactory.makeMark,
    'small': FontsFactory.makeSmall,
    'big': FontsFactory.makeBig,
    'headings': HeadingFactory.make,
    'thumb': ThumbnailFactory.make,
    'noformat': NoFormatFactory.make,
    'preformat': PreFormatFactory.make,
    'horline': HorLineFactory.make,
    'link': LinkFactory.make,
    'align': AlignFactory.make,
    'table': TableFactory.make,
    'url': UrlFactory.make,
    'urlImage': UrlImageFactory.make,
    'attaches': AttachFactory.make,
    'attachImages': AttachImagesFactory.make,
    'adhoctokens': AdHocFactory.make,
    'lists': ListFactory.make,
    'definitionList': DefinitionListFactory.make,
    'lineBreak': LineBreakFactory.make,
    'lineJoin': LineJoinFactory.make,
    'command': CommandFactory.make,
    'text': TextFactory.make,
    'wikistyle_inline': WikiStyleInlineFactory.make,
    'wikistyle_block': WikiStyleBlockFactory.make,
    'comment': CommentFactory.make,
}

def initTokens(obj, action=None, names=[], all=None):
    if all:
        names = tokens

    for name in names:
        if hasattr(obj, name): continue

        setattr(obj, name, tokens[name](obj))

        if action and name != 'text':
            getattr(obj, name).setParseAction(action)
