"""Модуль **raw** содержит функции для расчета LOC-метрик файлов и 
функций.

Главные функции модуля: :func:`analyze_file`, :func:`analyze_files`, 
:func:`analyze_functions`. Только эти функции должны использоваться для
расчета метрик.
"""
from metrics import parser
from clang.cindex import CursorKind
from clang.cindex import TokenKind
from metrics import filters
import clang.cindex
import collections
from functools import reduce
import os.path

#: Объект RawMetrics, в полях объекта хранятся различные LOC-метрики.
#:
#: Объект RawMatrics - это :func:`collections.namedtuple` c полями для
#: хранения показателей LOC-метрик. Данный объект возвращается функциями
#: для расчета метрик.
#:
#: :Поля объекта:
#:    * loc (*int*) - общее количество строк кода (LOC)
#:    * lloc (*int*) - количество логических строк кода (LLOC)
#:    * ploc (*int*) - количество физических строк кода (PLOC)
#:    * comments (*int*) - количество строк комментариев
#:    * blanks (*int*) - количество пустых строк
#:
RawMetrics = collections.namedtuple('RawMetrics',
        ['loc', 'lloc', 'ploc', 'comments', 'blanks']
)

# Добавляем сигнатуру функции clang_Cursor_getCommentRange в список
# функций привязки Clang. Данный список регистрируется привязкой при 
# загрузке библиотеки.
clang.cindex.functionList.append(
        ('clang_Cursor_getCommentRange',
            [clang.cindex.Cursor],
            clang.cindex.SourceRange)
)

class PhysicalLineCounter:
    """Класс **PhysicalLineCounter** - это счетчик физических строк
    кода.

    Для подсчета физических строк необходимо использовать метод
    :meth:`count_cursor`. Итоговое количество строк можно получить методом
    :meth:`ploc`. Для сброса счетчика используется метод :meth:`reset`.
    """
    def __init__(self):
        self._physical_lines = set()

    @property
    def physical_lines(self):
        """Возвращает множество (:class:`frozenset`) номеров физических 
        строк.
        """
        return frozenset(self._physical_lines)

    def ploc(self):
        """Возвращает количество (*int*) физических строк."""
        return len(self._physical_lines)

    def count_cursor(self, node):
        """Добавляет физические строки курсора *node* к текущим 
        подсчитанным.

        :param node: курсор, который необходимо подсчитать
        :type node: clang.cindex.Cursor
        """

        if node.kind is not CursorKind.TRANSLATION_UNIT:
            self._physical_lines.add(node.location.line)

            if node.kind is CursorKind.COMPOUND_STMT:
                self._physical_lines.add(node.extent.end.line)

    def reset(self):
        """Cброс счетчика. Очищаем множество подсчитанных физических 
        строк."""
        self._physical_lines.clear()


def _count_comments(tokens):
    """Функция подсчитывает количество строк комментариев для списка 
    токенов *tokens*.

    :param tokens: список токенов, который получается из курсора методом :meth:`clang.cindex.Cursor.get_tokens`
    :type tokens: функция-генератор, которую возвращает :class:`clang.cindex.Token`
    :returns: кортеж (:class:`tuple`) вида (количество строк, множество (:class:`frozenset`) номеров строк)
    """
    comment_lines = set()

    for t in tokens:
        if t.kind is TokenKind.COMMENT:
            comment_lines.update(range(t.extent.start.line, 
                t.extent.end.line + 1))

    return (len(comment_lines), frozenset(comment_lines)) 


def _is_logical(node):
    """Булевая функция. Возвращает признак: является ли курсор *node* 
    логической строкой или нет.

    :param node: курсор
    :type node: :class:`clang.cindex.Cursor`
    :returns: признак
    :rtype: bool
    """
    return node.kind not in [CursorKind.DECL_STMT, 
            CursorKind.INTEGER_LITERAL, CursorKind.BINARY_OPERATOR, 
            CursorKind.UNEXPOSED_EXPR, CursorKind.DECL_REF_EXPR, 
            CursorKind.STRING_LITERAL, CursorKind.MACRO_INSTANTIATION,
            CursorKind.COMPOUND_STMT, CursorKind.TRANSLATION_UNIT,
            CursorKind.PARM_DECL]


def _analyze(cursor):
    lloc = 0
    pl_counter = PhysicalLineCounter()

    # Функция обратного вызова (callback), которая вызывается при обходе
    # AST методом traverse_ast
    def _loc_callback(node, parent):
        nonlocal lloc

        if _is_logical(node):
            lloc += 1

        pl_counter.count_cursor(node)

    loc = cursor.extent.end.line - 1
    parser.ClangSingleFileParser.traverse_ast(cursor, _loc_callback)
    comments, comment_lines = _count_comments(cursor.get_tokens())
    ploc = pl_counter.ploc()

    # Объединяем номера строк комментариев и физических строк
    no_blank_lines = reduce(frozenset.union, [comment_lines, 
                            pl_counter.physical_lines])

    blanks = loc - len(no_blank_lines)
        
    return RawMetrics(loc, lloc, ploc, comments, blanks)


