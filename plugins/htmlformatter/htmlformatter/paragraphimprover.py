import re
from io import StringIO

from outwiker.core.htmlimprover import HtmlImprover


class ParagraphHtmlImprover(HtmlImprover):
    """
    Class cover paragraphes by <p> tags
    """
    def _appendLineBreaks(self, text):
        result = self._prepareText(text)
        result = self._coverParagraphs(result)
        result = self._addLineBreaks(result)
        result = self._improveRedability(result)

        return result

    def _prepareText(self, text):
        result = text

        closetags = r'[uod]l|li|d[td]'

        # Remove \n before some block elements
        pattern = r'\n(?=</(?:' + closetags + r')>)'
        result = re.sub(pattern, '', result, flags=re.I | re.M)

        return result

    def _improveRedability(self, text):
        result = text

        minopentags = r'[uod]l|hr|h\d|t[rdh]|blockquote'
        opentags = minopentags + r'|table'
        closetags = r'[uod]l|li|d[td]|t[rdh]|caption|table|thead|tfoot|tbody|colgroup|col|h\d|blockquote'

        # Replacement <section></p> with </p><section>
        result = re.sub(r'(<section[^>]*>)</p>', r'</p>\1', result, flags=re.I | re.M)
        # Replacement <p></section> with </section><p>
        result = re.sub(r'<p></section>', r'</section><p>', result, flags=re.I | re.M)

        # Remove <br> tag before some block elements
        remove_br_before = r'<br\s*/?>\s*(?=<(?:' + opentags + r')[ >]|</(?:' + closetags + r')>)'
        result = re.sub(remove_br_before, '', result, flags=re.I | re.M)

        # Remove <br> tag after some block elements
        remove_br_after = r'(<(?:' + opentags + r')(?: [^>]*?)?>|</(?:' + closetags + r')>)\s*<br\s*/?>'
        result = re.sub(remove_br_after, r'\1', result, flags=re.I | re.M)

        # Append </p> before some elements
        append_p_before = r'(?<!</p>)(<(?:h\d|blockquote|[uod]l)[ >])'
        result = re.sub(append_p_before, r'</p>\1', result, flags=re.I | re.M | re.S)

        # Append <p> after some closing elements
        append_p_after = r'(</(?:h\d|blockquote)>)(?!\s*(?:<p[ >]|</t[dh]>))'
        result = re.sub(append_p_after, r'\1<p>', result, flags=re.I | re.M | re.S)

        # Append <p> inside after some elements
        append_p_after_inside = r'(<(?:blockquote)(?: .*?)?>)'
        result = re.sub(append_p_after_inside, r'\1<p>', result, flags=re.I | re.M)

        # Append </p> inside before some closing elements
        append_p_before_inside = r'(</(?:blockquote)>)'
        result = re.sub(append_p_before_inside, r'</p>\1', result, flags=re.I | re.M)

        # Remove <p> tag before some block elements
        remove_p_before = r'<p>\s*(?=<(?:' + opentags + r')[ >])'
        result = re.sub(remove_p_before, '', result, flags=re.I | re.M)

        # Remove </p> tag after some block elements
        remove_p_after = r'(<(?:' + opentags + r')(?: [^>]*?)?>|</(?:' + closetags + r')>)\s*</p>'
        result = re.sub(remove_p_after, r'\1', result, flags=re.I | re.M)

        # Normalize <p>...</p> inside <div>
        append_p_inside = r'(?P<tag><div.*?>)'
        # append_p_inside = r'(?P<start><div.*?>)(?P<content>.*?)(?P<end></div>)'
        # append_p_inside = r'(?P<start><div((?!</div>).)*?>)(?P<content>((?!</div>).)*?</p>.*?)(?P<end></div>)'
        result = re.sub(append_p_inside,
                        '\\g<tag><p>',
                        result,
                        flags=re.I | re.M)
        result = result.replace('</div>', '</p></div>')

        # Remove <p> tag before div elements
        remove_p_before = r'<p>(?=<div.*?>)'
        result = re.sub(remove_p_before, '', result, flags=re.I)

        # Remove </p> after div element
        result = result.replace('</div></p>', '</div>\n')

        # Remove <p> inside <div> for single paragraph
        remove_single_p = r"(?P<start><div((?!</div>).)*?>)<p>(?P<content>((?!</div>|<p>).)*?)</p>(?P<end></div>)"
        result = re.sub(remove_single_p,
                        "\\g<start>\\g<content>\\g<end>",
                        result,
                        flags=re.I | re.M | re.S)

        # Remove empty paragraphs
        empty_par = r'<p></p>'
        result = re.sub(empty_par, '', result, flags=re.I | re.M)

        # Remove <br> on the paragraph end
        final_linebreaks = r'<br\s*/?>\s*(?=</p>)'
        result = re.sub(final_linebreaks, r'', result, flags=re.I | re.M)

        # Append line breaks before some elements (to improve readability)
        append_eol_before = r'\n*(<(?:li|h\d|/?[uo]l|hr|p|script|/?table|/?tr|td)[ >])'
        result = re.sub(append_eol_before, r'\n\1', result, flags=re.I | re.M)

        # Append line breaks after some elements (to improve readability)
        append_eol_after = r'(<(?:hr(?: [^>]*?)?/?|br\s*/?|/\s*(?:h\d|p|script|[uo]l|table))>)\n*'
        result = re.sub(append_eol_after, r'\1\n', result, flags=re.I | re.M)

        # Remove </p> at the begin and <p> at the end
        remove_p_start_end = r'^</p>|<p>$'
        result = re.sub(remove_p_start_end, '', result, flags=re.I)

        return result

    def _addLineBreaks(self, text):
        return text.replace('\n', '<br/>')

    def _coverParagraphs(self, text):
        paragraphs = (par.strip()
                      for par
                      in text.split('\n\n')
                      if len(par.strip()) != 0)

        buf = StringIO()
        for par in paragraphs:
            buf.write('<p>')
            buf.write(par)
            buf.write('</p>')

        return buf.getvalue()
