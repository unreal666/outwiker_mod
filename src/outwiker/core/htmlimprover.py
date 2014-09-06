# -*- coding: UTF-8 -*-

import re
# import timeit


class HtmlImprover (object):
    """
    Класс, который делает HTML более читаемым (где надо, расставляет переводы строк)
    """
    @staticmethod
    def run (text):
        """
        Сделать HTML более читаемым
        """
        stoptag = '{{{__NOHTMLIMPROVE__}}}'   # Стоп-тег, при присутствии которого HTML-код "улучшаться"" не будет.
        if stoptag not in text:
            # start_time = timeit.default_timer()
            text = HtmlImprover.__improveText (text)
            # print( 'Выполнено: ' + str(timeit.default_timer() - start_time))
        else:
            text = text.replace (stoptag, '')

        return text


    @staticmethod
    def __improveText (text):
        result = text.replace ("\r\n", "\n")
        result = HtmlImprover.__replaceEndlines (result)

        return result


    @staticmethod
    def __replaceEndlines (text):
        """
        Заменить переводы строк, но не трогать текст внутри <pre>...</pre>
        """
        text_lower = text.lower()

        starttag = "<pre"
        endtag = "</pre>"

        # Разобьем строку по <pre>
        part1 = text_lower.split (starttag)

        # Подстроки разобьем по </pre>
        parts2 = [item.split (endtag) for item in part1]

        # Склеим части в один массив
        parts = reduce (lambda x, y: x + y, parts2, [])

        # В четных элементах массива заменим переводы строк, а нечетные оставим как есть
        # Строки берем из исходного текста с учетом пропущенных в массиве тегов <pre> и </pre>
        result = u""
        index = 0

        for n in range (len (parts)):
            textitem = text[index: index + len (parts[n])]
            if n % 2 == 0:
                textitem = HtmlImprover.__improveTags (textitem)
                index += len (parts[n]) + len (starttag)
            else:
                textitem = "\n<pre" + textitem + "</pre>\n"
                index += len (parts[n]) + len (endtag)

            result += textitem

        return result


    @staticmethod
    def __improveTags (text):
        """
        Улучшения переводов строк до и после некоторых тегов
        """
        result = text
        result = re.sub(r'(\n+)\n\n', lambda m: '<p>&nbsp;</p>' * len(m.group(1)), result)
        result = result.replace ("\n\n", "<p>")
        result = result.replace ("\n", "<br>")

        # Компенсация восстановления переносов строк после списков
        ro0 = r"(?<=</[uo]l>)<p><br>(?=<[uo]l>)"
        result = re.sub(ro0, "\n\n", result, flags=re.I)

        # Сохраним исходный регистр тега <p>.
        # result = re.sub ("<(p)>", r"</\1>\n<\1>", result, flags=re.I)

        block_tags = r"[uod]l|h\d|pre|table|div|blockquote|hr"
        opening_tags = r"[uod]l|hr|h\d|table"
        inner_table_tags = r"t[rdh]|caption|thead|tfoot|tbody|colgroup|col"
        inner_list_tags = r"li|d[td]"
        closing_tags = inner_list_tags + "|" + inner_table_tags + r"|h\d"

        # Удаление тега <p> перед некоторыми блочными элементами
        remove_p_before = r"<p>(?=(?:<br>)?)(?=<(?:" + block_tags + r")[ >])"
        result = re.sub(remove_p_before, r"", result, flags=re.I)

        # Удаление тега </p> после некоторых блочных элементов
        remove_p_after = r"(</(?:" + block_tags + r")>|<hr ?/?>)</p>"
        result = re.sub(remove_p_after, r"\1", result, flags=re.I)

        # Удаление тега <br> перед некоторыми блочными элементами
        remove_br_before = r"<br\s*/?>[\s\n]*(?=<(?:" + opening_tags + r")[ >/])"
        result = re.sub(remove_br_before, "", result, flags=re.I)

        # Удаление тега <br> после некоторых блочных элементов
        remove_br_after = r"(<(?:" + opening_tags + r")( [^>]+)? ?/?>|</(?:" + closing_tags + r")>)[\s\n]*<br\s*/?>"
        result = re.sub(remove_br_after, r"\1", result, flags=re.I)

        # Удаление некоторого разного мусора/бесполезного кода
        remove_other_trash = r"<p>(?=</)"
        result = re.sub(remove_other_trash, "", result, flags=re.I)

        # Добавление переноса строки перед некоторыми элементами
        append_eol_before = r"\n*(?=<(?:h\d|/?[uod]l|/?table|p|div|blockquote)[\s>]|<hr\s*/?>)"
        result = re.sub(append_eol_before, "\n", result, flags=re.I)

        # Добавление переноса строки + табуляции перед некоторыми элементами
        append_eol_tab_before = r"\n*(?=<(?:" + inner_list_tags + "|" + inner_table_tags + ")[\s>])"
        result = re.sub(append_eol_tab_before, "\n\t", result, flags=re.I)

        # Добавление переноса строки после некоторых элементов
        append_eol_after = r"(<[hb]r\s*/?>|</\s*(?:h\d|[uod]l|table|p|div|blockquote)>)\n*"
        result = re.sub(append_eol_after, "\\1\n", result, flags=re.I)

        return result