def analyze_code(filename, source_code):
    """Функция подсчитывает LOC-метрики для исходного кода, 
    который хранится в памяти.

    Параметр *filename* используется для того, чтобы привязать код из памяти к имени файла.

    Функция возвращает объект :obj:`RawMetrics` с подсчитанными 
    LOC-метриками для указанного исходного кода.

    :param string filename: имя файла исходного кода
    :param string source_code: исходный код в памяти
    :returns: LOC-метрики файла
    :rtype: :obj:`RawMetrics`
    """
    cparser = parser.ClangSingleFileParser(
            parser.Option.PARSE_MACROS | parser.Option.PARSE_COMMENTS)
    cursor = cparser.parse_from_memory(filename, source_code)
    return _analyze(cursor)


def analyze_file(source_filepath):
    """Функция подсчитывает LOC-метрики для файла с указанным путем 
    *source_filepath*.

    Функция возвращает объект :obj:`RawMetrics` с подсчитанными 
    LOC-метриками для указанного файла.

    :param source_filepath: абсолютный путь к файлу
    :type source_filepath: string
    :returns: LOC-метрики файла
    :rtype: :obj:`RawMetrics`
    """
    cparser = parser.ClangSingleFileParser(
            parser.Option.PARSE_MACROS | parser.Option.PARSE_COMMENTS)
    cursor = cparser.parse(source_filepath)
    return _analyze(cursor)


def analyze_files(source_files):
    """Функция подсчитывает LOC-метрики для нескольких файлов с указанными
     путями *source_filepath*.

    Функция возвращает словарь (*dict*) объектов :obj:`RawMetrics` 
    с подсчитанными LOC-метриками для указанных файлов.

    :param source_files: список абсолютных путей к файлам
    :type source_files: list
    :returns: словарь LOC-метрик файлов ({название файла::obj:`RawMetrics`})
    :rtype: dict
    """
    common_prefix = os.path.commonprefix(source_files)
    return { os.path.relpath(fp, common_prefix):analyze_file(fp) 
            for fp in source_files }


def analyze_functions(source_files, func_list=None):
    """Функция подсчитывает LOC-метрики для нескольких функций в 
    нескольких файлах с указанными путями *source_filepath*.

    Функция возвращает словарь (*dict*) объектов :obj:`RawMetrics` 
    с подсчитанными LOC-метриками для нескольких функций. Также можно
    фильтровать функции по списку названий функций *func_list*. Если
    не передавать список названий (по-умолчанию), то метрики
    подсчитываются для всех функций в файлах.

    :param source_files: список абсолютных путей к файлам
    :type source_files: list
    :param func_list: список названий функций, для которых необходимо подсчитать LOC-метрики
    :type func_list: list
    :returns: словарь LOC-метрик файлов ({название функции::obj:`RawMetrics`})
    :rtype: dict
    """
    cparser = parser.ClangMultipleFilesParser(
            parser.Option.PARSE_MACROS | parser.Option.PARSE_COMMENTS)
    cparser.parse(source_files)

    ffilter = filters.FunctionFilter(func_list)
    pl_counter = PhysicalLineCounter()
    lloc = 0
    last_func_node = None
    last_func_name = None

    results = {}
    is_first_enter = True

    def save_result(func_node, func_name):
        loc = func_node.extent.end.line \
                - func_node.extent.start.line + 1
        comments, comment_lines = _count_comments(
                func_node.get_tokens())

        no_blank_lines = reduce(
                frozenset.union, 
                [comment_lines, pl_counter.physical_lines]
                )
        
        blanks = loc - len(no_blank_lines)

        results[func_name] = RawMetrics(
                loc, lloc, pl_counter.ploc(), comments, blanks)

    # Функция обратного вызова (callback), которая вызывается при обходе
    # AST методом traverse_ast
    def _loc_callback(node, parent):
        nonlocal lloc, is_first_enter, last_func_name, last_func_node

        if ffilter.filter(node):
            if ffilter.is_new_func_found:
                if is_first_enter:
                    is_first_enter = False
                    last_func_name = ffilter.current_func_name
                    last_func_node = node
                else:
                    save_result(last_func_node, last_func_name)
                    last_func_name = ffilter.current_func_name
                    last_func_node = node
                    pl_counter.reset()
                    lloc = 0

            if _is_logical(node):
                lloc += 1
            pl_counter.count_cursor(node)

    cparser.traverse_ast(_loc_callback)

    # Проверка в случае, если в файле вообще не было объявлений функций
    if last_func_node:
        save_result(last_func_node, last_func_name)
    
    return results
 
