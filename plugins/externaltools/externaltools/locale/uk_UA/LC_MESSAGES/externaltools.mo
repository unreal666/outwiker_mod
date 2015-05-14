��    "      ,  /   <      �  ,   �  %   &     L     l     �     �     �     �     �     �  '   �            -   '  o   U  m   �  i   3  n   �               .     3     M     k  �       J  :   V     �  ;   �  >   �     &  
   ,  *   7  !  b  S   �  D   �  6     D   T     �  !   �     �  ;   �  7        P  C   _  %   �     �  F   �  �     �   �  �   �  �   m     7  &   D     k  @   ~  $   �  >   �  O  #  %   s  �   �  0   $  �   U  �   �     q     �  (   �                                       	                                             !                                    
          "                            %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Error Executables (*.exe)|*.exe|All Files|*.* External Tools [Plugin] ExternalTools ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Link Open Content File with... Open Result HTML File with... Open file dialog... Open notes files with external editor.

For OutWiker 1.9 and above ExternalTools adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command has the following optional parameters:
<ul>
<li>format. If the parameter equals "button" command will create a button instead of a link.</li>
<li>title. The parameter sets the text for link or button.</li>
</ul>

The (:exec:) command allow to run many applications. Every application must writed on the separated lines.

If line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.

<b>Examples</b>

Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>

Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>

Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code>

Run many applications:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>
 Remove tool Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Show warning before executing applications by (:exec:) command Title Tools List http://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: outwiker
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2015-05-13 22:18+0300
PO-Revision-Date: 2015-05-14 10:11+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: Ukrainian
Language: uk_UA
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
X-Generator: Poedit 1.5.4
X-Crowdin-Project: outwiker
X-Crowdin-Language: uk
X-Crowdin-File: externaltools.po
 %attach%. Шлях до поточної папки долучених файлів %folder%. Шлях до папки поточної сторінки %html%. Поточна сторінка. HTML-файл %page%. Поточна сторінка. Текстовий файл Всі Файли|* Додати застосунок Кнопка Не вдалося запустити застосунок Не вдалося зберегти параметри Помилка Виконувані файли (*.exe)|*.exe|Всі файли|*.* External Tools [Розширення] ExternalTools Додаток ExternalTools. Вставити команду (:exec:) Додаток ExternalTools. Вставити макрос %attach%. Цей макрос буде замінений на шлях до папки з долученими файлами поточної сторінки. Додаток ExternalTools. Вставити макрос %folder%. Цей макрос буде замінений на шлях до папки поточної сторінки. Додаток ExternalTools. Вставити макрос %html%. Цей макрос буде замінений на шлях до HTML-файлу поточної сторінки. Додаток ExternalTools. Вставити макрос %page%. Цей макрос буде замінений на шлях до текстового файлу поточної сторінки. Формат Вставка команди (:exec:) Посилання Відкрити файл з текстом нотатки в... Відкрити HTML-файл в... Діалогове вікно відкриття файлу... Відкриває файли нотаток у зовнішніх редакторах.

Для OutWiker 1.9 і вище ExternalTools додає команду (:exec:) для створення посилання або кнопки для запуску зовнішніх застосунків з викісторінки.

Команда (:exec:) має наступні необов'язкові параметри:
<ul>
<li>format. Якщо цей параметр дорівнює "button", то команда створить кнопку замість посилання (за замовчуванням).</li>
<li>title. Цей параметр задає текст для посилання або кнопки.</li>
</ul>

Команда (:exec:) дозволяє запускати декілька застосунків. Кожен застосунок має бути записаний на окремому рядку.

Якщо рядок починається з "#", то цей рядок ігнорується. "#" на початку рядка - це символ коментаря.

<b>Приклади</b>

Створення посилання для запуску application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>

Те ж саме, але для створення кнопки
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>

Створити посилання для запуску application.exe з параметрами:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code>

Запустити декілька застосунків:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>
 Видалити застосунок Запустити застосунок за допомогою додатку ExternalTools?
Це може бути небезпечно. Запустити застосунок (:exec:) Запустити застосунки за допомогою додатку ExternalTools?
Це може бути небезпечно. Показувати попередження перед запуском
застосунків за допомогою команди (:exec:) Заголовок Список засобів http://jenyay.net/Outwiker/ExternalTools 