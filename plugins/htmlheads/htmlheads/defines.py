# -*- coding: utf-8 -*-
# Dummy function. It's needed for translation.
def _(msg): return msg

PLUGIN_NAME = 'HtmlHeads'
PLUGIN_URL = _('http://jenyay.net/Outwiker/HtmlHeadsEn')
PLUGIN_NAME_LOWERCASE = PLUGIN_NAME.lower()
PREFIX_ID = PLUGIN_NAME + '_'

PLUGIN_DESCRIPTION = _('''Plugin adds wiki-commands (:title:), (:description:), (:keywords:), (:htmlhead:) and (:htmlattrs:).

<b>Usage:</b>
(:title Page title:)

(:description Page description:)

(:keywords keyword_1, keyword_2, other keyword:)

(:htmlhead:)
&lt;meta http-equiv='Content-Type' content='text/html; charset=utf-8' /&gt;

&lt;meta name='robots' content='index,follow' /&gt;
(:htmlheadend:)

(:htmlattrs attr1="value" attr2="value":)
''')

MENU_HTMLHEADS = 'Plugin_%s' % PLUGIN_NAME
ACTION_DESCRIPTION = _('{} plugin. Insert (:%s ...:) command').format(PLUGIN_NAME)
